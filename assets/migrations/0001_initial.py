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
            name='Asset',
            fields=[
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('id', models.CharField(default=uuid.UUID('4bff99ad-0a7d-478d-b738-200bc28226e9'), max_length=50, primary_key=True, serialize=False)),
                ('asset_name', models.CharField(max_length=50)),
                ('asset_model', models.CharField(max_length=50)),
                ('asset_type', models.CharField(max_length=50)),
                ('asset_description', models.CharField(max_length=250)),
                ('is_deleted', models.BooleanField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AssignedAsset',
            fields=[
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('id', models.CharField(default=uuid.UUID('4bff99ad-0a7d-478d-b738-200bc28226e9'), max_length=50, primary_key=True, serialize=False)),
                ('asset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assets.asset')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assigned_asset', to='employees.employee')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
