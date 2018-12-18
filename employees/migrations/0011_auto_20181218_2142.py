# Generated by Django 2.1.1 on 2018-12-18 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0008_accountingsettings_currency_exchange_table'),
        ('employees', '0010_auto_20181218_1508'),
    ]

    operations = [
        migrations.AddField(
            model_name='deduction',
            name='account_paid_into',
            field=models.ForeignKey(default=5008, on_delete=None, to='accounting.Account'),
        ),
        migrations.AddField(
            model_name='employeessettings',
            name='payroll_account',
            field=models.ForeignKey(default=1000, on_delete=None, to='accounting.Account'),
        ),
        migrations.AddField(
            model_name='payslip',
            name='entry',
            field=models.ForeignKey(blank=True, null=True, on_delete=None, to='accounting.JournalEntry'),
        ),
        migrations.AddField(
            model_name='payslip',
            name='status',
            field=models.CharField(choices=[('draft', 'Draft'), ('verified', 'Verified'), ('paid', 'Paid')], default='draft', max_length=16),
        ),
        migrations.AlterField(
            model_name='employeessettings',
            name='payroll_date_four',
            field=models.PositiveSmallIntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14), (15, 15), (16, 16), (17, 17), (18, 18), (19, 19), (20, 20), (21, 21), (22, 22), (23, 23), (24, 24), (25, 25), (26, 26), (27, 27), (28, 28)]),
        ),
        migrations.AlterField(
            model_name='employeessettings',
            name='payroll_date_one',
            field=models.PositiveSmallIntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14), (15, 15), (16, 16), (17, 17), (18, 18), (19, 19), (20, 20), (21, 21), (22, 22), (23, 23), (24, 24), (25, 25), (26, 26), (27, 27), (28, 28)]),
        ),
        migrations.AlterField(
            model_name='employeessettings',
            name='payroll_date_three',
            field=models.PositiveSmallIntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14), (15, 15), (16, 16), (17, 17), (18, 18), (19, 19), (20, 20), (21, 21), (22, 22), (23, 23), (24, 24), (25, 25), (26, 26), (27, 27), (28, 28)]),
        ),
        migrations.AlterField(
            model_name='employeessettings',
            name='payroll_date_two',
            field=models.PositiveSmallIntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14), (15, 15), (16, 16), (17, 17), (18, 18), (19, 19), (20, 20), (21, 21), (22, 22), (23, 23), (24, 24), (25, 25), (26, 26), (27, 27), (28, 28)]),
        ),
        migrations.AlterField(
            model_name='employeessettings',
            name='payroll_officer',
            field=models.ForeignKey(blank=True, limit_choices_to={'payroll_officer__isnull': False}, null=True, on_delete=None, related_name='payroll_officer', to='employees.Employee'),
        ),
        migrations.AlterField(
            model_name='leave',
            name='authorized_by',
            field=models.ForeignKey(limit_choices_to={'payroll_officer__isnull': False}, null=True, on_delete=None, related_name='authority', to='employees.Employee'),
        ),
    ]
