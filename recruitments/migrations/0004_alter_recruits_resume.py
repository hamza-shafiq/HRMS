# Generated by Django 4.1.1 on 2023-02-07 09:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recruitments', '0003_alter_recruits_resume'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recruits',
            name='resume',
            field=models.FileField(upload_to='media'),
        ),
    ]
