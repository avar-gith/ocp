# file: organization/urls.py

from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import CompanyViewSet, TeamViewSet, SquadViewSet, PositionViewSet, EmployeeViewSet, SkillViewSet
from office.views import generate_events_view

router = DefaultRouter()
router.register(r'companies', CompanyViewSet)
router.register(r'teams', TeamViewSet)
router.register(r'squads', SquadViewSet)
router.register(r'positions', PositionViewSet)
router.register(r'employees', EmployeeViewSet)
router.register(r'skills', SkillViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('generate-events/', generate_events_view, name='generate_events'),
]
