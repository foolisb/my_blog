# Generated by Django 3.2.5 on 2021-08-02 15:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0008_articlespost_avatar'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='articlespost',
            name='avatar',
        ),
    ]
