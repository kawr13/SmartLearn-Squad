# Generated by Django 4.2.6 on 2024-01-12 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CabinetApp', '0003_record_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='cabinet',
            name='user_count',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]