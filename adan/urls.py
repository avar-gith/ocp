#file: adan/urls.py

from django.urls import path
from . import views

# URL-ek definiálása az 'Adan' alkalmazáshoz
# Az 'adan/' útvonal az adan_view nézethez kapcsolódik
urlpatterns = [
    path('', views.adan_view, name='adan_view'),  # 'Adan' oldal elérési útvonala
]
