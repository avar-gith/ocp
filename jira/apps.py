# file: jira/apps.py

from django.apps import AppConfig

class JiraConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'jira'

    def ready(self):
        import jira.signals  # Importáljuk a signals.py fájlt
