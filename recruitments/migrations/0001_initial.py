# Generated by Django 4.1.1 on 2022-09-28 12:54

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
            name='Recruits',
            fields=[
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('is_deleted', models.BooleanField(default=False)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('config', models.JSONField(blank=True, default=dict)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('phone_number', models.TextField(max_length=20)),
                ('position', models.CharField(max_length=20)),
                ('resume', models.URLField()),
                ('status', models.CharField(choices=[('IN_PROCESS', 'IN_PROCESS'), ('SCHEDULED', 'SCHEDULED'), ('PENDING', 'PENDING'), ('SELECTED', 'SELECTED'), ('REJECTED', 'REJECTED')], max_length=100)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Referrals',
            fields=[
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('is_deleted', models.BooleanField(default=False)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('config', models.JSONField(blank=True, default=dict)),
                ('recruit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='referrers', to='recruitments.recruits')),
                ('referer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recruits_referred', to='employees.employee')),
            ],
            options={
                'unique_together': {('recruit', 'referer')},
            },
        ),
    ]