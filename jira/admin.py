# file: jira/admin.py

from django.contrib import admin
from .models import Project, Story, Task

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'start_date', 'end_date', 'deadline', 'creator', 'responsible')
    search_fields = ('name', 'description')
    list_filter = ('status', 'creator', 'responsible')

@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'project', 'status', 'creation_date', 'deadline', 'creator', 'responsible')
    search_fields = ('name', 'description')
    list_filter = ('status', 'project', 'creator', 'responsible')

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'project', 'story', 'status', 'creation_date', 'deadline', 'creator', 'responsible')
    search_fields = ('name', 'description')
    list_filter = ('status', 'project', 'story', 'creator', 'responsible')
