
from crispy_forms.bootstrap import Tab, TabHolder
from crispy_forms.helper import FormHelper
from crispy_forms.layout import (Fieldset, 
                                Layout, 
                                Submit, 
                                HTML,
                                Row,
                                Column)
from django import forms
from django.contrib.auth.models import User

from common_data.forms import BootstrapMixin
from inventory.models import Supplier, WareHouse

from . import models


class ConfigForm(forms.ModelForm, BootstrapMixin):
    class Meta:
        model = models.AccountingSettings
        fields = "__all__"
        
class AssetForm(forms.ModelForm, BootstrapMixin):
    class Meta:
        fields = "__all__"
        model = models.Asset

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self

class ExpenseForm(forms.ModelForm, BootstrapMixin):
    class Meta:
        exclude = "entry", 
        model = models.Expense

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            TabHolder(
                Tab('basic',
                    Row(
                        Column('customer', css_class='form-group col-6'),
                        Column('date', css_class='form-group col-6'),
                    ),
                    Row(
                        Column('amount', css_class='form-group col-6'),
                        Column('debit_account', css_class='form-group col-6'),                        
                    ),
                    'category',
                    'recorded_by',
                    'cycle',
                ),
                Tab('description',
                    'description',
                    'reference',
                ),
            )
        )
        self.helper.add_input(Submit('submit', 'Submit'))
class RecurringExpenseForm(forms.ModelForm, BootstrapMixin):
    class Meta:
        exclude = "last_created_date", 'entry'
        model = models.RecurringExpense

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            TabHolder(
                Tab('basic',
                    Row(
                        Column('start_date', css_class='form-group col-6'),
                        Column('expiration_date', css_class='form-group col-6'),
                    ),
                    Row(
                        Column('amount', css_class='form-group col-6'),
                        Column('debit_account', css_class='form-group col-6'),
                    ),
                    'category',
                    'recorded_by',
                    'cycle',
                ),
                Tab('description',
                    'description',
                    'reference',
                ),
            )
        )
        self.helper.add_input(Submit('submit', 'Submit'))

class DirectPaymentForm(BootstrapMixin, forms.Form):
    date = forms.DateField()
    paid_to = forms.ModelChoiceField(Supplier.objects.all())
    account_paid_from = forms.ModelChoiceField(models.Account.objects.all())
    method = forms.ChoiceField(choices=[
        ('cash', 'Cash'),
        ('transfer', 'Transfer'),
        ('ecocash', 'Ecocash')])
    amount = forms.CharField(widget=forms.NumberInput)
    reference = forms.CharField()
    notes = forms.CharField(widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            TabHolder(
                Tab('basic',
                    'date',
                    Row(
                        Column('paid_to', css_class='form-group col-6'),
                        Column('account_paid_from', css_class='form-group col-6'),
                        ),
                    Row(
                        Column('method', css_class='form-group col-6'),
                        Column('amount', css_class='form-group col-6'),                
                        ),
                        'reference',
                ),
                Tab('notes',
                    'notes',
                ),
            )
            
        )
        self.helper.add_input(Submit('submit', 'Submit'))

class TaxForm(forms.ModelForm, BootstrapMixin):
    class Meta:
        fields ='__all__'
        model = models.Tax

class TaxUpdateForm(forms.ModelForm, BootstrapMixin):
    class Meta:
        fields ='name',
        model = models.Tax

class SimpleJournalEntryForm(forms.ModelForm, BootstrapMixin):
    amount = forms.DecimalField()
    credit = forms.ModelChoiceField(models.Account.objects.all())
    debit = forms.ModelChoiceField(models.Account.objects.all())
    class Meta:
        exclude = "draft", "posted_to_ledger", "adjusted"
        model = models.JournalEntry

    def save(self, *args, **kwargs):
        obj = super(SimpleJournalEntryForm, self).save(*args, **kwargs)
        obj.simple_entry(
            self.cleaned_data['amount'],
            self.cleaned_data['credit'],
            self.cleaned_data['debit']
        )
        return obj

class ComplexEntryForm(forms.ModelForm, BootstrapMixin):
    class Meta:
        exclude="posted_to_ledger", "adjusted"
        model = models.JournalEntry

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
            Column('date', 
                    'journal',
                    'created_by',
                    'draft',
                    css_class="col-sm-6"),
            Column('memo', css_class="col-sm-6")
            )
        )
        self.helper.add_input(Submit('submit', 'Submit'))


class AccountForm(forms.ModelForm, BootstrapMixin):
    class Meta:
        exclude="active",
        model = models.Account

class AccountUpdateForm(forms.ModelForm, BootstrapMixin):
    class Meta:
        exclude="active", "balance"
        model = models.Account


class LedgerForm(forms.ModelForm, BootstrapMixin):
    class Meta:
        fields="__all__"
        model = models.Ledger


class JournalForm(forms.ModelForm, BootstrapMixin):
    class Meta:
        exclude="active",
        model = models.Journal

class NonInvoicedSaleForm(BootstrapMixin,forms.Form):
    date = forms.DateField()
    sold_from = forms.ModelChoiceField(WareHouse.objects.all())
    comments = forms.CharField(widget=forms.Textarea)


class BookkeeperForm(forms.ModelForm, BootstrapMixin):
    class Meta:
        exclude = "active",
        model = models.Bookkeeper


class ExchangeTableForm(forms.ModelForm):
    class Meta:
        fields = 'reference_currency', 'name',
        model = models.CurrencyConversionTable