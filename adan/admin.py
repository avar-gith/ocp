# file: adan/admin.py

from django.contrib import admin
from django.utils.html import format_html
from .models import Model, Type, Personality, LearningPath, API

# Egyedi admin osztály a Model adminisztrációhoz
@admin.register(Model)
class ModelAdmin(admin.ModelAdmin):
    # Megjelenítendő oszlopok az admin felületen
    list_display = ('name', 'type', 'personality', 'learning_path', 'is_active_display')
    # Keresés a Modell neve alapján
    search_fields = ('name',)
    # API-k kezelése a Model admin felületen
    filter_horizontal = ('apis',)
    # Adminisztrációs műveletek hozzáadása
    actions = ['make_active']

    def is_active_display(self, obj):
        """
        Színes kiemelés az aktív Modellnél
        """
        if obj.is_active:
            # Ha aktív, zöld színnel emeljük ki
            return format_html('<span style="color: green; font-weight: bold;">Aktív</span>')
        return format_html('<span style="color: gray;">Nem aktív</span>')

    is_active_display.short_description = 'Aktív állapot'  # Megjelenített oszlopnév

    def get_queryset(self, request):
        """
        A queryset módosítása, hogy az aktív Modell mindig elöl legyen
        és a többi ABC sorrendben kövesse
        """
        qs = super().get_queryset(request)
        # Az aktív Modellt tesszük az első helyre, a többit ABC sorrendben jelenítjük meg
        return qs.order_by('-is_active', 'name')

    # Egyedi admin művelet a Modell aktiválására
    def make_active(self, request, queryset):
        """
        A kiválasztott Modell aktívra állítása.
        Egyszerre csak egy Modell lehet aktív.
        """
        if queryset.count() > 1:
            # Figyelmeztetés, ha több Modellt választottak ki
            self.message_user(request, "Egyszerre csak egy Modellt aktiválhatsz.", level='error')
            return
        
        # Először minden más Modellt deaktiválunk
        Model.objects.filter(is_active=True).update(is_active=False)
        # A kiválasztott egy Modellt aktívra állítjuk
        queryset.update(is_active=True)
        self.message_user(request, "A kiválasztott Modell sikeresen aktiválva lett.")
    
    make_active.short_description = "Kiválasztott Modell aktiválása"

# API adminisztráció hozzáadása
@admin.register(API)
class APIAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'description')  # API adatainak megjelenítése
    search_fields = ('name', 'url')  # Kereshető mezők

# A többi Modell adminisztrációja
admin.site.register(Type)
admin.site.register(Personality)
admin.site.register(LearningPath)
