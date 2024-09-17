# file: adan/views/token_views.py

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
import json
import uuid
from datetime import datetime
import logging
from .storage import data_store, token_expiry_time 

# Inicializálj egy logger-t
logger = logging.getLogger(__name__)

@csrf_exempt
def generate_token(request):
    """
    Token generálása és a Jira API-ról, valamint az Organization API-ról lekérdezett projektek tárolása a tokenhez.
    """
    if request.method == 'POST':
        try:
            # API végpontok definiálása
            api_endpoints = [
                "http://localhost:8000/api/jira/projects/",

            ]

            # Lekérdezések és adatok gyűjtése
            all_data = {}
            for url in api_endpoints:
                response = requests.get(url)
                if response.status_code == 200:
                    all_data[url] = response.json()
                else:
                    logger.error(f"Hiba a következő API hívásnál: {url}, Státusz: {response.status_code}")
                    return JsonResponse({'error': f'Nem sikerült lekérdezni az adatokat: {url}'}, status=500)

            # Egyedi token generálása
            token = str(uuid.uuid4())
            expiry_time = datetime.now() + token_expiry_time

            # A tokenhez hozzárendeljük az összes lekérdezett adatot és a lejárati időt
            data_store[token] = {
                'data': all_data,
                'expires_at': expiry_time
            }

            # Naplózzuk a lekérdezett adatokat
            logger.info("Token generálva: %s, lejárati idő: %s", token, expiry_time)

            return JsonResponse({'token': token, 'data': all_data, 'message': 'Token sikeresen generálva az adatokkal.'})
        except Exception as e:
            logger.error("Error generating token: %s", str(e))
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Hibás kérés'}, status=400)


"""             "http://localhost:8000/api/jira/tasks/",
                "http://localhost:8000/api/organization/employees/",
                "http://localhost:8000/api/organization/teams/",
                "http://localhost:8000/api/organization/skills/",
                "http://localhost:8000/api/organization/positions/",
                "http://localhost:8000/api/organization/squads/",
                "http://localhost:8000/api/jira/stories/" """
