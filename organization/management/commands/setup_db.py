# file: organization/management/commands/setup_db.py

from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.contrib.auth.models import User
import os

class Command(BaseCommand):
    help = 'Törli az adatbázist, alkalmazza a migrációkat, létrehoz egy admin felhasználót, és importálja az adatokat.'

    def handle(self, *args, **options):
        # Töröljük a SQLite adatbázis fájlt
        if os.path.exists('db.sqlite3'):
            os.remove('db.sqlite3')
            self.stdout.write(self.style.SUCCESS('Adatbázis fájl törölve.'))

        # Töröljük az organization alkalmazás migrációs fájljait
        org_migrations_folder = 'organization/migrations'
        if os.path.exists(org_migrations_folder):
            for file in os.listdir(org_migrations_folder):
                if file.endswith('.py') and file != '__init__.py':
                    os.remove(os.path.join(org_migrations_folder, file))
                    self.stdout.write(self.style.SUCCESS(f'Organization migrációs fájl törölve: {file}'))

        # Töröljük a jira alkalmazás migrációs fájljait
        jira_migrations_folder = 'jira/migrations'
        if os.path.exists(jira_migrations_folder):
            for file in os.listdir(jira_migrations_folder):
                if file.endswith('.py') and file != '__init__.py':
                    os.remove(os.path.join(jira_migrations_folder, file))
                    self.stdout.write(self.style.SUCCESS(f'Jira migrációs fájl törölve: {file}'))

        # Előkészítjük a migrációkat
        call_command('makemigrations')
        self.stdout.write(self.style.SUCCESS('Migrációk előkészítve.'))

        # Alkalmazzuk a migrációkat
        call_command('migrate')
        self.stdout.write(self.style.SUCCESS('Migrációk alkalmazva.'))

        # Létrehozunk egy admin felhasználót
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(username='admin', email='admin@example.com', password='admin')
            self.stdout.write(self.style.SUCCESS('Admin felhasználó létrehozva.'))
        else:
            self.stdout.write(self.style.SUCCESS('Admin felhasználó már létezik.'))

        # Importáljuk az adatokat
        try:
            call_command('import_data')
            self.stdout.write(self.style.SUCCESS('Adatok sikeresen importálva.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Az adatok importálása hiba történt: {e}'))
