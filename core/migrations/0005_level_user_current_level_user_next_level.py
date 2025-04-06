# Generated by Django 4.1.7 on 2024-01-14 12:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_customer_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Level',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('points', models.PositiveIntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='current_level',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='current_level', to='core.level'),
        ),
        migrations.AddField(
            model_name='user',
            name='next_level',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='next_level', to='core.level'),
        ),
    ]
