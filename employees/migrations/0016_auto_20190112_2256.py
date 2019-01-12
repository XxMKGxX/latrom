# Generated by Django 2.1.4 on 2019-01-12 20:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0015_auto_20190104_2114'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deduction',
            name='account_paid_into',
            field=models.ForeignKey(default=5008, on_delete=django.db.models.deletion.SET_DEFAULT, to='accounting.Account'),
        ),
        migrations.AlterField(
            model_name='employeessettings',
            name='payroll_account',
            field=models.ForeignKey(default=1000, on_delete=django.db.models.deletion.SET_DEFAULT, to='accounting.Account'),
        ),
    ]
