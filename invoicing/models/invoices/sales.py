# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
import itertools
from decimal import Decimal as D
from functools import reduce

from django.db import models
from django.db.models import Q
from django.utils import timezone

import inventory
from accounting.models import (Account,
                             Journal, 
                             JournalEntry, 
                             Tax,
                             Post,
                             Ledger)
from common_data.models import Person, SingletonModel
from employees.models import Employee
from invoicing.models.payment import Payment
from services.models import Service

from .abstract import AbstractSale


class SalesInvoice(AbstractSale):
    '''used to charge for finished products'''
    DEFAULT_WAREHOUSE = 1 #make fixture
    purchase_order_number = models.CharField(blank=True, max_length=32)
    #add has returns field
    ship_from = models.ForeignKey('inventory.WareHouse', on_delete=models.SET_NULL, null=True,
         default=DEFAULT_WAREHOUSE)

    def add_product(self, product, quantity):
        self.salesinvoiceline_set.create(
            product=product, 
            quantity=quantity,
            price=product.unit_sales_price,
            invoice=self
        )

    @property
    def returned_total(self):
        return reduce(lambda x,y: x + y, 
            [i.returned_value for i in self.salesinvoiceline_set.all()], 0)

    @property
    def subtotal(self):
        return reduce(lambda x, y: x+ y, 
            [i.subtotal for i in self.salesinvoiceline_set.all()], 0)

    @property
    def cost_of_goods_sold(self):
        # TODO test
        total = 0
        for line in self.salesinvoiceline_set.all():
            total += line.value

        return total


    def update_inventory(self):
        #called in views.py
        for line in self.salesinvoiceline_set.all():
            #check if ship_from has the product in sufficient quantity
             self.ship_from.decrement_item(line.product, line.quantity)

    def create_entry(self):
        #verified
        '''sales entries debits the inventory and in the case of credit 
        sales credits the customer account or the cash book otherwise.
        First a journal entry is made to debit the inventory and credit the 
        customer account. If the invoice is on credit nothing further happens.
        However if it is a cash invoice, the payment object is created along with its accompanying entry.'''
        #only one entry per invoice
        if self.entry:
            return
        j = JournalEntry.objects.create(
                memo= 'Auto generated entry from sales invoice.',
                date=self.date,
                journal =Journal.objects.get(pk=3),#Sales Journal
                created_by = self.salesperson.employee.user
            )
        j.credit(self.subtotal, Account.objects.get(pk=4000))#sales
        j.debit(self.total, self.customer.account)
        if self.tax_amount > D(0):
            j.credit(self.tax_amount, Account.objects.get(pk=2001))#sales tax
        
        # purchases for cost of goods sold
        j.debit(self.cost_of_goods_sold, Account.objects.get(pk=4006))
        #inventory
        j.credit(self.cost_of_goods_sold, Account.objects.get(pk=1004))

        self.entry = j
        self.save()

        #posting to accounts receivable
        
        return j

class SalesInvoiceLine(models.Model):
    invoice = models.ForeignKey('invoicing.SalesInvoice',
        on_delete=models.CASCADE,)
    product = models.ForeignKey("inventory.Product", on_delete=models.SET_NULL, 
        null=True)
    quantity = models.FloatField(default=0.0)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)
    discount = models.DecimalField(max_digits=4, decimal_places=2, default=0.0)
    returned_quantity = models.FloatField(default=0.0)
    returned = models.BooleanField(default=False)
    # value is calculated once when the invoice is generated to prevent 
    # distortions as prices change
    value = models.DecimalField(max_digits=4, decimal_places=2, default=0.0)
    
    @property
    def subtotal(self):
        return D(self.quantity) * self.price

    def _return(self, quantity):
        self.returned_quantity += float(quantity)
        self.returned = True
        self.save()

    def set_value(self):
        # TODO test
        self.value = self.product.stock_value * D(self.quantity)
        self.save()

    @property
    def returned_value(self):
        if self.price == D(0.0):
            return self.product.unit_sales_price * D(self.returned_quantity)
        return self.price * D(self.returned_quantity)

    def save(self, *args, **kwargs):
        super(SalesInvoiceLine, self).save(*args, **kwargs)
        if self.returned_quantity > 0:
            self.returned = True
            
        if self.price == 0.0 and self.product.unit_sales_price != D(0.0):
            self.price = self.product.unit_sales_price
            self.save()

        if self.value == D(0.0) and self.product.stock_value > D(0.0):
            self.set_value()