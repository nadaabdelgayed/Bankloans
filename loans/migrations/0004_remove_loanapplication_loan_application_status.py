# Generated by Django 4.2.4 on 2023-08-07 00:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('loans', '0003_remove_loan_loan_is_approved_loanapplication_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='loanapplication',
            name='loan_application_status',
        ),
    ]