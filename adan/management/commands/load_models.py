# adan/management/commands/load_models.py

from django.core.management.base import BaseCommand
from adan.models import Model, Type, Personality, LearningPath

class Command(BaseCommand):
    help = 'Alapértelmezett modellek betöltése a Model modellbe'

    def handle(self, *args, **kwargs):
        # Keresd meg az első elemeket a Type és LearningPath modellekből
        default_type = Type.objects.first()

     # Ellenőrizd, hogy a szükséges elemek léteznek-e
        if not default_type:
            self.stdout.write(self.style.ERROR('A szükséges alapmodell (Type) nem található!'))
            return

        # Modell létrehozása
        model_instance, created = Model.objects.get_or_create(
            name="Alapmodell",
            defaults={
                'type': default_type,
                'is_active': True  # Alapértelmezett állapot
            }
        )

        if created:
            self.stdout.write(self.style.SUCCESS(f'Sikeresen létrehozva: {model_instance}'))
        else:
            self.stdout.write(self.style.WARNING(f'Már létezik: {model_instance}'))
