# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-06-22 03:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoicing', '0002_auto_20180621_1958'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='comments',
            field=models.TextField(blank=True),
        ),
    ]