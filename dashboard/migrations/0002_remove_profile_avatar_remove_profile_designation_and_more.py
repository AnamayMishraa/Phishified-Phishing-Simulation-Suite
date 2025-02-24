# Generated by Django 5.1.5 on 2025-01-30 06:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='avatar',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='designation',
        ),
        migrations.AddField(
            model_name='profile',
            name='role',
            field=models.CharField(default='User', max_length=50),
        ),
    ]
