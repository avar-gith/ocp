# file: jira/urls.py

from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, StoryViewSet, TaskViewSet

router = DefaultRouter()
router.register(r'projects', ProjectViewSet)
router.register(r'stories', StoryViewSet)
router.register(r'tasks', TaskViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
