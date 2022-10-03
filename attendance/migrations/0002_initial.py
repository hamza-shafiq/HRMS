# Generated by Django 4.1.1 on 2022-10-03 15:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('employees', '0002_initial'),
        ('attendance', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='leaves',
            name='employee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='leaves', to='employees.employee'),
        ),
        migrations.AddField(
            model_name='attendance',
            name='employee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attendance', to='employees.employee'),
        ),
    ]
