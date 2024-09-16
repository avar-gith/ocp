# file: jira/management/commands/import_projects.py

import json
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from jira.models import Project, Story
from organization.models import Employee

class Command(BaseCommand):
    help = 'Importálja a projekteket és történeteket JSON fájlokból az adatbázisba.'

    def handle(self, *args, **options):
        # JSON fájlok elérési útjai
        project_file = 'static/jira/projects.json'
        story_file = 'static/jira/stories.json'
        
        # Fájl elérési utak
        project_path = os.path.join(settings.BASE_DIR, project_file)
        story_path = os.path.join(settings.BASE_DIR, story_file)

        # Töröld a meglévő projekteket és történeteket
        Project.objects.all().delete()
        Story.objects.all().delete()

        # Importáljuk a projekteket
        self.import_projects(project_path)

        # Importáljuk a történeteket
        self.import_stories(story_path)

        self.stdout.write(self.style.SUCCESS('Projektek és történetek sikeresen importálva.'))

    def import_projects(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'Fájl nem található: {file_path}'))
            return
        except json.JSONDecodeError:
            self.stdout.write(self.style.ERROR(f'JSON dekódolási hiba a fájlban: {file_path}'))
            return

        for project_data in data.get('projects', []):
            try:
                creator = Employee.objects.get(id=project_data['creator_id'])
                responsible = Employee.objects.get(id=project_data['responsible_id'])
                
                # Ha a 'deadline' mező nincs, használjuk az 'end_date' értékét
                end_date = project_data.get('end_date')
                deadline = project_data.get('deadline', end_date)
                
            except Employee.DoesNotExist as e:
                self.stdout.write(self.style.ERROR(f'Employee nem található: {str(e)}'))
                continue

            Project.objects.create(
                name=project_data['name'],
                description=project_data['description'],
                status=project_data['status'],
                start_date=project_data['start_date'],
                end_date=end_date,
                deadline=end_date,
                creator=creator,
                responsible=responsible
            )
        self.stdout.write(self.style.SUCCESS('Projektek sikeresen importálva.'))

    def import_stories(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'Fájl nem található: {file_path}'))
            return
        except json.JSONDecodeError:
            self.stdout.write(self.style.ERROR(f'JSON dekódolási hiba a fájlban: {file_path}'))
            return

        for story_data in data.get('stories', []):
            try:
                project = Project.objects.get(id=story_data['project_id'])
                creator = Employee.objects.get(id=story_data['creator_id'])
                responsible = Employee.objects.get(id=story_data['responsible_id'])
            except (Project.DoesNotExist, Employee.DoesNotExist) as e:
                self.stdout.write(self.style.ERROR(f'{str(e)}'))
                continue

            Story.objects.create(
                name=story_data['name'],
                project=project,
                description=story_data['description'],
                status=story_data['status'],
                creation_date=story_data['creation_date'],
                deadline=story_data['deadline'],
                creator=creator,
                responsible=responsible
            )
        self.stdout.write(self.style.SUCCESS('Történetek sikeresen importálva.'))
