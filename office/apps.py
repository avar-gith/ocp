# file: office/apps.py

from django.apps import AppConfig

class OfficeConfig(AppConfig):
    name = 'office'

    def ready(self):
        import office.signals  # Jelentse be a signals.py fájl importálását
