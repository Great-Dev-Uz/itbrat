# Generated by Django 5.0.7 on 2024-07-30 06:23

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='chatmessage',
            options={'verbose_name': 'Сообщение', 'verbose_name_plural': 'Сообщение'},
        ),
        migrations.AlterModelOptions(
            name='conversation',
            options={'verbose_name': 'Разговор', 'verbose_name_plural': 'Разговор'},
        ),
        migrations.AlterField(
            model_name='chatmessage',
            name='attachment',
            field=models.FileField(blank=True, null=True, upload_to='', verbose_name='Файл'),
        ),
        migrations.AlterField(
            model_name='chatmessage',
            name='conversation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='chat.conversation', verbose_name='Разговор'),
        ),
        migrations.AlterField(
            model_name='chatmessage',
            name='info',
            field=models.JSONField(blank=True, null=True, verbose_name='Информация'),
        ),
        migrations.AlterField(
            model_name='chatmessage',
            name='sender',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Отправитель'),
        ),
        migrations.AlterField(
            model_name='chatmessage',
            name='text',
            field=models.CharField(blank=True, max_length=200, verbose_name='Сообщение'),
        ),
        migrations.AlterField(
            model_name='conversation',
            name='initiator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='initiated_conversations', to=settings.AUTH_USER_MODEL, verbose_name='Инициатор'),
        ),
        migrations.AlterField(
            model_name='conversation',
            name='receiver',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='received_conversations', to=settings.AUTH_USER_MODEL, verbose_name='Получатель'),
        ),
        migrations.AlterModelTable(
            name='chatmessage',
            table='chat_message',
        ),
    ]
