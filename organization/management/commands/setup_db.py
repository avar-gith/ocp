# file: organization/management/commands/setup_db.py

from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.contrib.auth.models import User
import os
import time

class Command(BaseCommand):
    help = 'Törli az adatbázist, alkalmazza a migrációkat, létrehoz egy admin felhasználót, és importálja az adatokat.'

    def handle(self, *args, **options):
        # Töröljük a SQLite adatbázis fájlt
        if os.path.exists('db.sqlite3'):
            os.remove('db.sqlite3')
            self.stdout.write(self.style.SUCCESS('Adatbázis fájl törölve.'))

        # Töröljük az organization alkalmazás migrációs fájljait
        self.remove_migrations('organization/migrations')

        # Töröljük a jira alkalmazás migrációs fájljait
        self.remove_migrations('jira/migrations')

        # Töröljük az office alkalmazás migrációs fájljait
        self.remove_migrations('office/migrations')

        # Töröljük az adan alkalmazás migrációs fájljait
        self.remove_migrations('adan/migrations')

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

        # Várakozás az import_projects parancs előtt
        time.sleep(2)  # Várakozás, ha szükséges

        # Projektek importálása
        try:
            call_command('import_projects')
            self.stdout.write(self.style.SUCCESS('Projektek sikeresen importálva.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Hiba történt a projektek importálásakor: {e}'))

        # Várakozás az import_tasks parancs előtt
        time.sleep(2)  # Várakozás, ha szükséges

        # Feladatok importálása
        try:
            call_command('import_tasks')
            self.stdout.write(self.style.SUCCESS('Feladatok sikeresen importálva.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Hiba történt a feladatok importálásakor: {e}'))

        # Várakozás az adan parancsok előtt
        time.sleep(4)  # Várakozás, ha szükséges

        # API-k betöltése
        try:
            call_command('load_apis')
            self.stdout.write(self.style.SUCCESS('API-k sikeresen betöltve.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Hiba történt az API-k betöltésekor: {e}'))
        time.sleep(1)

        # Típusok betöltése
        try:
            call_command('load_types')
            self.stdout.write(self.style.SUCCESS('Típusok sikeresen betöltve.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Hiba történt a típusok betöltésekor: {e}'))
        time.sleep(1)

        # Személyiségek betöltése
        try:
            call_command('load_personalities')
            self.stdout.write(self.style.SUCCESS('Személyiségek sikeresen betöltve.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Hiba történt a személyiségek betöltésekor: {e}'))
        time.sleep(1)

        # Tanulási utak betöltése
        try:
            call_command('load_learning_paths')
            self.stdout.write(self.style.SUCCESS('Tanulási utak sikeresen betöltve.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Hiba történt a tanulási utak betöltésekor: {e}'))
        time.sleep(1)

        # Modellek betöltése
        try:
            call_command('load_models')
            self.stdout.write(self.style.SUCCESS('Modellek sikeresen betöltve.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Hiba történt a modellek betöltésekor: {e}'))

    def remove_migrations(self, folder):
        """
        Törli a migrációs fájlokat a megadott mappából.
        """
        if os.path.exists(folder):
            for file in os.listdir(folder):
                if file.endswith('.py') and file != '__init__.py':
                    os.remove(os.path.join(folder, file))
                    self.stdout.write(self.style.SUCCESS(f'Migrációs fájl törölve: {file}'))
