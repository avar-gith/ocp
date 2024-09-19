# file: jira/serializers.py

from rest_framework import serializers
from .models import Project, Story, Task

class ProjectSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'status', 'status_display', 'start_date', 'end_date', 'deadline', 'creator', 'responsible']

class StorySerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Story
        fields = ['id', 'name', 'description', 'status', 'status_display', 'creation_date', 'deadline', 'creator', 'responsible', 'project']

class TaskSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'name', 'description', 'status', 'status_display', 'creation_date', 'deadline', 'creator', 'responsible', 'project', 'story']
