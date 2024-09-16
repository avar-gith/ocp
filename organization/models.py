# file: organization/models.py

from django.db import models

class Company(models.Model):
    name = models.CharField(max_length=100, verbose_name='Név')
    description = models.TextField(verbose_name='Leírás')

    class Meta:
        verbose_name = 'Vállalat'
        verbose_name_plural = 'Vállalatok'

    def __str__(self):
        return self.name

class Team(models.Model):
    name = models.CharField(max_length=100, verbose_name='Név')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name='Vállalat')
    description = models.TextField(verbose_name='Leírás')

    class Meta:
        verbose_name = 'Csapat'
        verbose_name_plural = 'Csapatok'

    def __str__(self):
        return self.name

class Squad(models.Model):
    name = models.CharField(max_length=100, verbose_name='Név')
    team = models.ForeignKey(Team, on_delete=models.CASCADE, verbose_name='Csapat')
    description = models.TextField(verbose_name='Leírás')

    class Meta:
        verbose_name = 'Squad'
        verbose_name_plural = 'Squadok'

    def __str__(self):
        return self.name

class Position(models.Model):
    name = models.CharField(max_length=100, verbose_name='Név')
    description = models.TextField(verbose_name='Leírás')

    class Meta:
        verbose_name = 'Pozíció'
        verbose_name_plural = 'Pozíciók'

    def __str__(self):
        return self.name

class Employee(models.Model):
    name = models.CharField(max_length=100, verbose_name='Név')
    squad = models.ForeignKey(Squad, on_delete=models.CASCADE, verbose_name='Squad')
    position = models.ForeignKey(Position, on_delete=models.CASCADE, verbose_name='Pozíció')

    class Meta:
        verbose_name = 'Kolléga'
        verbose_name_plural = 'Kollégák'

    def __str__(self):
        return self.name

class Skill(models.Model):
    name = models.CharField(max_length=100, verbose_name='Név')
    level = models.IntegerField(verbose_name='Szint')
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name='Kolléga')

    class Meta:
        verbose_name = 'Készség'
        verbose_name_plural = 'Készségek'

    def __str__(self):
        return self.name
