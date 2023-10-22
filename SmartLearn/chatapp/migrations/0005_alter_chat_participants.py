# Generated by Django 4.2.6 on 2023-10-22 16:32

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chatapp', '0004_message_chat'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chat',
            name='participants',
            field=models.ManyToManyField(related_name='chat', to=settings.AUTH_USER_MODEL),
        ),
    ]
