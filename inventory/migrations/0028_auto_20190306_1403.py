# Generated by Django 2.1.4 on 2019-03-06 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0027_auto_20190306_1339'),
    ]

    operations = [
        migrations.RenameField(
            model_name='inventorysettings',
            old_name='product_sales_pricing_method',
            new_name='default_product_sales_pricing_method',
        ),
        migrations.RemoveField(
            model_name='inventorysettings',
            name='order_template_theme',
        ),
        migrations.AlterField(
            model_name='inventorysettings',
            name='inventory_valuation_method',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Averaging')], default=1),
        ),
    ]
