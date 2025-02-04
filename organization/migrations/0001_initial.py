# Generated by Django 5.0.1 on 2024-09-18 21:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Név')),
                ('description', models.TextField(verbose_name='Leírás')),
            ],
            options={
                'verbose_name': 'Vállalat',
                'verbose_name_plural': 'Vállalatok',
            },
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Név')),
                ('description', models.TextField(verbose_name='Leírás')),
            ],
            options={
                'verbose_name': 'Pozíció',
                'verbose_name_plural': 'Pozíciók',
            },
        ),
        migrations.CreateModel(
            name='Squad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Név')),
                ('description', models.TextField(verbose_name='Leírás')),
            ],
            options={
                'verbose_name': 'Squad',
                'verbose_name_plural': 'Squadok',
            },
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Név')),
                ('position', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organization.position', verbose_name='Pozíció')),
                ('squad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organization.squad', verbose_name='Squad')),
            ],
            options={
                'verbose_name': 'Kolléga',
                'verbose_name_plural': 'Kollégák',
            },
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Név')),
                ('level', models.IntegerField(verbose_name='Szint')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organization.employee', verbose_name='Kolléga')),
            ],
            options={
                'verbose_name': 'Készség',
                'verbose_name_plural': 'Készségek',
            },
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Név')),
                ('description', models.TextField(verbose_name='Leírás')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organization.company', verbose_name='Vállalat')),
            ],
            options={
                'verbose_name': 'Csapat',
                'verbose_name_plural': 'Csapatok',
            },
        ),
        migrations.AddField(
            model_name='squad',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organization.team', verbose_name='Csapat'),
        ),
    ]
