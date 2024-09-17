# file: jira/management/commands/generate_random_sprint.py

import random
from django.core.management.base import BaseCommand
from jira.models import Story, Sprint
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Generál egy véletlenszerű sprintet egy nyitott történethez és elmenti az adatbázisba.'

    def handle(self, *args, **options):
        # Nyitott történetek keresése
        stories = Story.objects.filter(status='new')
        if not stories:
            self.stderr.write(self.style.ERROR('Nincs nyitott történet.'))
            return

        available_stories = []

        for story in stories:
            # Ellenőrizzük, hogy volt-e már sprint az utolsó 7 napon belül
            last_sprint = Sprint.objects.filter(story=story).order_by('-created_at').first()
            if last_sprint:
                if (datetime.now().date() - last_sprint.created_at).days >= 7:
                    available_stories.append(story)
            else:
                available_stories.append(story)

        if not available_stories:
            self.stderr.write(self.style.ERROR('Nincs elérhető történet új sprint létrehozásához.'))
            return

        # Véletlenszerű történet kiválasztása
        selected_story = random.choice(available_stories)

        # Új sprint létrehozása
        new_sprint = Sprint(
            story=selected_story,
            created_at=datetime.now().date()
        )
        new_sprint.save()

        self.stdout.write(self.style.SUCCESS('Random sprint sikeresen generálva és elmentve az adatbázisba.'))
