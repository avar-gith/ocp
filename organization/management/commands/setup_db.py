# file: organization/management/commands/setup_db.py

from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.contrib.auth.models import User
import os

class Command(BaseCommand):
    help = 'Törli az adatbázist, alkalmazza a migrációkat, és létrehoz egy admin felhasználót'

    def handle(self, *args, **options):
        # Töröljük a SQLite adatbázis fájlt és a migrációs fájlokat
        if os.path.exists('db.sqlite3'):
            os.remove('db.sqlite3')
            self.stdout.write(self.style.SUCCESS('Adatbázis fájl törölve.'))

        migrations_folder = 'organization/migrations'
        if os.path.exists(migrations_folder):
            for file in os.listdir(migrations_folder):
                if file.endswith('.py') and file != '__init__.py':
                    os.remove(os.path.join(migrations_folder, file))
                    self.stdout.write(self.style.SUCCESS(f'Migrációs fájl törölve: {file}'))

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
