# Generated by Django 4.1.1 on 2022-09-27 19:11

from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('employees', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payroll',
            fields=[
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('id', models.CharField(default=uuid.UUID('4bff99ad-0a7d-478d-b738-200bc28226e9'), max_length=50, primary_key=True, serialize=False)),
                ('basic_salary', models.FloatField()),
                ('bonus', models.FloatField()),
                ('reimbursement', models.FloatField()),
                ('travel_allowance', models.FloatField()),
                ('tax_deduction', models.FloatField()),
                ('month', models.CharField(max_length=20)),
                ('year', models.CharField(max_length=50)),
                ('released', models.BooleanField()),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payroll', to='employees.employee')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
