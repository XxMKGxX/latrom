# Generated by Django 2.1.1 on 2018-11-02 06:20

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0003_auto_20181101_1514'),
    ]

    operations = [
        migrations.AddField(
            model_name='accountingsettings',
            name='default_bookkeeper',
            field=models.ForeignKey(blank=True, null=True, on_delete=None, to='accounting.Bookkeeper'),
        ),
        migrations.AddField(
            model_name='interestbearingaccount',
            name='date_account_opened',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AddField(
            model_name='interestbearingaccount',
            name='last_interest_earned_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='expense',
            name='customer',
            field=models.ForeignKey(blank=True, null=True, on_delete=None, to='invoicing.Customer'),
        ),
        migrations.AlterField(
            model_name='interestbearingaccount',
            name='interest_method',
            field=models.IntegerField(choices=[(0, 'Simple')], default=0),
        ),
        migrations.AlterField(
            model_name='recurringexpense',
            name='last_created_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='recurringexpense',
            name='start_date',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
