# file: jira/management/commands/generate_random_story.py

import json
import random
from django.core.management.base import BaseCommand
from jira.models import Project, Story, Employee
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Generál egy véletlenszerű történetet egy nyitott projekthez és elmenti az adatbázisba.'

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

        # Véletlenszerű projekt kiválasztása
        selected_project = random.choice(projects)

        # Új történet létrehozása
        creator = random.choice(Employee.objects.all())
        responsible = random.choice(Employee.objects.all())

        # Státusz beállítása
        status = random.choice(['new', 'analysis', 'implementation'])

        creation_date = datetime.now()
        deadline = creation_date + timedelta(days=random.randint(30, 180))  # Határidő 1-6 hónap között

        new_story = Story(
            project=selected_project,
            name=random.choice(tasknames),
            description=random.choice(taskdescriptions),
            status=status,
            creation_date=creation_date,
            deadline=deadline,
            creator=creator,
            responsible=responsible
        )
        new_story.save()

        self.stdout.write(self.style.SUCCESS('Random történet sikeresen generálva és elmentve az adatbázisba.'))
