# file: office/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import Email
from jira.models import Project, Story, Task
from organization.models import Employee

def get_project_status_message(project, status):
    """
    Visszaadja a státuszhoz tartozó üzenetet a projekthez.
    """
    status_messages = {
        'new': f'A "{project.name}" projekt státusza most "Új igény". További részletekért nézze meg a projektet.',
        'analysis': f'A "{project.name}" projekt állapota "Elemzés". Kérjük, tekintse át a projekt követelményeit.',
        'implementation': f'A "{project.name}" projekt állapota "Megvalósítás". Az aktuális feladatok nyomon követéséhez kérjük, ellenőrizze a projektet.',
        'stopped': f'A "{project.name}" projekt státusza "Elhalasztva". Kérjük, nézze meg a projekt állapotát és az új ütemtervet.',
        'escalation': f'A "{project.name}" projekt állapota "Eszkaláció". Kérjük, ellenőrizze az eszkalációs intézkedéseket.',
        'completed': f'A "{project.name}" projekt befejeződött. Kérjük, nézze át az eredményeket és zárja le a projektet.',
    }
    return status_messages.get(status, 'Ismeretlen státusz')

def get_story_status_message(story, status):
    """
    Visszaadja a státuszhoz tartozó üzenetet a történethez.
    """
    status_messages = {
        'new': f'A "{story.name}" történet újonnan létrejött a "{story.project.name}" projektben. Az új státusz: "Új igény". Kérjük, ellenőrizze a történetet.',
        'analysis': f'A "{story.name}" történet állapota most "Elemzés". Kérjük, nézze át a történet követelményeit a "{story.project.name}" projektben.',
        'implementation': f'A "{story.name}" történet most a "Megvalósítás" státuszban van. Kérjük, kövesse nyomon a feladatok előrehaladását a "{story.project.name}" projektben.',
        'stopped': f'A "{story.name}" történet státusza "Elhalasztva". Kérjük, ellenőrizze a történet állapotát és az új ütemtervet a "{story.project.name}" projektben.',
        'escalation': f'A "{story.name}" történet állapota "Eszkaláció". Kérjük, vizsgálja meg az eszkalációs intézkedéseket a "{story.project.name}" projektben.',
        'completed': f'A "{story.name}" történet befejeződött. Kérjük, nézze át az eredményeket a "{story.project.name}" projektben és zárja le a történetet.',
    }
    return status_messages.get(status, 'Ismeretlen státusz')

def get_task_status_message(task, status):
    """
    Visszaadja a státuszhoz tartozó üzenetet a feladathoz.
    """
    status_messages = {
        'new': f'A "{task.name}" feladat újonnan létrejött a "{task.story.name}" történetben a "{task.project.name}" projektben. Státusz: "Új igény".\n\nLeírás: {task.description}\nHatáridő: {task.deadline}',
        'analysis': f'A "{task.name}" feladat most "Elemzés" státuszban van a "{task.story.name}" történetben a "{task.project.name}" projektben.\n\nLeírás: {task.description}\nHatáridő: {task.deadline}',
        'implementation': f'A "{task.name}" feladat "Megvalósítás" státuszban van a "{task.story.name}" történetben a "{task.project.name}" projektben.\n\nLeírás: {task.description}\nHatáridő: {task.deadline}',
        'stopped': f'A "{task.name}" feladat "Elhalasztva" státuszba került a "{task.story.name}" történetben a "{task.project.name}" projektben.\n\nLeírás: {task.description}\nHatáridő: {task.deadline}',
        'escalation': f'A "{task.name}" feladat "Eszkaláció" státuszba került a "{task.story.name}" történetben a "{task.project.name}" projektben.\n\nLeírás: {task.description}\nHatáridő: {task.deadline}',
        'completed': f'A "{task.name}" feladat befejeződött a "{task.story.name}" történetben a "{task.project.name}" projektben.\n\nLeírás: {task.description}\nHatáridő: {task.deadline}',
    }
    return status_messages.get(status, 'Ismeretlen státusz')

@receiver(post_save, sender=Project)
def send_project_status_email(sender, instance, created, **kwargs):
    """
    Signal kezelő, amely e-mailt küld, amikor egy projekt létrejön, lezáródik, vagy státuszt vált.
    """
    if created:
        message = f'A projekt "{instance.name}" újonnan létrejött. A projekt állapota: {instance.get_status_display()}.'
    else:
        previous_status = sender.objects.get(pk=instance.pk).status
        if previous_status != instance.status:
            message = get_project_status_message(instance, instance.status)
        elif instance.end_date and instance.end_date <= timezone.now().date():
            message = f'A projekt "{instance.name}" lezárult. Az állapota: {instance.get_status_display()}.'
        else:
            return

    first_employee = Employee.objects.first()
    if not first_employee:
        return

    recipients = []
    if instance.creator:
        recipients.append(instance.creator)
    if instance.responsible:
        recipients.append(instance.responsible)

    if recipients:
        if not Email.objects.filter(
            sender=first_employee,
            content=message,
            sent_at__date=timezone.now().date()
        ).exists():
            Email.objects.create(
                sender=first_employee,
                content=message,
                sent_at=timezone.now()
            )

@receiver(post_save, sender=Story)
def send_story_status_email(sender, instance, created, **kwargs):
    """
    Signal kezelő, amely e-mailt küld, amikor egy történet létrejön, lezáródik, vagy státuszt vált.
    """
    if created:
        message = f'A "{instance.name}" történet újonnan létrejött a "{instance.project.name}" projektben. Az új státusz: {instance.get_status_display()}.'
    else:
        previous_status = sender.objects.get(pk=instance.pk).status
        if previous_status != instance.status:
            message = get_story_status_message(instance, instance.status)
        else:
            return

    first_employee = Employee.objects.first()
    if not first_employee:
        return

    recipients = []
    if instance.creator:
        recipients.append(instance.creator)
    if instance.responsible:
        recipients.append(instance.responsible)

    if recipients:
        if not Email.objects.filter(
            sender=first_employee,
            content=message,
            sent_at__date=timezone.now().date()
        ).exists():
            Email.objects.create(
                sender=first_employee,
                content=message,
                sent_at=timezone.now()
            )

@receiver(post_save, sender=Task)
def send_task_status_email(sender, instance, created, **kwargs):
    """
    Signal kezelő, amely e-mailt küld, amikor egy feladat létrejön, státuszt vált, vagy más jelentős esemény történik.
    """
    if created:
        message = f'A "{instance.name}" feladat újonnan létrejött a "{instance.story.name}" történetben a "{instance.project.name}" projektben.\n\nLeírás: {instance.description}\nHatáridő: {instance.deadline}\nStátusz: {instance.get_status_display()}.'
    else:
        previous_status = sender.objects.get(pk=instance.pk).status
        if previous_status != instance.status:
            message = get_task_status_message(instance, instance.status)
        else:
            return

    first_employee = Employee.objects.first()
    if not first_employee:
        return

    recipients = []
    if instance.creator:
        recipients.append(instance.creator)
    if instance.responsible:
        recipients.append(instance.responsible)

    if recipients:
        if not Email.objects.filter(
            sender=first_employee,
            content=message,
            sent_at__date=timezone.now().date()
        ).exists():
            Email.objects.create(
                sender=first_employee,
                content=message,
                sent_at=timezone.now()
            )
