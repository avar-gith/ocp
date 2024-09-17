# file: adan/urls.py
from django.urls import path
from . import views

# URL-ek definiálása az 'Adan' alkalmazáshoz
urlpatterns = [
    path('', views.adan_view, name='adan_view'),  # Adan oldal megjelenítése
    path('chat/', views.adan_chat_api, name='adan_chat_api'),  # Chat API végpont
    path('generate-token/', views.generate_token, name='generate_token'),  # Token generálás végpont
]
