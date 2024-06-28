# Generated by Django 4.1.1 on 2024-06-27 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0008_attendance_total_time_alter_leaves_leave_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leaves',
            name='leave_type',
            field=models.CharField(choices=[('SICK_LEAVE', 'SICK_LEAVE'), ('CASUAL_LEAVE', 'CASUAL_LEAVE'), ('MATERNITY_LEAVE', 'MATERNITY_LEAVE'), ('PATERNITY_LEAVE', 'PATERNITY_LEAVE'), ('MARRIAGE_LEAVE', 'MARRIAGE_LEAVE'), ('EMERGENCY_LEAVE', 'EMERGENCY_LEAVE'), ('WORK_FROM_HOME', 'WORK_FROM_HOME'), ('EXTRA_DAYS', 'EXTRA_DAYS')], max_length=50),
        ),
    ]
