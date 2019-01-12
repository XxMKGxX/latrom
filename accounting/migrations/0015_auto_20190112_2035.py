# Generated by Django 2.1.4 on 2019-01-12 18:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0014_auto_20190111_1504'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('credit', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounting.Credit')),
                ('debit', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounting.Debit')),
            ],
        ),
        migrations.RenameField(
            model_name='journalentry',
            old_name='posted_to_general_ledger',
            new_name='posted_to_ledger',
        ),
        migrations.RemoveField(
            model_name='journalentry',
            name='reference',
        ),
        migrations.AddField(
            model_name='post',
            name='entry',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounting.JournalEntry'),
        ),
        migrations.AddField(
            model_name='post',
            name='ledger',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounting.Ledger'),
        ),
    ]
