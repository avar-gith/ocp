# file: jira/management/commands/generate_random_project.py

import json
import random
from django.core.management.base import BaseCommand
from jira.models import Project, Employee
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Generál egy véletlenszerű projektet és elmenti az adatbázisba.'

    def handle(self, *args, **options):
        tasknames_file = 'static/jira/projectnames.json'
        taskdescriptions_file = 'static/jira/projectdescriptions.json'

        # Projekt neveket tartalmazó JSON fájl betöltése
        with open(tasknames_file, 'r', encoding='utf-8') as f:
            projectnames = json.load(f)

        # Projekt leírásokat tartalmazó JSON fájl betöltése
        with open(taskdescriptions_file, 'r', encoding='utf-8') as f:
            projectdescriptions = json.load(f)

        # Nyitott projektek keresése
        existing_projects = Project.objects.filter(status='implementation').values_list('name', flat=True)

        # Véletlenszerű projekt létrehozása
        while True:
            name = random.choice(projectnames)
            if name not in existing_projects:
                break

        creation_date = datetime.now()
        deadline = creation_date + timedelta(days=17 * 30)  # Kb. 17 hónap

        creator = random.choice(Employee.objects.all())
        responsible = random.choice(Employee.objects.all())

        new_project = Project(
            name=name,
            description=random.choice(projectdescriptions),
            status='new',  # Kezdési státusz
            start_date=creation_date,
            end_date=deadline,
            deadline=deadline,
            creator=creator,
            responsible=responsible
        )
        new_project.save()

        self.stdout.write(self.style.SUCCESS('Random projekt sikeresen generálva és elmentve az adatbázisba.'))
