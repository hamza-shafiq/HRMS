# Generated by Django 4.1.1 on 2023-11-27 08:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0009_employee_remaining_leaves'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='extra_leaves',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='employee',
            name='total_leaves',
            field=models.IntegerField(default=18),
        ),
        migrations.AlterField(
            model_name='employee',
            name='remaining_leaves',
            field=models.IntegerField(default=18, null=True),
        ),
    ]
