# Generated by Django 3.2.5 on 2021-08-05 16:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0011_alter_articlespost_text'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='articlespost',
            options={'ordering': ('-updated',)},
        ),
    ]
