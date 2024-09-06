# Generated by Django 5.0.7 on 2024-09-06 06:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0004_subscribe'),
    ]

    operations = [
        migrations.CreateModel(
            name='Faq',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250, verbose_name='Заголовок')),
                ('description', models.TextField(verbose_name='Описание')),
            ],
            options={
                'verbose_name': 'Faq',
                'verbose_name_plural': 'Faq',
                'db_table': 'faq',
            },
        ),
    ]
