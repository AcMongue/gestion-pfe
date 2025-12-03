from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import FileExtensionValidator
from users.models import User
from projects.models import Project


class Message(models.Model):
    """Modèle représentant un message entre utilisateurs."""
    
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages', verbose_name=_('expéditeur'))
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages', verbose_name=_('destinataire'))
    subject = models.CharField(_('sujet'), max_length=200)
    content = models.TextField(_('contenu'))
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, related_name='messages', null=True, blank=True, verbose_name=_('projet'))
    attachment = models.FileField(_('pièce jointe'), upload_to='messages/attachments/', null=True, blank=True)
    is_read = models.BooleanField(_('lu'), default=False)
    read_at = models.DateTimeField(_('lu le'), null=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, related_name='replies', null=True, blank=True, verbose_name=_('en réponse à'))
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _('message')
        verbose_name_plural = _('messages')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.sender.get_full_name()} → {self.recipient.get_full_name()}: {self.subject}"


class Notification(models.Model):
    """Modèle représentant une notification système."""
    
    TYPE_CHOICES = [
        ('application', 'Candidature'),
        ('application_status', 'Statut de candidature'),
        ('project', 'Projet'),
        ('milestone', 'Jalon'),
        ('deliverable', 'Livrable'),
        ('message', 'Message'),
        ('defense', 'Soutenance'),
        ('general', 'Général'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications', verbose_name=_('utilisateur'))
    type = models.CharField(_('type'), max_length=30, choices=TYPE_CHOICES)
    title = models.CharField(_('titre'), max_length=200)
    message = models.TextField(_('message'))
    link = models.CharField(_('lien'), max_length=500, blank=True)
    is_read = models.BooleanField(_('lu'), default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _('notification')
        verbose_name_plural = _('notifications')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.title}"
