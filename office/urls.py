# file: office/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EmailViewSet, WikiPageViewSet

router = DefaultRouter()
router.register(r'emails', EmailViewSet)
router.register(r'wikipages', WikiPageViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
