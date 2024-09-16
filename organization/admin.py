# file: organization/admin.py

from django.contrib import admin
from .models import Company, Team, Squad, Position, Employee, Skill

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    """Adminisztrátor nézet a Vállalat modellekhez."""
    list_display = ('name', 'description')
    search_fields = ('name', 'description')

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    """Adminisztrátor nézet a Csapat modellekhez."""
    list_display = ('name', 'company', 'description')
    search_fields = ('name', 'description')
    list_filter = ('company',)

@admin.register(Squad)
class SquadAdmin(admin.ModelAdmin):
    """Adminisztrátor nézet a Squad modellekhez."""
    list_display = ('name', 'team', 'description')
    search_fields = ('name', 'description')
    list_filter = ('team',)

@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    """Adminisztrátor nézet a Pozíció modellekhez."""
    list_display = ('name', 'description')
    search_fields = ('name', 'description')

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    """Adminisztrátor nézet a Kolléga modellekhez."""
    list_display = ('name', 'squad', 'position')
    search_fields = ('name',)
    list_filter = ('squad', 'position')

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    """Adminisztrátor nézet a Készség modellekhez."""
    list_display = ('name', 'level', 'employee')
    search_fields = ('name', 'employee__name')
    list_filter = ('employee',)
