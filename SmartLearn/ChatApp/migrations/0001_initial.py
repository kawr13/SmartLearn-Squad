# Generated by Django 4.2.6 on 2023-11-07 21:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_chat', models.CharField(max_length=100, verbose_name='Название')),
                ('type', models.CharField(choices=[('D', 'Dialog'), ('C', 'Chat')], default='D', max_length=1, verbose_name='Тип')),
                ('members', models.ManyToManyField(related_name='chats', to=settings.AUTH_USER_MODEL, verbose_name='Участник')),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('is_readed', models.BooleanField(default=False)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author_message', to=settings.AUTH_USER_MODEL)),
                ('chat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='ChatApp.chat')),
            ],
            options={
                'ordering': ['timestamp'],
            },
        ),
    ]
