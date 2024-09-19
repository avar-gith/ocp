# file: organization/management/commands/getapiinfo.py

import json
import requests
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Lekérdezi az API információkat és létrehoz egy sampledata.json fájlt.'

    def handle(self, *args, **options):
        # Definiáld az API listát
        api_list = {
            "employees": "http://localhost:8000/api/organization/employees/",
            "teams": "http://localhost:8000/api/organization/teams/",
            "emails": "http://localhost:8000/api/office/emails/",
            "tasks": "http://localhost:8000/api/jira/tasks/",
            "skills": "http://localhost:8000/api/organization/skills/",
            "positions": "http://localhost:8000/api/organization/positions/",
            "projects": "http://localhost:8000/api/jira/projects/",
            "squads": "http://localhost:8000/api/organization/squads/",
            "stories": "http://localhost:8000/api/jira/stories/",
            "companies": "http://localhost:8000/api/organization/companies/",
            "wikipages": "http://localhost:8000/api/office/wikipages/"
        }

        sample_data = {}

        # Lekérdezzük az API-kat és minta adatokat generálunk
        for key, url in api_list.items():
            self.stdout.write(f'Lekérdezés: {key} - {url}')
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    data = response.json()
                    sample_data[key] = data[:2] if data else []  # Legfeljebb 2 elem, vagy üres lista
                    self.stdout.write(f'Sikeres lekérdezés: {key}, {len(data)} elem található.')
                else:
                    self.stdout.write(self.style.ERROR(f'Hiba a lekérdezés során: {key}, állapotkód: {response.status_code}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Hiba történt az API lekérdezése közben: {e}'))

        # Mintaadatok mentése JSON fájlba
        with open('sampledata.json', 'w', encoding='utf-8') as json_file:
            json.dump(sample_data, json_file, ensure_ascii=False, indent=4)

        self.stdout.write(self.style.SUCCESS('Mintaadatok sikeresen létrehozva: sampledata.json'))
