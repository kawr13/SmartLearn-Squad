# Generated by Django 4.2.6 on 2023-10-11 11:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profileapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='images',
            field=models.ImageField(blank=True, default='static/image/profile_img/img.png', null=True, upload_to='users/images'),
        ),
    ]