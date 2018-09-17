# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from functools import reduce
import datetime
from django.db import models
from django.db.models import Q
from decimal import Decimal as D
from django.utils import timezone

from services.models import Service
from accounting.models import Account, Journal, JournalEntry, Tax, Expense
import itertools
from invoicing import models as inv_models


class AbstractSale(models.Model):
    DEFAULT_TAX = 1
    DEFAULT_SALES_REP = 1
    DEFAULT_CUSTOMER = 1
    SALE_STATUS = [
        ('quotation', 'Quotation'),
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('paid', 'Paid In Full'),
        ('paid-partially', 'Paid Partially'),
        ('reversed', 'Reversed'),
    ]
    status = models.CharField(max_length=16, choices=SALE_STATUS)
    customer = models.ForeignKey("invoicing.Customer", on_delete=None,default=DEFAULT_CUSTOMER)
    salesperson = models.ForeignKey('invoicing.SalesRepresentative',
        on_delete=None, default=DEFAULT_SALES_REP)
    active = models.BooleanField(default=True)
    due= models.DateField( default=datetime.date.today)
    date= models.DateField(default=datetime.date.today)
    discount = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)
    tax = models.ForeignKey('accounting.Tax', on_delete=None,blank=True, 
        null=True)
    terms = models.CharField(max_length = 128, blank=True)
    comments = models.TextField(blank=True)
    
    @property
    def overdue(self):
        TODAY = timezone.now().date()

        if self.due < TODAY:
            return (self.due - TODAY).days
        return 0
        
    @staticmethod
    def abstract_filter(filter):
        '''wrap all filters in one Q object and pass it to this function'''
        sales = inv_models.SalesInvoice.objects.filter(filter)
        service = inv_models.ServiceInvoice.objects.filter(filter)
        bill = inv_models.Bill.objects.filter(filter)
        combined = inv_models.CombinedInvoice.objects.filter(filter)
        invoices = itertools.chain(sales, service, bill, combined)

        return invoices

    def delete(self):
        self.active = False
        self.save()
    
    @property
    def total(self):
        return self.subtotal + self.tax_amount

    @property
    def on_credit(self):
        # might need to improve the logic
        return self.status == 'sent' and self.due < self.date

    @property
    def total_paid(self):
        return reduce(lambda x,y: x + y, 
            [p.amount for p in self.payment_set.all()], 0)

    @property
    def total_due(self):
        return self.total - self.total_paid

    @property
    def tax_amount(self):
        if self.tax:
            return self.subtotal * D((self.tax.rate / 100.0)).quantize(D('1.00'))
        return 0

    @property
    def subtotal(self):
        raise NotImplementedError()

    def __str__(self):
        return 'SINV' + str(self.pk)

    def save(self, *args, **kwargs):
        super(AbstractSale, self).save(*args, **kwargs)
        config = inv_models.SalesConfig.objects.first()
        if self.tax is None and config.sales_tax is not None:
            self.tax = config.sales_tax
            self.save()