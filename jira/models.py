# file: jira/models.py

from django.db import models
from organization.models import Employee

class Project(models.Model):
    STATUS_CHOICES = [
        ('new', 'Új igény'),
        ('analysis', 'Elemzés'),
        ('implementation', 'Megvalósítás'),
        ('stopped', 'Elhalasztva'),
        ('escalation', 'Eszkaláció'),
        ('completed', 'Kész'),
    ]

    name = models.CharField(max_length=200, verbose_name='Név')
    description = models.TextField(verbose_name='Leírás')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name='Státusz')
    start_date = models.DateField(verbose_name='Kezdési dátum')
    end_date = models.DateField(verbose_name='Befejezési dátum', null=True, blank=True)
    deadline = models.DateField(verbose_name='Határidő', null=True, blank=True)
    creator = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_projects', verbose_name='Létrehozó')
    responsible = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True, related_name='responsible_projects', verbose_name='Felelős')

    class Meta:
        verbose_name = 'Projekt'
        verbose_name_plural = 'Projektek'

    def __str__(self):
        return self.name

class Story(models.Model):
    STATUS_CHOICES = [
        ('new', 'Új igény'),
        ('analysis', 'Elemzés'),
        ('implementation', 'Megvalósítás'),
        ('stopped', 'Elhalasztva'),
        ('escalation', 'Eszkaláció'),
        ('completed', 'Kész'),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='stories', verbose_name='Projekt')
    name = models.CharField(max_length=200, verbose_name='Név')
    description = models.TextField(verbose_name='Leírás')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name='Státusz')
    creation_date = models.DateField(verbose_name='Létrehozási dátum')
    deadline = models.DateField(verbose_name='Határidő', null=True, blank=True)
    creator = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_stories', verbose_name='Létrehozó')
    responsible = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True, related_name='responsible_stories', verbose_name='Felelős')

    class Meta:
        verbose_name = 'Történet'
        verbose_name_plural = 'Történetek'

    def __str__(self):
        return self.name

class Task(models.Model):
    STATUS_CHOICES = [
        ('new', 'Új igény'),
        ('analysis', 'Elemzés'),
        ('implementation', 'Megvalósítás'),
        ('stopped', 'Elhalasztva'),
        ('escalation', 'Eszkaláció'),
        ('completed', 'Kész'),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks', verbose_name='Projekt', null=True, blank=True)
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='tasks', verbose_name='Történet', null=True, blank=True)
    name = models.CharField(max_length=200, verbose_name='Név')
    description = models.TextField(verbose_name='Leírás')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name='Státusz')
    creation_date = models.DateField(verbose_name='Létrehozási dátum')
    deadline = models.DateField(verbose_name='Határidő', null=True, blank=True)
    creator = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_tasks', verbose_name='Létrehozó')
    responsible = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True, related_name='responsible_tasks', verbose_name='Felelős')

    class Meta:
        verbose_name = 'Feladat'
        verbose_name_plural = 'Feladatok'

    def __str__(self):
        return self.name
