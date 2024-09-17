# file: office/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EmailViewSet, WikiPageViewSet, office_view, organization_chart_view


router = DefaultRouter()
router.register(r'emails', EmailViewSet)
router.register(r'wikipages', WikiPageViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('mail/', office_view, name='office'),
    path('organization-chart/', organization_chart_view, name='organization_chart'),
]
