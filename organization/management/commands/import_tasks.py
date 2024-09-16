# file: jira/management/commands/import_tasks.py

import json
from django.core.management.base import BaseCommand
from jira.models import Project, Story, Task
from organization.models import Employee

class Command(BaseCommand):
    help = 'Feltölti a feladatokat az adatbázisba a JSON fájlból.'

    def handle(self, *args, **options):
        tasks_file = 'static/jira/tasks.json'
        
        # JSON fájl betöltése
        with open(tasks_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            tasks = data.get('tasks', [])

        # Státuszok validálása
        valid_statuses = {status[0] for status in Task.STATUS_CHOICES}

        # Adatok importálása
        for task_data in tasks:
            project_id = task_data.get('project_id')
            story_id = task_data.get('story_id')
            creator_id = task_data.get('creator_id')
            responsible_id = task_data.get('responsible_id')
            status = task_data.get('status')

            # Ellenőrizzük, hogy a státusz érvényes-e
            if status not in valid_statuses:
                self.stderr.write(self.style.ERROR(f'Invalid status "{status}" for task with ID {task_data.get("id")}.'))
                continue

            # Ellenőrizzük, hogy a projekt és a történet létezik
            project = Project.objects.filter(id=project_id).first()
            story = Story.objects.filter(id=story_id).first()
            creator = Employee.objects.filter(id=creator_id).first()
            responsible = Employee.objects.filter(id=responsible_id).first()

            if not project:
                self.stderr.write(self.style.ERROR(f'Projekt ID {project_id} nem található.'))
                continue

            if not story:
                self.stderr.write(self.style.ERROR(f'Történet ID {story_id} nem található.'))
                continue

            if not creator:
                self.stderr.write(self.style.ERROR(f'Létrehozó ID {creator_id} nem található.'))
                continue

            if not responsible:
                self.stderr.write(self.style.ERROR(f'Felelős ID {responsible_id} nem található.'))
                continue

            # Task létrehozása
            Task.objects.create(
                project=project,
                story=story,
                name=task_data.get('name'),
                description=task_data.get('description'),
                status=status,
                creation_date=task_data.get('creation_date'),
                deadline=task_data.get('deadline'),
                creator=creator,
                responsible=responsible
            )

        self.stdout.write(self.style.SUCCESS(f'Feladatok sikeresen importálva a "{tasks_file}" fájlból.'))
