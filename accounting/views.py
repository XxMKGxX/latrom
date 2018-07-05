# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import json
import urllib
import datetime
import decimal

from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView,  FormView
from django.http import HttpResponseRedirect
from django_filters.views import FilterView
from django.urls import reverse_lazy
from rest_framework import viewsets

import serializers
import models 
import filters
import forms
from inventory.models import Item
from common_data.utilities import ExtraContext, load_config, apply_style

#constants
CREATE_TEMPLATE = os.path.join('common_data', 'create_template.html')

class Dashboard(TemplateView):
    template_name = os.path.join('accounting', 'dashboard.html')

#############################################################
#                 JournalEntry Views                         #
#############################################################

# update and delete removed for security, only adjustments can alter the state 
# of an entry 

class JournalEntryCreateView(ExtraContext, CreateView):
    '''This type of journal entry has only one credit and one debit'''
    template_name = CREATE_TEMPLATE
    model = models.JournalEntry
    form_class = forms.SimpleJournalEntryForm
    success_url = reverse_lazy('accounting:dashboard')
    extra_context = {"title": "Create New Journal Entry"}

class ComplexEntryView(ExtraContext, CreateView):
    '''This type of journal entry can have any number of 
    credits and debits. The front end page uses react to dynamically 
    alter the content of page hence the provided data from react is 
    sent to the server as urlencoded json in a hidden field called items[]
    
    '''
    template_name = os.path.join('accounting', 'compound_transaction.html')
    form_class= forms.ComplexEntryForm

    def post(self, request, *args, **kwargs):
        j = models.JournalEntry.objects.create(
                reference = request.POST['reference'],
                memo = request.POST['memo'],
                date = request.POST['date'],
                journal = models.Journal.objects.get(
                    pk=request.POST['journal']),
            )
        for item in request.POST.getlist('items[]'):
            item_data = json.loads(urllib.unquote(item))
            amount = decimal.Decimal(item_data['amount'])
            if item_data['debit'] == '1':
                models.Debit.objects.create(
                    entry = j,
                    account = models.Account.objects.get(
                    pk=int(item_data['account'])),
                    amount = amount
                ) 
            else:
                models.Credit.objects.create(
                    entry = j,
                    account = models.Account.objects.get(
                    pk=int(item_data['account'])),
                    amount = amount
                )

        return HttpResponseRedirect(reverse_lazy('accounting:dashboard'))

class JournalEntryDetailView(DetailView):
    template_name = os.path.join('accounting', 'transaction_detail.html')
    model = models.JournalEntry

#############################################################
#                 Employee  Views                            #
#############################################################

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = models.Employee.objects.all()
    serializer_class = serializers.EmployeeSerializer

class EmployeeCreateView(ExtraContext, CreateView):
    template_name = os.path.join('common_data', 'crispy_create_template.html')
    success_url = reverse_lazy('accounting:dashboard')
    form_class = forms.EmployeeForm
    extra_context = {
        'title': 'Add Employee to payroll system'
    }

class EmployeeUpdateView(ExtraContext, UpdateView):
    template_name = os.path.join('common_data', 'crispy_create_template.html')
    success_url = reverse_lazy('accounting:dashboard')
    form_class = forms.EmployeeForm
    model = models.Employee
    extra_context = {
        'title': 'Edit Employee data on payroll system'
    }

class EmployeeListView(ExtraContext, FilterView):
    template_name = os.path.join('accounting', 'employee_list.html')
    filterset_class = filters.EmployeeFilter
    extra_context = {
        'title': 'List of Employees',
        'new_link': reverse_lazy('accounting:create-employee')
    }
    def get_queryset(self):
        return models.Employee.objects.filter(active=True).order_by('first_name')

class EmployeeDetailView(DetailView):
    template_name = os.path.join('accounting', 'employee_detail.html')
    model = models.Employee

class EmployeeDeleteView(DeleteView):
    template_name = os.path.join('common_data', 'delete_template.html')
    success_url = reverse_lazy('accounting:list-employees')
    model = models.Employee


#############################################################
#                 Account  Views                            #
#############################################################
class AccountViewSet(viewsets.ModelViewSet):
    queryset = models.Account.objects.all()
    serializer_class = serializers.AccountSerializer


class AccountTransferPage(ExtraContext, CreateView):
    template_name = CREATE_TEMPLATE
    success_url = reverse_lazy('accounting:dashboard')
    form_class = forms.SimpleJournalEntryForm
    extra_context = {
        'title': 'Transfer between Accounts'
    }

class AccountCreateView(ExtraContext, CreateView):
    template_name = CREATE_TEMPLATE
    model = models.Account
    form_class = forms.AccountForm
    success_url = reverse_lazy('accounting:dashboard')
    extra_context = {"title": "Create New Account"}

class AccountUpdateView(ExtraContext, UpdateView):
    template_name = CREATE_TEMPLATE
    model = models.Account
    form_class = forms.AccountForm
    success_url = reverse_lazy('accounting:dashboard')
    extra_context = {"title": "Update Existing Account"}


class AccountDetailView(DetailView):
    template_name = os.path.join('accounting', 'account_detail.html')
    model = models.Account 
    

class AccountListView(ExtraContext, FilterView):
    template_name = os.path.join('accounting', 'account_list.html')
    filterset_class = filters.AccountFilter
    paginate_by = 10
    extra_context = {
        "title": "Chart of Accounts",
        'new_link': reverse_lazy('accounting:create-account')
                }
    def get_queryset(self):
        return models.Account.objects.filter(active=True).order_by('pk')
#############################################################
#                        Misc Views                         #
#############################################################

class TaxViewset(viewsets.ModelViewSet):
    queryset = models.Tax.objects.all()
    serializer_class = serializers.TaxSerializer

class TaxUpdateView(ExtraContext, UpdateView):
    form_class = forms.TaxForm
    model= models.Tax
    template_name = os.path.join('common_data','create_template.html')
    success_url = reverse_lazy('accounting:dashboard')
    extra_context = {
        'title': 'Editing Existing Tax'
    }

class TaxCreateView(ExtraContext, CreateView):
    form_class = forms.TaxForm
    template_name = os.path.join('common_data','create_template.html')
    success_url = reverse_lazy('accounting:util-list')
    extra_context = {
        'title': 'Add Taxes For Invoices'
    }

class TaxDeleteView(DeleteView):
    template_name = os.path.join('common_data', 'delete_template.html')
    success_url = reverse_lazy('accounting:util-list')
    model = models.Tax

class DeductionCreateView(ExtraContext, CreateView):
    form_class = forms.DeductionForm
    template_name = os.path.join('common_data','create_template.html')
    success_url = reverse_lazy('accounting:dashboard')
    extra_context = {
        'title': 'Add Deductions For Payroll'
    }

class DeductionUpdateView(ExtraContext, UpdateView):
    form_class = forms.DeductionForm
    model = models.Deduction
    template_name = os.path.join('common_data','create_template.html')
    success_url = reverse_lazy('accounting:util-list')
    extra_context = {
        'title': 'Update existing deduction'
    }

class DeductionDeleteView(DeleteView):
    template_name = os.path.join('common_data', 'delete_template.html')
    success_url = reverse_lazy('accounting:util-list')
    model = models.Deduction

class UtilsListView(TemplateView):
    template_name = os.path.join('accounting', 'utils_list.html')

    def get_context_data(self, *args, **kwargs):
        context = super(UtilsListView, self).get_context_data(*args, **kwargs)
        context['allowances'] = models.Allowance.objects.filter(active=True).order_by('name')
        context['deductions'] = models.Deduction.objects.filter(active=True).order_by('name')
        context['commissions'] = models.CommissionRule.objects.filter(active=True).order_by('name')
        context['taxes'] = models.Tax.objects.all().order_by('name')
        return context


class AllowanceCreateView(ExtraContext, CreateView):
    form_class = forms.AllowanceForm
    template_name = os.path.join('common_data','create_template.html')
    success_url = reverse_lazy('accounting:dashboard')
    extra_context = {
        'title': 'Create New Allowance '
    }

class AllowanceUpdateView(ExtraContext, UpdateView):
    form_class = forms.AllowanceForm
    model = models.Allowance
    template_name = os.path.join('common_data','create_template.html')
    success_url = reverse_lazy('accounting:util-list')
    extra_context = {
        'title': 'Edit Existing Allowance '
    }

class AllowanceDeleteView(DeleteView):
    template_name = os.path.join('common_data', 'delete_template.html')
    success_url = reverse_lazy('accounting:util-list')
    model = models.Allowance

class CommissionCreateView(ExtraContext, CreateView):
    form_class = forms.CommissionForm
    template_name = os.path.join('common_data','create_template.html')
    success_url = reverse_lazy('accounting:dashboard')
    extra_context = {
        'title': 'Add Commission Rule for pay grades'
    }

class CommissionUpdateView(ExtraContext, UpdateView):
    form_class = forms.CommissionForm
    model = models.CommissionRule
    template_name = os.path.join('common_data','create_template.html')
    success_url = reverse_lazy('accounting:util-list')
    extra_context = {
        'title': 'Edit Existing Commission Rule'
    }

class CommissionDeleteView(DeleteView):
    template_name = os.path.join('common_data', 'delete_template.html')
    success_url = reverse_lazy('accounting:util-list')
    model = models.CommissionRule

class DirectPaymentFormView(ExtraContext, FormView):
    '''Uses a simple form view as a wrapper for a transaction in the journals
    for transactions involving two accounts.
    '''
    form_class = forms.DirectPaymentForm
    template_name = CREATE_TEMPLATE
    success_url = reverse_lazy('accounting:dashboard')
    extra_context = {'title': 'Create Direct Payment'}
    def post(self, request):
        
        form = self.form_class(request.POST)
        if form.is_valid():
            notes_string = """
                This payment was made out to: %s.
                the payment method used: %s \n """ % \
                (form.cleaned_data['paid_to'],
                    form.cleaned_data['method'])
            journal = models.Journal.objects.get(
                pk=4)#purchases journal
            j = models.JournalEntry.objects.create(
                reference = 'DPMT:' + form.cleaned_data['reference'],
                memo=notes_string + form.cleaned_data['notes'],
                date=form.cleaned_data['date'],
                journal = journal
            )
            j.simple_entry(
                form.cleaned_data['amount'],
                models.Account.objects.get(pk=4006),#purchases account
                form.cleaned_data['account_paid_to'],
            )
        return super(DirectPaymentFormView, self).post(request)

class AccountConfigView(FormView):
    '''
    Tabbed Configuration view for accounts 
    '''
    form_class = forms.ConfigForm
    template_name = os.path.join('accounting', 'config.html')
    success_url = reverse_lazy('accounting:dashboard')
    
    def get_initial(self):
        return load_config()

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            config = load_config()
            new_config = dict(config)
            new_config.update(request.POST.dict())
            json.dump(new_config, open('config.json', 'w'))

        return super(AccountConfigView, self).post(request)

###################################################
#                 Pay Grade Views                 #
###################################################

class PayGradeCreateView(ExtraContext, CreateView):
    form_class = forms.PayGradeForm
    template_name =CREATE_TEMPLATE
    success_url = reverse_lazy('accounting:dashboard')
    extra_context = {
        'title': 'Add pay grades for payroll'
    }

class PayGradeUpdateView(ExtraContext, UpdateView):
    form_class = forms.PayGradeForm
    template_name =CREATE_TEMPLATE
    success_url = reverse_lazy('accounting:dashboard')
    extra_context = {
        'title': 'Edit existing Pay Grade'
    }

class PayGradeListView(ListView):
    template_name = os.path.join('accounting', 'pay_grade_list.html')
    paginate_by = 10
    extra_context = {
        'title': 'List of Payslips'
    }

class PayGradeDeleteView(DeleteView):
    template_name = os.path.join('common_data', 'delete_template')
    success_url = reverse_lazy('accounting:list-pay-grades')
    model = models.PayGrade

class NonInvoicedCashSale(FormView):
    '''
    A transaction handled entirely in the accounting part of the application
    No invoice is generated but the relevant accounts are transacted on and 
    the appropriate inventory is updated.
    React is used to provide a table of items that can be added to the cash
    sale. It communicates with the server in the form of json submitted as 
    part of a number of hidden fields called 'items[]'.
    '''
    form_class = forms.NonInvoicedSaleForm
    template_name = os.path.join('accounting', 'non_invoiced_cash_sale.html')
    success_url = reverse_lazy('accounting:dashboard')

    def post(self, request, *args, **kwargs):
        resp = super(NonInvoicedCashSale, self).post(request, *args, **kwargs)
        total = 0
        config = load_config()
        for item in request.POST.getlist('items[]'):
            data = json.loads(urllib.unquote(item))
            quantity = float(data['quantity'])
            item = Item.objects.get(pk=data['code'])
            #update inventory
            item.decrement(quantity)
            amount_sold = item.unit_sales_price * quantity 
            discount = amount_sold * (float(data['discount']) / 100)
            total += amount_sold - discount
            #fix
            date = datetime.datetime.strptime(
                request.POST['date'], '%m/%d/%Y').strftime('%Y-%m-%d')
        
        #add taxes here from the config


        j = models.JournalEntry.objects.create(
                date=date,
                memo = request.POST['comments'],
                reference = "Journal Entry derived from non invoiced cash sale",
                journal = load   
            )
        j.simple_entry(
            total,
            models.Account.objects.get(pk=4000),#sales
            models.Account.objects.get(pk=1004),#inventory
        )
        return resp

class DirectPaymentList(ExtraContext, TemplateView):
    template_name = os.path.join('accounting', 'direct_payment_list.html')
    extra_context = {
        'entries': lambda : models.JournalEntry.objects.filter(
           journal = models.Journal.objects.get(pk=4)) 
    }

#############################################################
#                     Payslip Views                         #
#############################################################

class PayslipView( DetailView):
    template_name = os.path.join('accounting', 'payslip.html')
    model= models.Payslip

    def get_context_data(self, *args, **kwargs):
        context = super(PayslipView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Pay Slip'
        context.update(load_config())
        return context

class PayslipListView(ExtraContext, FilterView):
    filterset_class = filters.PayslipFilter
    template_name = os.path.join('accounting', 'payslip_list.html')
    paginate_by = 10
    extra_context = {
        'title': 'List of Payslips'
    }

    def get_queryset(self):
        return models.Payslip.objects.all().order_by('start_period')
        

class PayslipViewset(viewsets.ModelViewSet):
    queryset = models.Payslip.objects.all()
    serializer_class = serializers.PayslipSerializer

#############################################################
#                    Journal Views                         #
#############################################################

class JournalCreateView(ExtraContext, CreateView):
    template_name = CREATE_TEMPLATE
    model = models.Journal
    form_class = forms.JournalForm
    success_url = reverse_lazy('accounting:dashboard')
    extra_context = {"title": "Create New Journal"}

class JournalDetailView(DetailView):
    template_name = os.path.join('accounting', 'journal_detail.html')
    model = models.Journal

class JournalListView(ExtraContext, FilterView):
    template_name = os.path.join('accounting', 'journal_list.html')
    filterset_class = filters.JournalFilter
    paginate_by = 10
    extra_context = {
        "title": "Accounting Journals",
        'new_link': reverse_lazy('accounting:create-journal')
                }

    def get_queryset(self):
        return models.Journal.objects.all().order_by('name')


#############################################################
#                    PayGrade Views                         #
#############################################################

class PayGradeUpdateView(ExtraContext, UpdateView):
    form_class = forms.PayGradeForm
    template_name =CREATE_TEMPLATE
    model = models.PayGrade
    success_url = reverse_lazy('accounting:dashboard')
    extra_context = {
        'title': 'Update existing pay grade'
    }


class PayGradeListView(ExtraContext, FilterView):
    template_name = os.path.join('accounting', 'pay_grade_list.html')
    extra_context = {
        'title': 'List of Pay Grades'
    }
    model = models.PayGrade

class PayrollConfigView(ExtraContext, TemplateView):
    template_name = os.path.join('accounting', 'payroll_config.html')
    extra_context = {
        'employees': models.Employee.objects.all()
    }