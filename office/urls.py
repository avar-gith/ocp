# file: office/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EmailViewSet, WikiPageViewSet, office_view, organization_chart_view, generate_events_view

# Router létrehozása az API nézetekhez
router = DefaultRouter()
router.register(r'emails', EmailViewSet)
router.register(r'wikipages', WikiPageViewSet)

urlpatterns = [
    path('', include(router.urls)),  # API URL-ek
    path('mail/', office_view, name='office'),  # Iroda nézet
    path('organization-chart/', organization_chart_view, name='organization_chart'),  # Szervezeti diagram
    path('generate-events/', generate_events_view, name='generate_events'),  # Események generálása
]
