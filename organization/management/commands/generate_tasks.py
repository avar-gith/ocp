# file: jira/management/commands/generate_tasks.py

import json
import random
from django.core.management.base import BaseCommand
from jira.models import Project, Story, Employee

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
            task_data = {
                'project_id': random.choice(projects).id,
                'story_id': random.choice(stories).id,
                'creator_id': random.choice(employees).id,
                'responsible_id': random.choice(employees).id,
                'name': random.choice(tasknames),
                'description': random.choice(taskdescriptions),
                'status': random.choice(['new', 'analysis', 'implementation', 'stopped', 'escalation', 'completed']),
                'creation_date': '2024-01-01',  # Példa dátum, ezt állíthatod igényeid szerint
                'deadline': '2024-12-31'  # Példa dátum, ezt állíthatod igényeid szerint
            }
            tasks.append(task_data)
        
        # Feladatok mentése a JSON fájlba
        with open(tasks_file, 'w', encoding='utf-8') as f:
            json.dump({'tasks': tasks}, f, ensure_ascii=False, indent=4)

        self.stdout.write(self.style.SUCCESS(f'Feladatok sikeresen generálva és elmentve a "{tasks_file}" fájlba.'))
