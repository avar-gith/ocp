# Generated by Django 5.0.1 on 2024-09-18 17:17

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('organization', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Email',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=255, verbose_name='Tárgy')),
                ('sent_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Küldés időpontja')),
                ('content', models.TextField(verbose_name='Tartalom')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_emails', to='organization.employee', verbose_name='Küldő')),
            ],
            options={
                'verbose_name': 'Mail',
                'verbose_name_plural': 'Mailek',
                'ordering': ['-sent_at'],
            },
        ),
        migrations.CreateModel(
            name='WikiPage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, unique=True, verbose_name='Cím')),
                ('description', models.TextField(verbose_name='Leírás')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Létrehozás időpontja')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_pages', to='organization.employee', verbose_name='Készítő')),
            ],
            options={
                'verbose_name': 'Wiki oldal',
                'verbose_name_plural': 'Wiki oldalak',
                'ordering': ['-created_at'],
            },
        ),
    ]
