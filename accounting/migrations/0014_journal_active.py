# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-07-05 13:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0013_tax_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='journal',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
