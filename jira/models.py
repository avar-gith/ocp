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

class Sprint(models.Model):
    """
    Modell a sprintek tárolására.
    """
    story = models.ForeignKey(
        Story, 
        on_delete=models.CASCADE, 
        related_name='sprints', 
        verbose_name='Történet'
    )
    name = models.CharField(
        max_length=200, 
        verbose_name='Név', 
        blank=True
    )  # Neve automatikusan generálva
    created_at = models.DateField(
        verbose_name='Létrehozás dátuma'
    )

    class Meta:
        verbose_name = 'Sprint'
        verbose_name_plural = 'Sprint-ek'

    def save(self, *args, **kwargs):
        if not self.name:  # Ha a név még nincs megadva
            max_sprint_number = Sprint.objects.filter(story=self.story).count() + 1
            self.name = f'{self.story.name} (Sprint {max_sprint_number})'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class TaskStatus(models.Model):
    """
    Modell a feladatok állapotainak tárolására egy sprint során.
    """
    sprint = models.ForeignKey(
        Sprint, 
        on_delete=models.CASCADE, 
        related_name='task_statuses', 
        verbose_name='Sprint'
    )
    task = models.ForeignKey(
        Task, 
        on_delete=models.CASCADE, 
        verbose_name='Feladat'
    )
    status = models.CharField(
        max_length=20, 
        choices=Task.STATUS_CHOICES, 
        verbose_name='Státusz'
    )

    class Meta:
        verbose_name = 'Feladat állapota'
        verbose_name_plural = 'Feladatok állapotai'
        unique_together = ('sprint', 'task')  # Biztosítjuk, hogy egy feladat csak egyszer szerepeljen egy sprintben

    def __str__(self):
        return f'{self.task.name} - {self.get_status_display()}'