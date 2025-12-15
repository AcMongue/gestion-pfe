# communications/models.py - Extension pour les notifications

from django.db import models
from django.utils import timezone


class Notification(models.Model):
    """
    Modèle pour tracer les notifications envoyées.
    """
    recipients = models.JSONField(
        verbose_name="Destinataires",
        help_text="Liste des emails des destinataires"
    )
    
    subject = models.CharField(
        max_length=200,
        verbose_name="Objet"
    )
    
    sent_at = models.DateTimeField(
        default=timezone.now,
        verbose_name="Envoyé le"
    )
    
    class Meta:
        verbose_name = "Notification email"
        verbose_name_plural = "Notifications email"
        ordering = ['-sent_at']
    
    def __str__(self):
        return f"{self.subject} - {self.sent_at.strftime('%d/%m/%Y %H:%M')}"
