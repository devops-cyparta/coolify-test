# Generated by Django 4.1.7 on 2024-01-15 11:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_user_achieved_daily_task'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='achieved_daily_task',
            new_name='achieved_daily_target',
        ),
    ]
