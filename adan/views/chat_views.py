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
            """ logger.info("Sending data to OpenAI API: %s", messages) """

            # OpenAI API hívása a felhasználói üzenettel
            client = openai.Client()
            response = client.chat.completions.create(
                model="gpt-4o-2024-08-06",
                messages=messages
            )

            response_text = response.choices[0].message.content.strip()
            logger.info("Response from OpenAI: %s", response_text)

            return JsonResponse({'response': response_text})
        except Exception as e:
            logger.error("Error processing request: %s", str(e))
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Hibás kérés'}, status=400)

from django.http import StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
import openai
import json
import logging

# Inicializálj egy logger-t
logger = logging.getLogger(__name__)

@csrf_exempt
def adan_service_call(request):
    """
    OpenAI API lekérdezés végpont, amely adatot és promptot fogad.
    A prompt alapján dolgozza fel az adatot, és választ generál.
    Az eredmény streamelve kerül vissza.
    """
    if request.method == 'POST':
        try:
            # Kérési adatok beolvasása
            data = json.loads(request.body)
            prompt = data.get('prompt')
            extra_data = data.get('data')

            # Naplózzuk a beérkező adatokat
            logger.info("Received prompt: %s", prompt)
            logger.info("Received data: %s", extra_data)

            # Az OpenAI API-nak küldendő üzenet létrehozása
            messages = [
                {"role": "system", "content": f"Extra data: {json.dumps(extra_data)}"},
                {"role": "user", "content": prompt}
            ]

            # Válasz generálása streameléssel az OpenAI API segítségével
            def event_stream():
                client = openai.Client()
                response = client.chat.completions.create(
                    model="gpt-4o-2024-08-06",  # GPT-4 modell használata
                    messages=messages,
                    stream=True  # Engedélyezzük a streamelést
                )

                # Streameljük a beérkező adatokat, darabonként
                for chunk in response:
                    chunk_message = chunk['choices'][0]['delta'].get('content', '')
                    if chunk_message:
                        logger.info("Streaming chunk: %s", chunk_message)
                        yield f"{chunk_message}"

            # A streameléshez StreamingHttpResponse használata
            return StreamingHttpResponse(event_stream(), content_type='text/plain')

        except Exception as e:
            # Hibakezelés és naplózás
            logger.error("Error processing request: %s", str(e))
            return JsonResponse({'error': str(e)}, status=500)

    # Hibás kérés esetén válasz
    return JsonResponse({'error': 'Hibás kérés'}, status=400)
