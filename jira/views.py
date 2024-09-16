# file: jira/views.py

from rest_framework import viewsets
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from .models import Project, Story, Task, Sprint, TaskStatus
from .serializers import ProjectSerializer, StorySerializer, TaskSerializer

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

class StoryViewSet(viewsets.ModelViewSet):
    queryset = Story.objects.all()
    serializer_class = StorySerializer

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

def create_sprint(request, story_id):
    """
    Létrehozza a sprintet a kiválasztott történethez, és frissíti a feladatok állapotát.
    """
    story = get_object_or_404(Story, pk=story_id)
    tasks = Task.objects.filter(story=story)

    # Létrehozzuk a sprintet
    sprint = Sprint.objects.create(
        story=story,
        created_at=timezone.now().date()
    )

    # Frissítjük a sprint állapotát
    for task in tasks:
        TaskStatus.objects.get_or_create(
            sprint=sprint,
            task=task,
            defaults={'status': task.status}
        )

    return redirect('admin:jira_sprint_changelist') 
