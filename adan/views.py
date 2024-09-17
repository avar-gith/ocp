#file: adan/views.py

from django.shortcuts import render

# Nézet a 'Adan' oldal megjelenítésére
# Ez a nézet rendereli az 'adan.html' sablont, amely az alapértelmezett szöveget tartalmazza
def adan_view(request):
    """
    Adan oldal betöltése. A nézet visszatéríti az 'adan.html' sablont, 
    amely az alkalmazás alapértelmezett szövegét tartalmazza.
    """
    return render(request, 'adan/adan.html')

import openai
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import uuid
from datetime import datetime, timedelta
import requests  # Ezzel hívjuk a Jira API-t

# OpenAI API kulcs beállítása a settings.py-ból
openai.api_key = settings.OPENAI_API_KEY

# Token alapú adat tárolás
data_store = {}
token_expiry_time = timedelta(hours=1)  # Token érvényességi ideje

@csrf_exempt
def generate_token(request):
    """
    Token generálása és a Jira API-ról lekérdezett projektek tárolása a tokenhez.
    """
    if request.method == 'POST':
        try:
            # Jira API lekérdezés
            jira_api_url = "http://localhost:8000/api/jira/projects/"  # Használd a megfelelő URL-t
            jira_response = requests.get(jira_api_url)

            # Ellenőrizzük, hogy sikerült-e lekérdezni az adatokat
            if jira_response.status_code == 200:
                jira_projects = jira_response.json()  # Feltételezzük, hogy az API JSON formátumban válaszol
            else:
                return JsonResponse({'error': 'Nem sikerült lekérdezni a Jira projekteket.'}, status=500)

            # Egyedi token generálása
            token = str(uuid.uuid4())
            expiry_time = datetime.now() + token_expiry_time

            # A tokenhez hozzárendeljük a Jira API-ból lekérdezett adatokat és a lejárati időt
            data_store[token] = {
                'data': jira_projects,  # A Jira projektek adatai
                'expires_at': expiry_time
            }

            return JsonResponse({'token': token, 'message': 'Token sikeresen generálva a Jira projektek adataival.'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Hibás kérés'}, status=400)

@csrf_exempt
def adan_chat_api(request):
    """
    Chat API végpont, amely a token alapján dolgozza fel az adatokat.
    Ha nincs token vagy adat, akkor alapértelmezett válasz működik.
    """
    if request.method == 'POST':
        try:
            # A kérésből érkező felhasználói üzenet és token
            data = json.loads(request.body)
            user_message = data.get('prompt')
            token = data.get('token')

            # Alapértelmezett válasz, ha nincs token
            stored_data = ""

            # Ha van token, próbáljuk meg lekérni a tokenhez tartozó adatokat
            if token:
                token_data = data_store.get(token)
                if token_data and token_data['expires_at'] > datetime.now():
                    stored_data = token_data['data']  # A tokenhez tartozó adat lekérése
                else:
                    stored_data = "Nincs érvényes adat."  # Token lejárt vagy nem érvényes

            # OpenAI API hívása a felhasználói üzenettel és az esetlegesen tárolt adattal
            client = openai.Client()
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",  # Vagy gpt-4
                messages=[
                    {"role": "system", "content": f"Adatok: {json.dumps(stored_data)}"},
                    {"role": "user", "content": user_message}
                ]
            )

            # A modell válaszának kinyerése
            response_text = response.choices[0].message.content.strip()

            # Válasz visszaküldése a frontendnek
            return JsonResponse({'response': response_text})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Hibás kérés'}, status=400)

