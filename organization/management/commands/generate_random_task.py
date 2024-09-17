# file: jira/management/commands/generate_random_task.py

import json
import random
from django.core.management.base import BaseCommand
from jira.models import Project, Story, Employee, Task
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Generál egy véletlenszerű feladatot egy nyitott projekthez és történethez.'

    def handle(self, *args, **options):
        tasknames_file = 'static/jira/tasknames.json'
        taskdescriptions_file = 'static/jira/taskdescriptions.json'

        # Task neveket tartalmazó JSON fájl betöltése
        with open(tasknames_file, 'r', encoding='utf-8') as f:
            tasknames = json.load(f)

        # Task leírásokat tartalmazó JSON fájl betöltése
        with open(taskdescriptions_file, 'r', encoding='utf-8') as f:
            taskdescriptions = json.load(f)

        # Nyitott projektek keresése
        projects = Project.objects.filter(status='implementation')
        if not projects:
            self.stderr.write(self.style.ERROR('Nincs nyitott projekt.'))
            return

        # Nyitott történetek kiválasztása
        valid_stories = []
        for project in projects:
            stories = Story.objects.filter(project_id=project.id, status='new')
            valid_stories.extend(stories)

        if not valid_stories:
            self.stderr.write(self.style.ERROR('Nincs nyitott történet a nyitott projektekben.'))
            return

        # Véletlenszerű projekt és történet kiválasztása
        selected_story = random.choice(valid_stories)
        selected_project = selected_story.project  # A történethez tartozó projekt

        creator = random.choice(Employee.objects.all())
        responsible = random.choice(Employee.objects.all())

        # Státusz beállítása
        status = random.choice(['new', 'analysis', 'implementation'])

        # Dátum generálás
        creation_date = datetime.now() + timedelta(days=random.randint(0, 30))
        deadline = creation_date + timedelta(days=random.randint(1, 60))

        # Új feladat létrehozása és mentése az adatbázisba
        new_task = Task(
            project=selected_project,
            story=selected_story,
            name=random.choice(tasknames),
            description=random.choice(taskdescriptions),
            status=status,
            creation_date=creation_date,
            deadline=deadline,
            creator=creator,
            responsible=responsible
        )
        new_task.save()

        self.stdout.write(self.style.SUCCESS('Random feladat sikeresen generálva és elmentve az adatbázisba.'))
