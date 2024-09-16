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

#file: adan/views.py
import openai
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# OpenAI API kulcs beállítása a settings.py-ból
openai.api_key = settings.OPENAI_API_KEY

@csrf_exempt
def adan_chat_api(request):
    """
    API végpont az OpenAI GPT-4 modell hívására.
    Ez a nézet fogadja a felhasználói promptot POST kérésként,
    majd az OpenAI API segítségével válaszol egy teljes válasszal.
    """
    if request.method == 'POST':
        try:
            # Kérésből származó adat
            data = json.loads(request.body)
            user_message = data.get('prompt')

            # OpenAI API hívása a teljes válasszal (nem streamelve)
            client = openai.Client()

            response = client.chat.completions.create(
                model="gpt-3.5-turbo",  # Vagy gpt-4
                messages=[
                    {"role": "system", "content": "Adan vagyok, az Elemző. Azért vagyok itt, hogy segítsek az AI üzleti használatában."},
                    {"role": "user", "content": user_message}
                ]
            )

            # A modell válaszának kinyerése helyes módon
            response_text = response.choices[0].message.content.strip()

            # Válasz visszaküldése a frontendnek
            return JsonResponse({'response': response_text})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=400)
