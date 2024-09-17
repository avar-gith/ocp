# file: jira/management/commands/generate_tasks.py

import json
import random
from django.core.management.base import BaseCommand
from jira.models import Project, Story, Employee, Task
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Generál feladatokat és elmenti őket a static/jira/tasks.json fájlba.'

    def handle(self, *args, **options):
        tasks_file = 'static/jira/tasks.json'
        tasknames_file = 'static/jira/tasknames.json'
        taskdescriptions_file = 'static/jira/taskdescriptions.json'

        # Task neveket tartalmazó JSON fájl betöltése
        with open(tasknames_file, 'r', encoding='utf-8') as f:
            tasknames = json.load(f)

        # Task leírásokat tartalmazó JSON fájl betöltése
        with open(taskdescriptions_file, 'r', encoding='utf-8') as f:
            taskdescriptions = json.load(f)

        # Az adatokat a fájlba írjuk
        tasks = []
        
        # Generálás a példák alapján (itt feltételezzük, hogy már léteznek projektek és történetek)
        projects = Project.objects.all()
        stories = Story.objects.all()
        employees = Employee.objects.all()
        
        if not projects or not stories or not employees:
            self.stderr.write(self.style.ERROR('Nincs elegendő projekt, történet vagy alkalmazott az adatbázisban.'))
            return

        for _ in range(214):  # 214 feladatot generálunk
            project = random.choice(projects)
            story = random.choice(stories.filter(project_id=project.id))
            creator = random.choice(employees)
            responsible = random.choice(employees)

            # Státusz logika a történet alapján
            if project.status == 'completed':
                status = 'completed' if random.random() < 0.5 else 'stopped'
            else:
                status = random.choice(['new', 'analysis', 'implementation'])

            # Dátum generálás
            creation_date = story.creation_date + timedelta(days=random.randint(0, 30))
            deadline = creation_date + timedelta(days=random.randint(1, 60))

            task_data = {
                'project_id': project.id,
                'story_id': story.id,
                'creator_id': creator.id,
                'responsible_id': responsible.id,
                'name': random.choice(tasknames),
                'description': random.choice(taskdescriptions),
                'status': status,
                'creation_date': creation_date.strftime('%Y-%m-%d'),
                'deadline': deadline.strftime('%Y-%m-%d')
            }
            tasks.append(task_data)

        # Feladatok mentése a JSON fájlba
        with open(tasks_file, 'w', encoding='utf-8') as f:
            json.dump({'tasks': tasks}, f, ensure_ascii=False, indent=4)

        self.stdout.write(self.style.SUCCESS(f'Feladatok sikeresen generálva és elmentve a "{tasks_file}" fájlba.'))