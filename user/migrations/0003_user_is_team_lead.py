# Generated by Django 4.1.1 on 2024-07-23 13:43

from django.db import migrations, models



class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_user_is_admin'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_team_lead',
            field=models.BooleanField(default=False),
        ),
    ]