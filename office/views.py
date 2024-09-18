# file: office/views.py

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Email
from office.serializers import EmailSerializer

class SendMailAPIView(APIView):
    """
    APIView az e-mailek küldésére.
    """
    def post(self, request, *args, **kwargs):
        serializer = EmailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'Email sent'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# file: office/views.py

from rest_framework import viewsets
from .models import Email, WikiPage
from .serializers import EmailSerializer, WikiPageSerializer

class EmailViewSet(viewsets.ModelViewSet):
    """
    ViewSet az e-mailek kezeléséhez.
    """
    queryset = Email.objects.all()
    serializer_class = EmailSerializer

    def create(self, request, *args, **kwargs):
        """
        E-mail küldésének kezelése.
        """
        return super().create(request, *args, **kwargs)

class WikiPageViewSet(viewsets.ModelViewSet):
    """
    ViewSet a wiki oldalak kezeléséhez.
    """
    queryset = WikiPage.objects.all()
    serializer_class = WikiPageSerializer
    
    
# file: office/views.py

from django.shortcuts import render
from .models import Email, WikiPage

def office_view(request):
    """
    Nézet az e-mailek és wiki oldalak megjelenítésére.
    """
    emails = Email.objects.all()  # Minden e-mail lekérése
    wiki_pages = WikiPage.objects.all()  # Minden wiki oldal lekérése
    
    return render(request, 'office/office.html', {
        'emails': emails,
        'wiki_pages': wiki_pages,
    })

def organization_chart_view(request):
    """
    Nézet a szervezeti ábra megjelenítésére.
    """
    return render(request, 'office/organization_chart.html')

# file: office/views.py

from django.http import JsonResponse
from django.core.management import call_command

def generate_events_view(request):
    if request.method == 'POST':
        # Hívjuk meg a szükséges parancsokat
        try:
            call_command('generate_random_project')  # A projekt generálása
            call_command('generate_random_sprint')   # A sprint generálása
            call_command('generate_random_story')    # A történet generálása
            call_command('generate_random_task')     # A feladat generálása

            return JsonResponse({'status': 'success', 'message': 'Események generálva.'})
        except Exception as e:
            return JsonResponse({'status': 'fail', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'fail', 'message': 'Invalid request method.'}, status=400)
