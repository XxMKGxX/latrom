# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-07-21 03:09
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('balance', models.DecimalField(decimal_places=2, max_digits=9)),
                ('type', models.CharField(choices=[('expense', 'Expense'), ('asset', 'Asset'), ('liability', 'Liability'), ('equity', 'Equity'), ('income', 'Income'), ('cost-of-sales', 'Cost of Sales')], max_length=32)),
                ('description', models.TextField()),
                ('balance_sheet_category', models.CharField(choices=[('current-assets', 'Current Assets'), ('long-term-assets', 'Long Term Assets'), ('current-liabilites', 'Current Liabilites'), ('long-term-liabilites', 'Long Term Liabilites'), ('expense', 'Expense'), ('current-assets', 'Current Assets'), ('not-included', 'Not Included')], default='current-assets', max_length=16)),
                ('active', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AccountingSettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_of_financial_year', models.DateField()),
                ('use_default_chart_of_accounts', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Adjustmet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Asset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('description', models.TextField(blank=True)),
                ('category', models.IntegerField(choices=[(0, 'Land'), (1, 'Buildings'), (2, 'Vehicles'), (3, 'LeaseHold Improvements'), (4, 'Furniture and Fixtures'), (5, 'Equipment')])),
                ('initial_value', models.DecimalField(decimal_places=2, max_digits=9)),
                ('depreciation_period', models.IntegerField()),
                ('init_date', models.DateField()),
                ('depreciation_method', models.IntegerField(choices=[(0, 'Straight Line'), (1, 'Sum of years digits'), (2, 'Double Declining balance')])),
                ('salvage_value', models.DecimalField(decimal_places=2, max_digits=9)),
            ],
        ),
        migrations.CreateModel(
            name='Bookkeeper',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Credit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=9)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Debit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=9)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('category', models.IntegerField(choices=[(0, 'Advertising'), (1, 'Bank Service Charges'), (2, 'Equipment Rental'), (3, 'Dues and Subscriptions'), (4, 'Telephone'), (5, 'Vehicles'), (6, 'Travel and Expenses'), (7, 'Suppliers'), (8, 'Rent'), (9, 'Payroll Expenses'), (10, 'Insurance'), (11, 'Office Expenses'), (12, 'Postage'), (13, 'Other')])),
                ('amount', models.DecimalField(decimal_places=2, max_digits=9)),
                ('date', models.DateField()),
                ('billable', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='InterestBearingAccount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('balance', models.DecimalField(decimal_places=2, max_digits=9)),
                ('type', models.CharField(choices=[('expense', 'Expense'), ('asset', 'Asset'), ('liability', 'Liability'), ('equity', 'Equity'), ('income', 'Income'), ('cost-of-sales', 'Cost of Sales')], max_length=32)),
                ('description', models.TextField()),
                ('balance_sheet_category', models.CharField(choices=[('current-assets', 'Current Assets'), ('long-term-assets', 'Long Term Assets'), ('current-liabilites', 'Current Liabilites'), ('long-term-liabilites', 'Long Term Liabilites'), ('expense', 'Expense'), ('current-assets', 'Current Assets'), ('not-included', 'Not Included')], default='current-assets', max_length=16)),
                ('active', models.BooleanField(default=True)),
                ('interest_rate', models.DecimalField(decimal_places=2, default=0.0, max_digits=6)),
                ('interest_interval', models.IntegerField(choices=[(0, 'monthly'), (1, 'annually')], default=1)),
                ('interest_method', models.IntegerField(choices=[(0, 'Simple'), (1, 'Commpound')], default=0)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Journal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('description', models.TextField(default='')),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='JournalEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reference', models.CharField(default='', max_length=128)),
                ('date', models.DateField(default=datetime.date.today)),
                ('memo', models.TextField()),
                ('posted_to_general_ledger', models.BooleanField(default=False)),
                ('adjusted', models.BooleanField(default=False)),
                ('journal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounting.Journal')),
            ],
        ),
        migrations.CreateModel(
            name='Ledger',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='RecurringExpense',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('category', models.IntegerField(choices=[(0, 'Advertising'), (1, 'Bank Service Charges'), (2, 'Equipment Rental'), (3, 'Dues and Subscriptions'), (4, 'Telephone'), (5, 'Vehicles'), (6, 'Travel and Expenses'), (7, 'Suppliers'), (8, 'Rent'), (9, 'Payroll Expenses'), (10, 'Insurance'), (11, 'Office Expenses'), (12, 'Postage'), (13, 'Other')])),
                ('amount', models.DecimalField(decimal_places=2, max_digits=9)),
                ('cycle', models.IntegerField(choices=[(1, 'Daily'), (7, 'Weekly'), (14, 'Bi- Monthly'), (30, 'Monthly'), (90, 'Quarterly'), (182, 'Bi-Annually'), (365, 'Annually')], default=30)),
                ('expiration_date', models.DateField(null=True)),
                ('start_date', models.DateField(null=True)),
                ('last_created_date', models.DateField(null=True)),
                ('debit_account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounting.Account')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Tax',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('rate', models.FloatField()),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='WorkBook',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
            ],
        ),
    ]
