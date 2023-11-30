# Generated by Django 4.1.1 on 2023-11-30 17:11

from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0010_employee_extra_leaves_employee_total_leaves_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActionLogs',
            fields=[
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('is_deleted', models.BooleanField(default=False)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('config', models.JSONField(blank=True, default=dict)),
                ('action', models.CharField(max_length=255)),
                ('details', models.TextField(blank=True, null=True)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='actions_performed', to='employees.employee')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
