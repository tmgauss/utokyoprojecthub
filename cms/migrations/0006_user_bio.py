# Generated by Django 2.2.11 on 2020-04-03 08:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0005_project_members'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='bio',
            field=models.TextField(blank=True, help_text='必須。140字以内。', max_length=140, verbose_name='自己紹介'),
        ),
    ]
