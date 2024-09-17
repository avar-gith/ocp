# file: jira/admin.py

from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Project, Story, Task, Sprint, TaskStatus
from django.utils import timezone

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'start_date', 'deadline', 'creator', 'responsible')
    search_fields = ('name', 'description')
    list_filter = ('status', 'creator', 'responsible')

@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'project', 'status', 'creation_date', 'deadline', 'creator', 'responsible')
    search_fields = ('name', 'description')
    list_filter = ('status', 'project', 'creator', 'responsible')
    actions = ['create_sprint']

    def create_sprint(self, request, queryset):
        """
        Létrehozza a sprintet a kiválasztott történetekhez.
        """
        for story in queryset:
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
        
        self.message_user(request, "Sprint(ek) sikeresen létrehozva.")
    create_sprint.short_description = "Sprint létrehozása kiválasztott történetekhez"

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'project', 'story', 'status', 'creation_date', 'deadline', 'creator', 'responsible')
    search_fields = ('name', 'description')
    list_filter = ('status', 'project', 'story', 'creator', 'responsible')

@admin.register(Sprint)
class SprintAdmin(admin.ModelAdmin):
    list_display = ('name', 'story', 'created_at')
    search_fields = ('name',)
    list_filter = ('story', 'created_at')

@admin.register(TaskStatus)
class TaskStatusAdmin(admin.ModelAdmin):
    list_display = ('sprint', 'task', 'status')
    search_fields = ('task__name',)
    list_filter = ('sprint', 'status')
