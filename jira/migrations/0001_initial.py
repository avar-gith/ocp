# Generated by Django 5.0.1 on 2024-09-18 21:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('organization', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Név')),
                ('description', models.TextField(verbose_name='Leírás')),
                ('status', models.CharField(choices=[('new', 'Új igény'), ('analysis', 'Elemzés'), ('implementation', 'Megvalósítás'), ('stopped', 'Elhalasztva'), ('escalation', 'Eszkaláció'), ('completed', 'Kész')], default='new', max_length=20, verbose_name='Státusz')),
                ('start_date', models.DateField(verbose_name='Kezdési dátum')),
                ('end_date', models.DateField(blank=True, null=True, verbose_name='Befejezési dátum')),
                ('deadline', models.DateField(blank=True, null=True, verbose_name='Határidő')),
                ('creator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_projects', to='organization.employee', verbose_name='Létrehozó')),
                ('responsible', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='responsible_projects', to='organization.employee', verbose_name='Felelős')),
            ],
            options={
                'verbose_name': 'Projekt',
                'verbose_name_plural': 'Projektek',
            },
        ),
        migrations.CreateModel(
            name='Story',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Név')),
                ('description', models.TextField(verbose_name='Leírás')),
                ('status', models.CharField(choices=[('new', 'Új igény'), ('analysis', 'Elemzés'), ('implementation', 'Megvalósítás'), ('stopped', 'Elhalasztva'), ('escalation', 'Eszkaláció'), ('completed', 'Kész')], default='new', max_length=20, verbose_name='Státusz')),
                ('creation_date', models.DateField(verbose_name='Létrehozási dátum')),
                ('deadline', models.DateField(blank=True, null=True, verbose_name='Határidő')),
                ('creator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_stories', to='organization.employee', verbose_name='Létrehozó')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stories', to='jira.project', verbose_name='Projekt')),
                ('responsible', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='responsible_stories', to='organization.employee', verbose_name='Felelős')),
            ],
            options={
                'verbose_name': 'Történet',
                'verbose_name_plural': 'Történetek',
            },
        ),
        migrations.CreateModel(
            name='Sprint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200, verbose_name='Név')),
                ('created_at', models.DateField(verbose_name='Létrehozás dátuma')),
                ('story', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sprints', to='jira.story', verbose_name='Történet')),
            ],
            options={
                'verbose_name': 'Sprint',
                'verbose_name_plural': 'Sprint-ek',
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Név')),
                ('description', models.TextField(verbose_name='Leírás')),
                ('status', models.CharField(choices=[('new', 'Új igény'), ('analysis', 'Elemzés'), ('implementation', 'Megvalósítás'), ('stopped', 'Elhalasztva'), ('escalation', 'Eszkaláció'), ('completed', 'Kész')], default='new', max_length=20, verbose_name='Státusz')),
                ('creation_date', models.DateField(verbose_name='Létrehozási dátum')),
                ('deadline', models.DateField(blank=True, null=True, verbose_name='Határidő')),
                ('creator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_tasks', to='organization.employee', verbose_name='Létrehozó')),
                ('project', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='jira.project', verbose_name='Projekt')),
                ('responsible', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='responsible_tasks', to='organization.employee', verbose_name='Felelős')),
                ('story', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='jira.story', verbose_name='Történet')),
            ],
            options={
                'verbose_name': 'Feladat',
                'verbose_name_plural': 'Feladatok',
            },
        ),
        migrations.CreateModel(
            name='TaskStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('new', 'Új igény'), ('analysis', 'Elemzés'), ('implementation', 'Megvalósítás'), ('stopped', 'Elhalasztva'), ('escalation', 'Eszkaláció'), ('completed', 'Kész')], max_length=20, verbose_name='Státusz')),
                ('sprint', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='task_statuses', to='jira.sprint', verbose_name='Sprint')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jira.task', verbose_name='Feladat')),
            ],
            options={
                'verbose_name': 'Feladat állapota',
                'verbose_name_plural': 'Feladatok állapotai',
                'unique_together': {('sprint', 'task')},
            },
        ),
    ]
