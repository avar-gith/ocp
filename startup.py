# file: startup.py

import os
import django
from django.core.management import call_command
from django.contrib.auth.models import User

def main():
    # Beállítjuk a Django környezetet
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
    django.setup()

    # Töröljük a SQLite adatbázis fájlt és a migrációs fájlokat
    if os.path.exists('db.sqlite3'):
        os.remove('db.sqlite3')
        print("Adatbázis fájl törölve.")

    migrations_folder = 'organization/migrations'
    if os.path.exists(migrations_folder):
        for file in os.listdir(migrations_folder):
            if file.endswith('.py') and file != '__init__.py':
                os.remove(os.path.join(migrations_folder, file))
                print(f"Migrációs fájl törölve: {file}")

    # Előkészítjük a migrációkat
    call_command('makemigrations')
    print("Migrációk előkészítve.")

    # Alkalmazzuk a migrációkat
    call_command('migrate')
    print("Migrációk alkalmazva.")

    # Létrehozunk egy admin felhasználót
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(username='admin', email='admin@example.com', password='admin')
        print("Admin felhasználó létrehozva.")
    else:
        print("Admin felhasználó már létezik.")

if __name__ == '__main__':
    main()
