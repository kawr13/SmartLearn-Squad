# Generated by Django 4.2.6 on 2023-10-15 18:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profileapp', '0003_post_images'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='category',
        ),
        migrations.DeleteModel(
            name='Category',
        ),
    ]