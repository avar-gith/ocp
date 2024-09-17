# adan/management/commands/load_learning_paths.py

from django.core.management.base import BaseCommand
from adan.models import LearningPath

class Command(BaseCommand):
    help = 'Alapértelmezett tanulási utak betöltése a LearningPath modellbe'

    def handle(self, *args, **kwargs):
        learning_paths = [
            {
                "name": "Matematika",
                "value": "Matematikai alapok és haladó technikák, beleértve az algebra, geometria és kalkulus témákat."
            },
            {
                "name": "Projektmenedzsment",
                "value": "Az alapvető projektmenedzsment technikák és eszközök, mint a Gantt-diagram és a kockázatelemzés."
            },
            {
                "name": "Alapvető elemzés",
                "value": "A statisztikai alapok megértése és az adatok elemzési módszereinek alkalmazása."
            },
            {
                "name": "Emelt szintű elemzés",
                "value": "Haladó statisztikai technikák, mint a regresszió és az időszaki adatelemzés."
            },
            {
                "name": "Üzleti stratégiák",
                "value": "A különböző üzleti stratégiák és modellek, mint a SWOT-analízis és a piackutatás."
            },
            {
                "name": "Időmenedzsment",
                "value": "Hatékony időbeosztás és prioritáskezelés technikái a munka és a magánélet egyensúlyának megteremtésére."
            },
        ]

        for path_data in learning_paths:
            path_instance, created = LearningPath.objects.get_or_create(
                name=path_data['name'],
                defaults={'value': path_data['value']}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Sikeresen létrehozva: {path_instance}'))
            else:
                self.stdout.write(self.style.WARNING(f'Már létezik: {path_instance}'))
