# Generated by Django 4.2.6 on 2023-10-18 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ProfileApp', '0002_teacher_count_peaple_teacher_max_peaple_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacher',
            name='count_peaple',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='max_peaple',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
