# Generated by Django 4.1.1 on 2024-03-20 10:11

from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0011_employeehistory'),
        ('recruitments', '0008_alter_referrals_referer'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecruitsHistory',
            fields=[
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('is_deleted', models.BooleanField(default=False)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('config', models.JSONField(blank=True, default=dict)),
                ('process_stage', models.CharField(max_length=255)),
                ('remarks', models.TextField(max_length=20)),
                ('event_date', models.DateField()),
                ('added_date', models.DateTimeField(auto_now_add=True)),
                ('added_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='recruit_history_added_by', to='employees.employee')),
                ('conduct_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='conduct_by', to='employees.employee')),
                ('recruit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recruit', to='recruitments.recruits')),
            ],
            options={
                'db_table': 'recruit_history',
            },
        ),
    ]
