# Generated by Django 2.1.1 on 2018-12-14 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0010_merge_20181213_1816'),
    ]

    operations = [
        migrations.AlterField(
            model_name='consumable',
            name='image',
            field=models.FileField(blank=True, null=True, upload_to='C:\\Users\\nakamura9a\\Documents\\code\\git\\latrom\\media'),
        ),
        migrations.AlterField(
            model_name='equipment',
            name='image',
            field=models.FileField(blank=True, null=True, upload_to='C:\\Users\\nakamura9a\\Documents\\code\\git\\latrom\\media'),
        ),
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.FileField(blank=True, null=True, upload_to='C:\\Users\\nakamura9a\\Documents\\code\\git\\latrom\\media'),
        ),
        migrations.AlterField(
            model_name='rawmaterial',
            name='image',
            field=models.FileField(blank=True, null=True, upload_to='C:\\Users\\nakamura9a\\Documents\\code\\git\\latrom\\media'),
        ),
    ]
