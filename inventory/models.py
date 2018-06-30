# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime

from django.db import models
from django.conf import settings
from invoicing.models import Invoice, InvoiceItem
from accounting.models import Account, Transaction


class Supplier(models.Model):
    name = models.CharField(max_length=64)
    contact_person = models.CharField(max_length=64, blank=True, default="")
    physical_address = models.CharField(max_length=128, blank=True, default="")
    telephone = models.CharField(max_length=16, blank=True, default="")
    email = models.EmailField(max_length=64, blank=True, default="")
    website = models.CharField(max_length=64, blank=True, default="")
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Item(models.Model):
    item_name = models.CharField(max_length = 32)
    code = models.AutoField(primary_key=True)
    unit = models.ForeignKey('inventory.UnitOfMeasure', blank=True, default="")
    unit_sales_price = models.FloatField()
    unit_purchase_price = models.FloatField()
    description = models.TextField(blank=True, default="")
    supplier = models.ForeignKey("inventory.Supplier", blank=True, null=True)
    image = models.FileField(blank=True, null=True, upload_to=settings.MEDIA_ROOT)
    quantity = models.FloatField(blank=True, default=0)
    minimum_order_level = models.IntegerField( default=0)
    maximum_stock_level = models.IntegerField(default=0)
    category = models.ForeignKey('inventory.Category', blank=True, null=True)
    sub_category = models.ForeignKey('inventory.Category', 
       related_name='sub_category', blank=True, null=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.code) + " - " + self.item_name

    @property
    def stock_value(self):
        return self.unit_sales_price * self.quantity
        
    @property
    def sales_to_date(self):
        items = InvoiceItem.objects.filter(item=self)
        total_sales = reduce(lambda x,y: x + y, [item.quantity * item.price for item in items], 0)
        return total_sales
    
    def increment(self, amount):
        self.quantity += float(amount)
        self.save()
        return self.quantity

    def decrement(self, amount):
        self.quantity -= float(amount)
        self.save()
        return self.quantity

class Order(models.Model):
    expected_receipt_date = models.DateField()
    issue_date = models.DateField()
    type_of_order = models.IntegerField(choices=[
        (0, 'Cash Order'),
        (1, 'Deffered Payment Order'),
        (2, 'Pay on Receipt') ], default=0)
    deferred_date = models.DateField(blank=True, null=True)
    supplier = models.ForeignKey('inventory.supplier', blank=True, null=True)
    bill_to = models.CharField(max_length=128, blank=True, default="")
    ship_to = models.CharField(max_length=128, blank=True, default="")
    tracking_number = models.CharField(max_length=64, blank=True, default="")

    notes = models.TextField(blank=True, default="")
    status = models.CharField(max_length=16, choices=[
        ('received', 'Received'),
        ('draft', 'Draft'),
        ('submitted', 'Submitted')
    ])
    active = models.BooleanField(default=True)
    
    def __str__(self):
        return 'ORD' + str(self.pk)

    @property
    def total(self):
        return reduce(lambda x, y: x + y , [item.subtotal for item in self.orderitem_set.all()], 0)

    
    @property
    def fully_received(self):
        for item in self.orderitem_set.all():
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

        return (float(received) / float(n_items)) * 100

    def receive(self):
        if self.status != 'received':
            StockReceipt.objects.create(
                    order=self,
                    receive_date= datetime.date.today(),
                    note = 'Autogenerated receipt from order number' + \
                        str(self.pk),
                    fully_received=True
                )
            for item in self.orderitem_set.all():
                item.receive(item.quantity)

    def save(self, *args, **kwargs):
        if self.type_of_order == 1:
            if self.deferred_date == None:
                raise ValueError('The Order with a deferred payment must have a deferred payment date.')
        else:
            super(Order, self).save(*args, **kwargs)

class OrderItem(models.Model):
    order = models.ForeignKey('inventory.Order', null=True)
    item = models.ForeignKey('inventory.item', null=True)
    quantity = models.FloatField()
    #change and move this to the item
    #make changes to the react app as well
    order_price = models.FloatField()
    received = models.FloatField(default=0.0)

    @property
    def fully_received(self):
        if self.received < self.quantity:
            return False
        return True

    def receive(self, n):
        self.received += float(n)
        self.item.quantity += float(n)
        self.item.save()
        self.save()
        
    def __str__(self):
        return str(self.item) + ' -' + str(self.order_price)

    def save(self, *args, **kwargs):
        if not self.order_price:
            self.order_price = self.item.unit_purchase_price
        super(OrderItem, self).save(*args, **kwargs)
        

    @property
    def subtotal(self):
        return self.quantity * self.order_price

class UnitOfMeasure(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField(default="")
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField(default="")

    def __str__(self):
        return self.name

class StockReceipt(models.Model):
    order = models.ForeignKey('inventory.Order', null=True)
    receive_date = models.DateField()
    note =models.TextField(blank=True, default="")
    fully_received = models.BooleanField(default=False)
    #deprecate
    def __str__(self):
        return str(self.pk) + ' - ' + str(self.receive_date)