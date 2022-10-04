# Generated by Django 4.1.1 on 2022-10-04 08:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
        ('employees', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('phone_number', models.TextField(max_length=20)),
                ('national_id_number', models.CharField(max_length=50, unique=True)),
                ('emergency_contact_number', models.TextField(max_length=20)),
                ('gender', models.CharField(choices=[('FEMALE', 'FEMALE'), ('MALE', 'MALE'), ('OTHER', 'OTHER')], max_length=255)),
                ('designation', models.CharField(max_length=50)),
                ('bank', models.CharField(max_length=50)),
                ('account_number', models.TextField(max_length=50)),
                ('profile_pic', models.URLField()),
                ('joining_date', models.DateTimeField()),
                ('employee_status', models.CharField(choices=[('WORKING', 'WORKING'), ('RESIGNED', 'RESIGNED'), ('FIRED', 'FIRED')], max_length=50)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employees', to='employees.department')),
            ],
            options={
                'abstract': False,
            },
            bases=('user.user',),
        ),
    ]
