# file: adan/views/api_views.py

from django.shortcuts import render
from rest_framework import viewsets
from ..models import API, Type, Personality, LearningPath
from ..serializers import APISerializer, TypeSerializer, PersonalitySerializer, LearningPathSerializer

def api_list_view(request):
    """
    Ez a nézet megjeleníti az összes API-t a /api/ útvonalon.
    """
    apis = API.objects.all()
    return render(request, 'adan/api_list.html', {'apis': apis})

class APISViewSet(viewsets.ModelViewSet):
    queryset = API.objects.all()
    serializer_class = APISerializer


class TypeViewSet(viewsets.ModelViewSet):
    queryset = Type.objects.all()
    serializer_class = TypeSerializer

class PersonalityViewSet(viewsets.ModelViewSet):
    queryset = Personality.objects.all()
    serializer_class = PersonalitySerializer

class LearningPathViewSet(viewsets.ModelViewSet):
    queryset = LearningPath.objects.all()
    serializer_class = LearningPathSerializer
