# Generated by Django 2.2.11 on 2020-03-27 05:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0002_auto_20200324_1601'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='members',
        ),
        migrations.RemoveField(
            model_name='project',
            name='tag',
        ),
    ]
