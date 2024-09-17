# file: adan/views/chat_views.py

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import openai
import json
from datetime import datetime
import logging
from .storage import data_store 

# Inicializálj egy logger-t
logger = logging.getLogger(__name__)

@csrf_exempt
def adan_chat_api(request):
    """
    Chat API végpont, amely a token alapján dolgozza fel az adatokat.
    Ha nincs token vagy adat, akkor alapértelmezett válasz működik.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('prompt')
            token = data.get('token')

            logger.info("Received message: %s", user_message)
            logger.info("Received token: %s", token)

            stored_data = ""
            if token:
                token_data = data_store.get(token)
                if token_data and token_data['expires_at'] > datetime.now():
                    stored_data = token_data['data']
                else:
                    stored_data = "Nincs érvényes adat."

            # Naplózzuk a küldött adatokat az API-nak
            messages = [
                {"role": "system", "content": f"Adatok: {json.dumps(stored_data)}"},
                {"role": "user", "content": user_message}
            ]
            logger.info("Sending data to OpenAI API: %s", messages)

            # OpenAI API hívása a felhasználói üzenettel
            client = openai.Client()
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages
            )

            response_text = response.choices[0].message.content.strip()
            logger.info("Response from OpenAI: %s", response_text)

            return JsonResponse({'response': response_text})
        except Exception as e:
            logger.error("Error processing request: %s", str(e))
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Hibás kérés'}, status=400)
