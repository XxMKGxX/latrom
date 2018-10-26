# Generated by Django 2.1.1 on 2018-10-26 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0002_payrollofficer'),
    ]

    operations = [
        migrations.AddField(
            model_name='payrollofficer',
            name='can_create_payroll_elements',
            field=models.BooleanField(blank=True, default=False),
        ),
        migrations.AddField(
            model_name='payrollofficer',
            name='can_log_timesheets',
            field=models.BooleanField(blank=True, default=False),
        ),
        migrations.AddField(
            model_name='payrollofficer',
            name='can_register_new_employees',
            field=models.BooleanField(blank=True, default=False),
        ),
        migrations.AddField(
            model_name='payrollofficer',
            name='can_run_payroll',
            field=models.BooleanField(blank=True, default=False),
        ),
        migrations.AlterField(
            model_name='employeetimesheet',
            name='complete',
            field=models.BooleanField(blank=True, default=False),
        ),
    ]
