# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.test import TestCase, Client
from django.urls import reverse

import models
from latrom import settings
from accounting.tests import create_account_models
from accounting.models import Transaction
from inventory.tests import create_test_inventory_models

TODAY = datetime.date.today()

settings.TEST_RUN_MODE = True

def create_test_invoicing_models(cls):
    cls.customer = models.Customer.objects.create(
        first_name = "First",
        last_name = 'Last',
        address = 'Somewhere',
        email='mai@mail.com',
        phone='12343243',
        billing_address='somwewhere',
        account = cls.account_c
    )
    
    cls.salesrep = models.SalesRepresentative.objects.create(
        employee=cls.employee
    )
    
    cls.invoice = models.Invoice.objects.create(
        type_of_invoice='cash',
        customer=cls.customer,
        date_issued= TODAY,
        due_date = TODAY,
        comments = "TEst Comment",
        tax = cls.tax,
        salesperson = cls.salesrep,
        account = cls.account_c
    )

    cls.invoice_c = models.Invoice.objects.create(
        type_of_invoice='credit',
        customer=cls.customer,
        date_issued= TODAY,
        due_date = TODAY,
        comments = "TEst Comment",
        tax = cls.tax,
        salesperson = cls.salesrep,
        account = cls.account_c
    )

    cls.invoice_item = models.InvoiceItem.objects.create(
        invoice =cls.invoice,
        item = cls.item,
        quantity= 10
    )

    cls.invoice_item_c = models.InvoiceItem.objects.create(
        invoice =cls.invoice_c,
        item = cls.item,
        quantity= 10
    )
    
    cls.payment = models.Payment.objects.create(
        invoice = cls.invoice_c,
        amount=110,
        date= TODAY,
        method = 'cash',
        sales_rep = cls.salesrep
    )
    cls.quote = models.Quote.objects.create(
        date=TODAY,
        customer = cls.customer,
        salesperson = cls.salesrep,
        comments = "comment",
        tax = cls.tax,
    )
    cls.quote_item = models.QuoteItem.objects.create(
        quote = cls.quote,
        item =cls.item,
        quantity=10
    )
    cls.receipt = models.Receipt.objects.create(
        payment= cls.payment,
        comments = "comment"
    )


class ModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        create_account_models(cls)
        create_test_inventory_models(cls)
        create_test_invoicing_models(cls)

    def test_create_customer(self):
        cus = models.Customer.objects.create(
            first_name = "First",
            last_name = 'Last',
            address = 'Somewhere',
            email='mai@mail.com',
            phone='12343243',
            billing_address='somwewhere',
            account = self.account_c
        )
        self.assertTrue(isinstance(cus, models.Customer))

    def test_create_invoice(self):
        inv = models.Invoice.objects.create(
            type_of_invoice='cash',
            customer=self.customer,
            date_issued= TODAY,
            due_date = TODAY,
            comments = "TEst Comment",
            tax = self.tax,
            salesperson = self.salesrep,
            account = self.account_c
        )
        self.assertIsInstance(inv, models.Invoice)

    def test_create_sales_rep(self):
        # too lazy to create more than one employee
        self.assertTrue(models.SalesRepresentative.objects.all().count() == 1)


    def test_create_invoice_item(self):
        obj = models.InvoiceItem.objects.create(
            invoice =self.invoice,
            item = self.item,
            quantity= 10
        )
        self.assertIsInstance(obj, models.InvoiceItem)

    def test_create_payment(self):
        # too lazy to create additional invoices
        self.assertTrue(models.Payment.objects.all().count() == 1)

    def test_create_quote(self):
        obj  = models.Quote.objects.create(
            date=TODAY,
        customer = self.customer,
        salesperson = self.salesrep,
        comments = "comment",
        tax = self.tax,
        )
        self.assertIsInstance(obj, models.Quote)

    def test_create_quote_item(self):
        obj  = models.QuoteItem.objects.create(
            quote = self.quote,
            item =self.item,
            quantity=10
        )
        self.assertIsInstance(obj, models.QuoteItem)

    def test_create_receipt(self):
        #too lazy to create additional payment
        self.assertTrue(models.Receipt.objects.all().count() == 1)

    def test_invoice_subtotal(self):
        self.assertEqual(self.invoice.subtotal, 100)

    def test_invoice_tax_amount(self):
        self.assertEqual(self.invoice.tax_amount, 10)

    def test_invoice_total(self):
        self.assertEqual(self.invoice.total, 110)

    def test_invoice_create_payment_error(self):
        self.assertRaises(ValueError, self.invoice.create_payment)

    def test_invoice_create_payment(self):
        inv = models.Invoice.objects.create(
            type_of_invoice='credit',
            customer=self.customer,
            date_issued= TODAY,
            due_date = TODAY,
            comments = "TEst Comment",
            tax = self.tax,
            salesperson = self.salesrep,
            account = self.account_c
        )
        self.assertIsInstance(inv.create_payment(), models.Payment)

    def test_invoice_create_transaction(self):
        self.assertIsInstance(self.invoice.create_transaction(), Transaction)

    def test_invoice_update_inventory(self): 
        self.invoice.update_inventory()
        self.assertEqual(
            self.invoice.invoiceitem_set.first().item.quantity, 0)
        self.invoice.invoiceitem_set.first().item.increment(10)
        
    def test_invoice_item_total_wout_discount(self):
        self.assertEqual(self.invoice_item.total_without_discount, 100)

    def test_invoice_item_subtotal(self):
        #includes discount
        self.invoice_item.discount = 10
        self.invoice_item.save()
        self.assertEqual(self.invoice_item.subtotal, 100)
        
        #undo changes
        self.invoice_item.discount = 0
        self.invoice_item.save()

    def test_invoice_item_price_update(self):
        self.invoice_item.item.unit_sales_price=100
        self.invoice_item.item.save()
        self.invoice_item.update_price()
        self.assertEqual(self.invoice_item.price, 100)
        
        #roll back changes
        self.invoice_item.item.unit_sales_price=10
        self.invoice_item.item.save()
        self.invoice_item.update_price()

    def test_sales_rep_sales(self):
        self.assertEqual(self.salesrep.sales(TODAY, TODAY), 200)

    def test_payment_due(self):
        self.assertEqual(self.payment.due, 0)

    def test_create_receipt(self):
        inv = models.Invoice.objects.create(
            type_of_invoice='credit',
            customer=self.customer,
            date_issued= TODAY,
            due_date = TODAY,
            comments = "TEst Comment",
            tax = self.tax,
            salesperson = self.salesrep,
            account = self.account_c
        )
        pmt = models.Payment.objects.create(
            invoice = inv,
        amount=100,
        date= TODAY,
        method = 'cash',
        sales_rep = self.salesrep
        )
        r = pmt.create_receipt()
        self.assertIsInstance(r, models.Receipt)
        
        #roll back
        r.delete()
        pmt.delete()
        inv.delete()

    def test_quote_subtotal(self):
        self.assertEqual(self.quote.subtotal, 100)

    def test_quote_total(self):
        self.assertEqual(self.quote.total, 110)

    def test_quote_tax(self):
        self.assertEqual(self.quote.tax_amount, 10)

    def test_create_invoice_from_quote(self):
        inv = self.quote.create_invoice()
        self.assertIsInstance(inv, models.Invoice)
        #roll back
        inv.delete()

    def test_quote_item_total_wout_discount(self):
        self.assertEqual(self.quote_item.total_without_discount, 100)

    def test_quote_item_subtotal(self):
        self.quote_item.discount = 10
        self.quote_item.save()
        self.assertEqual(self.quote_item.subtotal, 90)
        #rollback
        self.quote_item.discount = 0
        self.quote_item.save()
        
    def test_quote_update_price(self):
        self.quote_item.item.unit_sales_price = 100
        self.quote_item.item.save()
        self.quote_item.update_price()
        self.assertEqual(self.quote_item.price, 100)
        #rollback
        self.quote_item.item.unit_sales_price = 10
        self.quote_item.item.save()

class ViewTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super(ViewTests, cls).setUpClass()
        cls.client = Client()

    @classmethod
    def setUpTestData(cls):
        create_account_models(cls)
        create_test_inventory_models(cls)
        create_test_invoicing_models(cls)

    def test_get_home(self):
        resp = self.client.get(reverse('invoicing:home'))
        self.assertEqual(resp.status_code, 200)

    def test_get_config(self):
        resp = self.client.get(reverse('invoicing:config'))
        self.assertEqual(resp.status_code, 200)

    def test_get_create_customer_form(self):
        resp = self.client.get(reverse('invoicing:create-customer'))
        self.assertEqual(resp.status_code, 200)

    def test_get_quick_customer(self):
        resp = self.client.get(reverse('invoicing:quick-customer'))
        self.assertEqual(resp.status_code, 200)

    def test_get_customer_update(self):
        resp = self.client.get(reverse('invoicing:update-customer',
            kwargs={
                'pk': self.customer.pk
            }))
        self.assertEqual(resp.status_code, 200)

    def test_get_customer_delete(self):
        resp = self.client.get(reverse('invoicing:delete-customer',
            kwargs={
                'pk': self.customer.pk
            }))
        self.assertEqual(resp.status_code, 200)

    def test_get_payment_list(self):
        resp = self.client.get(reverse('invoicing:payments-list'))
        self.assertEqual(resp.status_code, 200)

    def test_get_payment_form(self):
        resp = self.client.get(reverse('invoicing:create-payment'))
        self.assertEqual(resp.status_code, 200)

    def test_get_payment_update(self):
        resp = self.client.get(reverse('invoicing:update-payment',
            kwargs={
                'pk': self.customer.pk
            }))
        self.assertEqual(resp.status_code, 200)

    def test_get_payment_delete(self):
        resp = self.client.get(reverse('invoicing:delete-payment',
            kwargs={
                'pk': self.customer.pk
            }))
        self.assertEqual(resp.status_code, 200)


    def test_get_sales_rep_list(self):
        resp = self.client.get(reverse('invoicing:sales-rep-list'))
        self.assertEqual(resp.status_code, 200)

    def test_get_sales_rep_form(self):
        resp = self.client.get(reverse('invoicing:create-sales-rep'))
        self.assertEqual(resp.status_code, 200)

    def test_get_sales_rep_update(self):
        resp = self.client.get(reverse('invoicing:update-sales-rep',
            kwargs={
                'pk': self.salesrep.pk
            }))
        self.assertEqual(resp.status_code, 200)

    def test_get_sales_rep_delete(self):
        resp = self.client.get(reverse('invoicing:delete-sales-rep',
            kwargs={
                'pk': self.salesrep.pk
            }))
        self.assertEqual(resp.status_code, 200)

    def test_get_invoices_list(self):
        resp = self.client.get(reverse('invoicing:invoices-list'))
        self.assertEqual(resp.status_code, 200)

    def test_get_invoice_form(self):
        resp = self.client.get(reverse('invoicing:create-invoice'))
        self.assertEqual(resp.status_code, 200)

    def test_get_invoice_update(self):
        resp = self.client.get(reverse('invoicing:update-invoice',
            kwargs={
                'pk': self.invoice.pk
            }))
        self.assertEqual(resp.status_code, 200)

    def test_get_invoice_detail(self):
        resp = self.client.get(reverse('invoicing:invoice-details',
            kwargs={
                'pk': self.invoice.pk
            }))
        self.assertEqual(resp.status_code, 200)

    def test_get_invoice_delete(self):
        resp = self.client.get(reverse('invoicing:delete-invoice',
            kwargs={
                'pk': self.invoice.pk
            }))
        self.assertEqual(resp.status_code, 200)


    def test_get_quote_list(self):
        resp = self.client.get(reverse('invoicing:quote-list'))
        self.assertEqual(resp.status_code, 200)

    def test_get_quote_form(self):
        resp = self.client.get(reverse('invoicing:create-quote'))
        self.assertEqual(resp.status_code, 200)

    def test_get_quote_update(self):
        resp = self.client.get(reverse('invoicing:quote-update',
            kwargs={
                'pk': self.quote.pk
            }))
        self.assertEqual(resp.status_code, 200)

    def test_get_quote_detail(self):
        resp = self.client.get(reverse('invoicing:quote-detail',
            kwargs={
                'pk': self.quote.pk
            }))
        self.assertEqual(resp.status_code, 200)

    def test_get_quote_delete(self):
        resp = self.client.get(reverse('invoicing:delete-quote',
            kwargs={
                'pk': self.quote.pk
            }))
        self.assertEqual(resp.status_code, 200)

    def test_get_receipt_list(self):
        resp = self.client.get(reverse('invoicing:receipt-list'))
        self.assertEqual(resp.status_code, 200)

    def test_get_receipt_form(self):
        resp = self.client.get(reverse('invoicing:create-receipt'))
        self.assertEqual(resp.status_code, 200)

    def test_get_receipt_update(self):
        resp = self.client.get(reverse('invoicing:receipt-update',
            kwargs={
                'pk': self.receipt.pk
            }))
        self.assertEqual(resp.status_code, 200)

    def test_get_receipt_detail(self):
        resp = self.client.get(reverse('invoicing:receipt-detail',
            kwargs={
                'pk': self.receipt.pk
            }))
        self.assertEqual(resp.status_code, 200)
