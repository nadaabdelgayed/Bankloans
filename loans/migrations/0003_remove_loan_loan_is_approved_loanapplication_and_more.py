# Generated by Django 4.2.4 on 2023-08-05 23:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('loans', '0002_rename_funds_fund'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='loan',
            name='loan_is_approved',
        ),
        migrations.CreateModel(
            name='LoanApplication',
            fields=[
                ('loan_application_id', models.AutoField(primary_key=True, serialize=False)),
                ('loan_application_created', models.DateTimeField(auto_now_add=True)),
                ('loan_application_updated', models.DateTimeField(auto_now=True)),
                ('loan_application_status', models.CharField(max_length=50)),
                ('loan_application_is_approved', models.BooleanField(default=False)),
                ('loan_ammount', models.IntegerField()),
                ('loan_tenure', models.IntegerField()),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='loans.user')),
            ],
        ),
        migrations.AddField(
            model_name='loan',
            name='loan_application_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='loans.loanapplication'),
        ),
    ]
