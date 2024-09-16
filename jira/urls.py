# file: jira/urls.py

from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, StoryViewSet, TaskViewSet, create_sprint

router = DefaultRouter()
router.register(r'projects', ProjectViewSet)
router.register(r'stories', StoryViewSet)
router.register(r'tasks', TaskViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('create_sprint/<int:story_id>/', create_sprint, name='create_sprint'),  # Új URL minta a sprint létrehozásához
]
