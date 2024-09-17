# adan/management/commands/load_types.py

from django.core.management.base import BaseCommand
from adan.models import Type

class Command(BaseCommand):
    help = 'Alapértelmezett típusok betöltése a Type modellbe'

    def handle(self, *args, **kwargs):
        types = [
            {"name": "OpenAI GPT 3.5", "value": "gpt-3.5"},
            {"name": "OpenAI GPT 3.5t", "value": "gpt-3.5-turbo"},
            {"name": "OpenAI GPT 4", "value": "gpt-4"},
            {"name": "OpenAI GPT 4t", "value": "gpt-4-turbo"},
            {"name": "OpenAI GPT 4m", "value": "gpt-4o-mini"},
        ]

        for type_data in types:
            type_instance, created = Type.objects.get_or_create(
                name=type_data['name'],
                defaults={'value': type_data['value']}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Sikeresen létrehozva: {type_instance}'))
            else:
                self.stdout.write(self.style.WARNING(f'Már létezik: {type_instance}'))
