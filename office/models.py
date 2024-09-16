# file: office/models.py

from django.db import models
from django.utils import timezone
from organization.models import Employee

class Email(models.Model):
    """
    Modell az e-mailek tárolására.
    """
    sender = models.ForeignKey(
        Employee, 
        on_delete=models.CASCADE, 
        related_name='sent_emails',
        verbose_name='Küldő'
    )
    sent_at = models.DateTimeField(
        default=timezone.now,
        verbose_name='Küldés időpontja'
    )
    content = models.TextField(
        verbose_name='Tartalom'
    )

    def __str__(self):
        """
        Az e-mail szöveges reprezentációja.
        """
        return f'Email from {self.sender} at {self.sent_at}'
    
    class Meta:
        verbose_name = 'Mail'
        verbose_name_plural = 'Mailek'
        ordering = ['-sent_at']

class WikiPage(models.Model):
    """
    Modell a wiki oldalak tárolására.
    """
    title = models.CharField(
        max_length=255, 
        unique=True,
        verbose_name='Cím'
    )
    description = models.TextField(
        verbose_name='Leírás'
    )
    created_by = models.ForeignKey(
        Employee, 
        on_delete=models.CASCADE, 
        related_name='created_pages',
        verbose_name='Készítő'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Létrehozás időpontja'
    )

    def __str__(self):
        """
        A wiki oldal szöveges reprezentációja.
        """
        return self.title
    
    class Meta:
        verbose_name = 'Wiki oldal'
        verbose_name_plural = 'Wiki oldalak'
        ordering = ['-created_at']
