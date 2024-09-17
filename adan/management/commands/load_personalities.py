# adan/management/commands/load_personalities.py

from django.core.management.base import BaseCommand
from adan.models import Personality

class Command(BaseCommand):
    help = 'Alapértelmezett személyiségek betöltése a Personality modellbe'

    def handle(self, *args, **kwargs):
        personalities = [
            {
                "name": "Alapállapot (nincs)",
                "value": "Minden tekintetben az alapmodellnek megfelelően viselkedj."
            },
            {
                "name": "Elemző: Adan - Minimális tanítás",
                "value": "Adan vagy egy barátságos elemző AI."
            },
            {
                "name": "Elemző: Adan",
                "value": "Adan vagy egy barátságos elemző AI. Kiváló matematikai és elemzési képességekkel és funkciókkal felszerelt modell, akinek a feladata, hogy professzionális üzleti elemzés végezzen."
            },
        ]

        for personality_data in personalities:
            personality_instance, created = Personality.objects.get_or_create(
                name=personality_data['name'],
                defaults={'value': personality_data['value']}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Sikeresen létrehozva: {personality_instance}'))
            else:
                self.stdout.write(self.style.WARNING(f'Már létezik: {personality_instance}'))
