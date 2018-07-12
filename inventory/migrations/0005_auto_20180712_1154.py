# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-07-12 09:54
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0004_auto_20180711_1815'),
    ]

    operations = [
        migrations.CreateModel(
            name='WareHouse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('address', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='WareHouseItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.FloatField()),
            ],
        ),
        migrations.RemoveField(
            model_name='item',
            name='quantity',
        ),
        migrations.AlterField(
            model_name='order',
            name='ship_to',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.WareHouse'),
        ),
        migrations.AddField(
            model_name='warehouseitem',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.Item'),
        ),
    ]
