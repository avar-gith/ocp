from django.contrib import admin
from .models import Email, WikiPage

@admin.register(Email)
class EmailAdmin(admin.ModelAdmin):
    """
    Adminisztrációs beállítások az Email modellhez.
    """
    # A mezők, amelyek az admin felületen megjelennek
    list_display = ('sender', 'subject', 'sent_at', 'content_preview')
    
    # Kereshető mezők az admin felületen
    search_fields = ('sender__name', 'subject', 'content')
    
    # Alapértelmezett rendezési sorrend
    ordering = ('-sent_at', 'subject')
    
    # Szűrők az oldalsávban
    list_filter = ('sender', 'sent_at', 'subject')
    
    # Formázott mezők a részletező oldalon
    fields = ('sender', 'subject', 'sent_at', 'content')
    
    # A mezők, amelyeket szerkesztés közben szerkeszthetővé teszünk
    readonly_fields = ('sent_at',)
    
    def content_preview(self, obj):
        """
        Tartalom előnézete az admin felületen.
        Csak az első 50 karakter jelenik meg, ha a tartalom hosszabb.
        """
        return obj.content[:50] + ('...' if len(obj.content) > 50 else '')
    content_preview.short_description = 'Tartalom előnézete'

@admin.register(WikiPage)
class WikiPageAdmin(admin.ModelAdmin):
    """
    Adminisztrációs beállítások a WikiPage modellhez.
    """
    # A mezők, amelyek az admin felületen megjelennek
    list_display = ('title', 'created_by', 'created_at')  # 'subject' eltávolítva
    
    # Kereshető mezők az admin felületen
    search_fields = ('title', 'description')  # 'subject' eltávolítva
    
    # Alapértelmezett rendezési sorrend
    ordering = ('-created_at',)  # 'subject' eltávolítva
    
    # Szűrők az oldalsávban
    list_filter = ('created_by', 'created_at')  # 'subject' eltávolítva
    
    # Formázott mezők a részletező oldalon
    fields = ('title', 'description', 'created_by', 'created_at')
    
    # A mezők, amelyeket szerkesztés közben szerkeszthetővé teszünk
    readonly_fields = ('created_at',)
