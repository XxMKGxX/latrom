# Generated by Django 2.1.4 on 2019-03-24 12:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manufacturing', '0017_auto_20190324_1417'),
        ('invoicing', '0017_auto_20190324_1417'),
        ('services', '0016_auto_20190324_1417'),
        ('inventory', '0030_auto_20190324_1303'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='consumable',
            name='category',
        ),
        migrations.RemoveField(
            model_name='consumable',
            name='supplier',
        ),
        migrations.RemoveField(
            model_name='consumable',
            name='unit',
        ),
        migrations.RemoveField(
            model_name='equipment',
            name='asset_data',
        ),
        migrations.RemoveField(
            model_name='equipment',
            name='category',
        ),
        migrations.RemoveField(
            model_name='equipment',
            name='supplier',
        ),
        migrations.RemoveField(
            model_name='equipment',
            name='unit',
        ),
        migrations.RemoveField(
            model_name='product',
            name='category',
        ),
        migrations.RemoveField(
            model_name='product',
            name='supplier',
        ),
        migrations.RemoveField(
            model_name='product',
            name='unit',
        ),
        migrations.RemoveField(
            model_name='rawmaterial',
            name='category',
        ),
        migrations.RemoveField(
            model_name='rawmaterial',
            name='supplier',
        ),
        migrations.RemoveField(
            model_name='rawmaterial',
            name='unit',
        ),
        migrations.DeleteModel(
            name='Consumable',
        ),
        migrations.DeleteModel(
            name='Equipment',
        ),
        migrations.DeleteModel(
            name='Product',
        ),
        migrations.DeleteModel(
            name='RawMaterial',
        ),
    ]
