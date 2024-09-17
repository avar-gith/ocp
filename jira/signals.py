# file: jira/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Project, Story, Task
from office.services import send_mail

# Állapotváltásokhoz tartozó e-mail tartalom a projektekhez
STATUS_EMAIL_CONTENT = {
    'new': 'A projekt új igényként lett létrehozva.',
    'analysis': 'A projekt elemzés alatt áll.',
    'implementation': 'A projekt megvalósítása alatt áll.',
    'stopped': 'A projekt elhalasztva lett.',
    'escalation': 'A projekt eszkaláció alatt áll.',
    'completed': 'A projekt lezárásra került.',
}

# Magyar státuszok
STATUS_NAMES = {
    'new': 'Új igény',
    'analysis': 'Elemzés',
    'implementation': 'Megvalósítás',
    'stopped': 'Elhalasztva',
    'escalation': 'Eszkaláció',
    'completed': 'Kész',
}

@receiver(post_save, sender=Project)
def project_status_change(sender, instance, created, **kwargs):
    if created:
        content = 'A projekt létrehozva: ' + instance.name
        subject_prefix = 'Projekt létrehozva'
        send_mail(sender=instance.creator, project_name=instance.name, content=content, subject_prefix=subject_prefix)
    else:
        if instance.status in STATUS_EMAIL_CONTENT:
            content = STATUS_EMAIL_CONTENT[instance.status]
            subject_prefix = f'Projekt státusz: {instance.name} - {STATUS_NAMES[instance.status]}'
            send_mail(sender=instance.responsible, project_name=instance.name, content=content, subject_prefix=subject_prefix)

@receiver(post_save, sender=Story)
def story_created_or_updated(sender, instance, created, **kwargs):
    if created:
        content = (
            f'A történet létrehozva: {instance.name}\n'
            f'Felelős: {instance.responsible}\n'
            f'Határidő: {instance.deadline}\n'
            f'Leírás: {instance.description}'
        )
        subject_prefix = 'Story létrehozva'
        send_mail(sender=instance.creator, project_name=instance.name, content=content, subject_prefix=subject_prefix)
    else:
        content = (
            f'A történet frissítve: {instance.name}\n'
            f'Új státusz: {STATUS_NAMES[instance.status]}\n'
            f'Felelős: {instance.responsible}\n'
            f'Határidő: {instance.deadline}\n'
            f'Leírás: {instance.description}'
        )
        subject_prefix = 'Story frissítve'
        send_mail(sender=instance.responsible, project_name=instance.name, content=content, subject_prefix=subject_prefix)

@receiver(post_save, sender=Task)
def task_created_or_updated(sender, instance, created, **kwargs):
    if created:
        content = (
            f'A feladat létrehozva: {instance.name}\n'
            f'Felelős: {instance.responsible}\n'
            f'Határidő: {instance.deadline}\n'
            f'Leírás: {instance.description}'
        )
        subject_prefix = 'Feladat létrehozva'
        send_mail(sender=instance.creator, project_name=instance.name, content=content, subject_prefix=subject_prefix)
    else:
        content = (
            f'A feladat frissítve: {instance.name}\n'
            f'Új státusz: {STATUS_NAMES[instance.status]}\n'
            f'Felelős: {instance.responsible}\n'
            f'Határidő: {instance.deadline}\n'
            f'Leírás: {instance.description}'
        )
        subject_prefix = f'Feladat státusz: {instance.name} - {STATUS_NAMES[instance.status]}'
        send_mail(sender=instance.responsible, project_name=instance.name, content=content, subject_prefix=subject_prefix)
