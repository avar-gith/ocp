# file: adan/management/commands/load_apis.py

from django.core.management.base import BaseCommand
from adan.models import API

class Command(BaseCommand):
    help = 'API-k feltöltése meghatározott adatokkal'

    def handle(self, *args, **kwargs):
        # API adatok meghatározott URL-ekkel
        apis = [
            {
                'name': 'Projektek API',
                'url': 'http://localhost:8000/api/jira/projects/',
                'description': 'Ez a Jira projektekhez tartozó API.'
            },
            {
                'name': 'Történetek API',
                'url': 'http://localhost:8000/api/jira/stories/',
                'description': 'Ez a Jira történetekhez tartozó API.'
            },
            {
                'name': 'Feladatok API',
                'url': 'http://localhost:8000/api/jira/tasks/',
                'description': 'Ez a Jira feladatokhoz tartozó API.'
            },
            {
                'name': 'E-mailek API',
                'url': 'http://localhost:8000/api/office/emails/',
                'description': 'Ez az Office e-mailekhez tartozó API.'
            },
            {
                'name': 'Wikipages API',
                'url': 'http://localhost:8000/api/office/wikipages/',
                'description': 'Ez az Office wikipages-hez tartozó API.'
            },
            {
                'name': 'Vállalatok API',
                'url': 'http://localhost:8000/api/organization/companies/',
                'description': 'Ez a szervezethez tartozó vállalatok API-ja.'
            },
            {
                'name': 'Csapatok API',
                'url': 'http://localhost:8000/api/organization/teams/',
                'description': 'Ez a szervezet csapataihoz tartozó API.'
            },
            {
                'name': 'Squadok API',
                'url': 'http://localhost:8000/api/organization/squads/',
                'description': 'Ez a szervezet squadjaihoz tartozó API.'
            },
            {
                'name': 'Pozíciók API',
                'url': 'http://localhost:8000/api/organization/positions/',
                'description': 'Ez a szervezet pozícióihoz tartozó API.'
            },
            {
                'name': 'Alkalmazottak API',
                'url': 'http://localhost:8000/api/organization/employees/',
                'description': 'Ez a szervezet alkalmazottaihoz tartozó API.'
            },
            {
                'name': 'Készségek API',
                'url': 'http://localhost:8000/api/organization/skills/',
                'description': 'Ez a szervezet készségeihez tartozó API.'
            }
        ]

        # API-k hozzáadása az adatbázishoz
        for api_data in apis:
            api, created = API.objects.get_or_create(
                name=api_data['name'],
                defaults={
                    'url': api_data['url'],
                    'description': api_data['description']
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"API létrehozva: {api.name}"))
            else:
                self.stdout.write(self.style.WARNING(f"API már létezik: {api.name}"))

        self.stdout.write(self.style.SUCCESS('API-k feltöltése befejeződött.'))
