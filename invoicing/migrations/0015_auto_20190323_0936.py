# Generated by Django 2.1.4 on 2019-03-23 07:36

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0015_auto_20190206_2117'),
        ('inventory', '0028_auto_20190306_1403'),
        ('accounting', '0022_remove_accountingsettings_use_default_chart_of_accounts'),
        ('invoicing', '0014_auto_20190304_1222'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExpenseLineComponent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expense', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounting.Expense')),
            ],
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True)),
                ('status', models.CharField(choices=[('quotation', 'Quotation'), ('draft', 'Draft'), ('proforma', 'Proforma Invoice'), ('invoice', 'Invoice'), ('paid', 'Paid In Full'), ('paid-partially', 'Paid Partially'), ('reversed', 'Reversed')], max_length=16)),
                ('invoice_number', models.PositiveIntegerField(null=True)),
                ('quotation_number', models.PositiveIntegerField(null=True)),
                ('due', models.DateField(default=datetime.date.today)),
                ('date', models.DateField(default=datetime.date.today)),
                ('discount', models.DecimalField(decimal_places=2, default=0.0, max_digits=6)),
                ('terms', models.CharField(blank=True, max_length=128)),
                ('comments', models.TextField(blank=True)),
                ('purchase_order_number', models.CharField(blank=True, max_length=32)),
                ('customer', models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.SET_NULL, to='invoicing.Customer')),
                ('entry', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounting.JournalEntry')),
                ('salesperson', models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.SET_NULL, to='invoicing.SalesRepresentative')),
                ('ship_from', models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventory.WareHouse')),
                ('shipping_expenses', models.ManyToManyField(to='accounting.Expense')),
                ('tax', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounting.Tax')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='InvoiceLine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('line_type', models.PositiveSmallIntegerField(choices=[(1, 'product'), (2, 'service'), (3, 'expense')])),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('expense', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='invoicing.ExpenseLineComponent')),
                ('invoice', models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.SET_NULL, to='invoicing.Invoice')),
            ],
        ),
        migrations.CreateModel(
            name='ProductLineComponent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('returned', models.BooleanField(default=False)),
                ('value', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('quantity', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
            ],
        ),
        migrations.CreateModel(
            name='ServiceLineComponent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hours', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('service', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='services.Service')),
            ],
        ),
        migrations.AddField(
            model_name='invoiceline',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='invoicing.ProductLineComponent'),
        ),
        migrations.AddField(
            model_name='invoiceline',
            name='service',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='invoicing.ServiceLineComponent'),
        ),
    ]
