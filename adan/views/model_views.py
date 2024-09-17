# file: adan/views/model_views.py

from rest_framework import viewsets
from ..models import Model
from ..serializers import ModelSerializer

# ModelViewSet a modellek kezeléséhez
class ModelViewSet(viewsets.ModelViewSet):
    queryset = Model.objects.all()
    serializer_class = ModelSerializer
