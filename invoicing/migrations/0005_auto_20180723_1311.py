# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-07-23 11:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoicing', '0004_auto_20180723_1216'),
    ]

    operations = [
        migrations.AlterField(
            model_name='abstractsale',
            name='status',
            field=models.CharField(choices=[('quotation', 'Quotation'), ('draft', 'Draft'), ('sent', 'Sent'), ('paid', 'Paid In Full'), ('paid-partially', 'Paid Partially'), ('reversed', 'Reversed')], max_length=16),
        ),
    ]
