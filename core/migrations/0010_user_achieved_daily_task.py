# Generated by Django 4.1.7 on 2024-01-15 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_user_daily_target'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='achieved_daily_task',
            field=models.BooleanField(default=False),
        ),
    ]
