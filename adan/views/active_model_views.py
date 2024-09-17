# file: adan/views/active_model_views.py

from django.shortcuts import render
from rest_framework import generics
from ..models import Model
from ..serializers import ModelSerializer

# Nézet az aktív modellek listázásához
class ActiveModelListView(generics.ListAPIView):
    queryset = Model.objects.filter(is_active=True)  # Csak az aktív modellek
    serializer_class = ModelSerializer

def adan_view(request):
    """
    Adan oldal betöltése. A nézet visszatéríti az 'adan.html' sablont, 
    amely az alkalmazás alapértelmezett szövegét tartalmazza.
    """
    return render(request, 'adan/adan.html')
