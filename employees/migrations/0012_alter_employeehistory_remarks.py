# Generated by Django 4.1.1 on 2024-07-12 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0011_employeehistory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeehistory',
            name='remarks',
            field=models.TextField(max_length=500),
        ),
    ]
