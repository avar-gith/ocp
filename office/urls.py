# file: office/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EmailViewSet, WikiPageViewSet, office_view, generate_events_view
from . import views

# Router létrehozása az API nézetekhez
router = DefaultRouter()
router.register(r'emails', EmailViewSet)
router.register(r'wikipages', WikiPageViewSet)

urlpatterns = [
    path('', include(router.urls)),  # API URL-ek
    path('mail/', office_view, name='office'),  # Iroda nézet
    path('generate-events/', generate_events_view, name='generate_events'),  # Események generálása
    path('organization-chart/', views.organization_chart, name='organization_chart'),
    path('jira/', views.jira_view, name='jira_view'),
]
