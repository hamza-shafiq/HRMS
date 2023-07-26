# Generated by Django 4.1.1 on 2022-10-05 13:27

from django.db import migrations, models
import django_extensions.db.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('is_deleted', models.BooleanField(default=False)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('config', models.JSONField(blank=True, default=dict)),
                ('check_in', models.DateTimeField(blank=True, null=True)),
                ('check_out', models.DateTimeField(blank=True, null=True)),
                ('status', models.CharField(choices=[('LATE_ARRIVAL', 'LATE_ARRIVAL'), ('EARLY_ARRIVAL', 'EARLY_ARRIVAL'), ('EARLY_DEPARTURE', 'EARLY_DEPARTURE'), ('LATE_DEPARTURE', 'LATE_DEPARTURE'), ('ON_TIME', 'ON_TIME')], max_length=50)),
            ],
            options={
                'db_table': 'attendances',
            },
        ),
        migrations.CreateModel(
            name='Leaves',
            fields=[
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('is_deleted', models.BooleanField(default=False)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('config', models.JSONField(blank=True, default=dict)),
                ('leave_type', models.CharField(max_length=50)),
                ('reason', models.TextField(max_length=500)),
                ('request_date', models.DateTimeField()),
                ('from_date', models.DateField()),
                ('to_date', models.DateField()),
            ],
            options={
                'db_table': 'leaves',
            },
        ),
    ]
