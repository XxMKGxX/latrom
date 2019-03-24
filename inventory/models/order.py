# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
from decimal import Decimal as D
from functools import reduce

import rest_framework
from django.conf import settings
from django.db import models
from django.db.models import Q

import inventory
from accounting.models import Account, Journal, JournalEntry
from common_data.models import SingletonModel, SoftDeletionModel

from .warehouse_models import StorageMedia, WareHouseItem

# TODO i need to separate the order types into product, consumable and 
# equipment orders. Each order has its own entries 

class Order(SoftDeletionModel):
    '''The record of all purchase orders for inventory of items that 
    will eventually be sold. Contains the necessary data to update 
    inventory and update the Purchases Journal.
    An aggregate with the OrderItem class.
    A cash order creates a transaction creation.
    A deferred payment pays on the deferred date.(Not yet implemented)
    A pay on receipt order creates the transaction when receiving a 
    goods received voucher.

    properties
    ------------
    total - returns the total value of the items ordered.
    received_total - returns the numerical value of items received
    fully_received - returns a boolean if all the ordered items have 
        been received.
    percent_received - is the percentage of the order that has been
        fulfilled by the supplier.
    
    methods
    -------------
    receive - quickly generates a stock receipt where all items are 
        marked fully received 
    '''
    ORDER_STATUS_CHOICES = [
        ('received-partially', 'Partially Received'),
        ('received', 'Received in Total'),
        ('draft', 'Internal Draft'),
        ('order', 'Order')
    ]
    
    expected_receipt_date = models.DateField()
    date = models.DateField()
    due = models.DateField(blank=True, null=True)
    supplier = models.ForeignKey('inventory.supplier', 
        on_delete=models.SET_NULL, null=True, default=1)
    supplier_invoice_number = models.CharField(max_length=32, 
        blank=True,  default="")
    bill_to = models.CharField(max_length=128, blank=True, 
        default="")
    ship_to = models.ForeignKey('inventory.WareHouse', 
        on_delete=models.SET_NULL, null=True)
    tax = models.ForeignKey('accounting.Tax',on_delete=models.SET_NULL, null=True, 
        default=1)
    tracking_number = models.CharField(max_length=64, blank=True, 
        default="")
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=24, 
        choices=ORDER_STATUS_CHOICES)
    received_to_date = models.FloatField(default=0.0)
    issuing_inventory_controller = models.ForeignKey('auth.user', 
        default=1, on_delete=models.SET_NULL, null=True)
    entry = models.ForeignKey('accounting.JournalEntry',
         blank=True, on_delete=models.SET_NULL, null=True, related_name="order_entry")
    shipping_cost_entries = models.ManyToManyField('accounting.JournalEntry', 
        related_name="shipping_cost_entries")

    @property
    def total_shipping_costs(self):
        # TODO test
        return sum([e.total_credits  for e in self.shipping_cost_entries.all()])

    @property
    def percentage_shipping_cost(self):
        return (float(self.total_shipping_costs) / float(self.total)) * 100.0
    


    def __str__(self):
        return 'ORD' + str(self.pk)

    # TODO test
    @property
    def product_total(self):
        return sum([i.subtotal for i in self.orderitem_set.filter(
            item_type = 1)])

    @property
    def equipment_total(self):
        return sum([i.subtotal for i in self.orderitem_set.filter(
            item_type = 3)])

    @property
    def consumables_total(self):
        return sum([i.subtotal for i in self.orderitem_set.filter(
            item_type = 2)])

    @property
    def items(self):
        return self.orderitem_set.all()

    @property
    def total(self):
        return self.subtotal + self.tax_amount
        

    @property
    def subtotal(self):
        return sum([i.subtotal for i in self.orderitem_set.all()])

    @property
    def tax_amount(self):
        if self.tax:
            return self.subtotal * (D(self.tax.rate) / D(100))
        return D(0.0)
    
    @property
    def payments(self):
        return inventory.models.item_management.OrderPayment.objects.filter(order=self)
    
    @property
    def total_due(self):
        total_paid = sum([i.amount for i in self.payments])
        return self.total - total_paid

    @property
    def payment_status(self):
        total_paid = sum([i.amount for i in self.payments])
        if total_paid >= self.total:
            return "paid"
        elif total_paid > 0 and total_paid < self.total:
            return "paid-partially"
        else:
            return "unpaid"

    @property
    def received_total(self):
        return sum([i.received_total for i in self.orderitem_set.all()])
    
    @property
    def fully_received(self):
        for item in self.items:
            if item.fully_received == False : return False
        return True

    @property
    def percent_received(self):
        items = self.orderitem_set.all()
        n_items = items.count()
        received = 0
        for item in items:
            if item.fully_received == True : 
                received += 1
        return (float(received) / float(n_items)) * 100.0

    def create_entry(self):
        #verified
        if not self.entry:
            j = JournalEntry.objects.create(
                    date=self.date,
                    memo = self.notes,
                    journal = Journal.objects.get(pk=4),
                    created_by = self.issuing_inventory_controller,
                    draft=False
                )

            #accounts payable
            # since we owe the supplier
            if not self.supplier.account:
                self.supplier.create_account()
            j.credit(self.total, self.supplier.account)
            j.debit(self.subtotal, Account.objects.get(pk=4006))#purchases
            j.debit(self.tax_amount, Account.objects.get(pk=2001))#tax
        else:
            j = self.entry

        if not self.entry:
            self.entry = j
    
        
    def receive(self):
        if self.status != 'received':
            sr = inventory.models.item_management.StockReceipt.objects.create(
                    order=self,
                    receive_date= datetime.date.today(),
                    note = 'Autogenerated receipt from order number' + \
                        str(self.pk),
                    fully_received=True
                )
            for item in self.orderitem_set.all():
                item.receive(item.quantity)
            self.status = 'received'
            self.save()

    #check for deffered date with deferred type of invoice

    @property
    def returned_total(self):
        return sum([i.returned_value for i in self.orderitem_set.all()])

class OrderItem(models.Model):
    '''A component of an order this tracks the order price 
    of an item its quantity and how much has been received.
    
    methods
    -----------
    receive - takes a number and adds its value to the item inventory
        and the orderitem's received quantity field.
    
    properties
    -----------
    received_total - returns the cash value of the items received
    subtotal - returns the cash value of the items ordered
    '''
    ITEM_TYPE_CHOICES =[
        (1, 'Product'),
        (2, 'Consumable'),
        (3, 'Equipment'),
        (4, 'Raw Material')
        ]
    order = models.ForeignKey('inventory.Order', 
        on_delete=models.SET_NULL, null=True)
    item = models.ForeignKey('inventory.inventoryitem', 
        null=True,
        on_delete=models.SET_NULL)
    quantity = models.FloatField()
    unit = models.ForeignKey('inventory.UnitOfMeasure', 
        on_delete=models.SET_NULL, null=True, default=1)
    order_price = models.DecimalField(max_digits=6, decimal_places=2)
    received = models.FloatField(default=0.0)

    @property
    def returned_quantity(self):
        return sum([dn.quantity \
            for dn in inventory.models.debit_note.DebitNoteLine.objects.filter(item=self)])


    @property
    def fully_received(self):
        if self.received < self.quantity:
            return False
        return True

    def receive(self, n, medium=None):
        n= float(n)
        self.received += n
        
        wh_item = self.order.ship_to.add_item(self.item, n, location=medium)
        
        self.item.set_purchase_price(self.order_price)
            
        self.save()
        
    def __str__(self):
        return str(self.item) + ' -' + str(self.order_price)

        
    @property
    def received_total(self):
        '''The total value of the item as received'''
        return D(self.received)  * self.order_price

    @property
    def subtotal(self):
        '''The total value of the item as ordered, not received'''
        return D(self.quantity) * self.order_price

    @property
    def returned(self):
        return self.returned_quantity > 0


    def _return_to_vendor(self, n):
        self.order.ship_to.decrement_item(self.item, n)
        

    @property
    def returned_value(self):
        return D(self.returned_quantity) * self.order_price