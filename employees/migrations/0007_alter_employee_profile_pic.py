# Generated by Django 4.1.1 on 2023-02-22 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0006_alter_employee_joining_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='profile_pic',
            field=models.FileField(upload_to='images', verbose_name='profile img'),
        ),
    ]