# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-07-05 10:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0017_auto_20180704_2229'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='image',
            field=models.FileField(blank=True, null=True, upload_to=b'F:\\Documents\\code\\git\\latrom\\media'),
        ),
    ]
