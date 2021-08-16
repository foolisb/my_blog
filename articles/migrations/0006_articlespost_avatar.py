# Generated by Django 3.2.5 on 2021-08-02 12:29

from django.db import migrations
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0005_articlespost_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='articlespost',
            name='avatar',
            field=imagekit.models.fields.ProcessedImageField(blank=True, upload_to='article/avatar/%Y%m%d'),
        ),
    ]