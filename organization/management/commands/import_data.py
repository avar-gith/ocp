# file: organization/management/commands/import_data.py

import json
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from organization.models import Company, Team, Squad, Position, Employee, Skill

class Command(BaseCommand):
    help = 'Importálja az adatokat egy JSON fájlból az adatbázisba.'

    def handle(self, *args, **options):
        # JSON fájl elérési útja
        json_file = 'static/organization/data.json'
        file_path = os.path.join(settings.BASE_DIR, json_file)
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'Fájl nem található: {file_path}'))
            return
        except json.JSONDecodeError:
            self.stdout.write(self.style.ERROR(f'JSON dekódolási hiba a fájlban: {file_path}'))
            return

        # Töröld a meglévő adatokat
        Company.objects.all().delete()
        Team.objects.all().delete()
        Squad.objects.all().delete()
        Position.objects.all().delete()
        Employee.objects.all().delete()
        Skill.objects.all().delete()

        # Vállalatok importálása
        for company_data in data.get('companies', []):
            Company.objects.create(
                name=company_data['name'],
                description=company_data['description']
            )

        # Csapatok importálása
        for team_data in data.get('teams', []):
            company = Company.objects.get(name=team_data['company'])
            Team.objects.create(
                name=team_data['name'],
                company=company,
                description=team_data['description']
            )

        # Squads importálása
        for squad_data in data.get('squads', []):
            team = Team.objects.get(name=squad_data['team'])
            Squad.objects.create(
                name=squad_data['name'],
                team=team,
                description=squad_data['description']
            )

        # Pozíciók importálása
        for position_data in data.get('positions', []):
            Position.objects.create(
                name=position_data['name'],
                description=position_data['description']
            )

        # Kollégák importálása
        for employee_data in data.get('employees', []):
            squad = Squad.objects.get(name=employee_data['squad'])
            position = Position.objects.get(name=employee_data['position'])
            Employee.objects.create(
                name=employee_data['name'],
                squad=squad,
                position=position
            )

        # Készségek importálása, ha létezik
        skills = data.get('skills', [])
        if skills:
            for skill_data in skills:
                employee = Employee.objects.get(name=skill_data['employee'])
                Skill.objects.create(
                    name=skill_data['name'],
                    level=skill_data['level'],
                    employee=employee
                )
                