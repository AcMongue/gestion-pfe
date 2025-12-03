from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator, FileExtensionValidator
from django.utils import timezone
from users.models import User
from subjects.models import Assignment


class Project(models.Model):
    """Modèle représentant un projet de PFE en cours."""
    
    STATUS_CHOICES = [
        ('in_progress', 'En cours'),
        ('submitted', 'Soumis'),
        ('under_review', 'En révision'),
        ('approved', 'Approuvé'),
        ('rejected', 'Rejeté'),
        ('completed', 'Terminé'),
    ]
    
    assignment = models.OneToOneField(Assignment, on_delete=models.CASCADE, related_name='project', verbose_name=_('affectation'))
    title = models.CharField(_('titre du projet'), max_length=300)
    description = models.TextField(_('description'))
    objectives = models.TextField(_('objectifs'))
    methodology = models.TextField(_('méthodologie'), blank=True)
    technologies = models.CharField(_('technologies utilisées'), max_length=500, blank=True)
    status = models.CharField(_('statut'), max_length=20, choices=STATUS_CHOICES, default='in_progress')
    progress_percentage = models.PositiveIntegerField(_('pourcentage d\'avancement'), default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    start_date = models.DateField(_('date de début'), default=timezone.now)
    expected_end_date = models.DateField(_('date de fin prévue'), null=True, blank=True)
    actual_end_date = models.DateField(_('date de fin réelle'), null=True, blank=True)
    repository_url = models.URLField(_('URL du dépôt'), blank=True)
    documentation_url = models.URLField(_('URL de la documentation'), blank=True)
    final_report = models.FileField(_('rapport final'), upload_to='projects/reports/', null=True, blank=True)
    presentation = models.FileField(_('présentation'), upload_to='projects/presentations/', null=True, blank=True)
    supervisor_notes = models.TextField(_('notes de l\'encadreur'), blank=True)
    supervisor_rating = models.PositiveIntegerField(_('note de l\'encadreur'), null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(20)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('projet')
        verbose_name_plural = _('projets')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title}"


class Milestone(models.Model):
    """Modèle représentant un jalon/étape du projet."""
    
    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('in_progress', 'En cours'),
        ('completed', 'Complété'),
        ('delayed', 'En retard'),
    ]
    
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='milestones')
    title = models.CharField(_('titre'), max_length=200)
    description = models.TextField(_('description'))
    order = models.PositiveIntegerField(_('ordre'), default=0)
    status = models.CharField(_('statut'), max_length=20, choices=STATUS_CHOICES, default='pending')
    due_date = models.DateField(_('date d\'échéance'))
    completed_date = models.DateField(_('date de complétion'), null=True, blank=True)
    notes = models.TextField(_('notes'), blank=True)
    validated_by_supervisor = models.BooleanField(_('validé'), default=False)
    validation_date = models.DateTimeField(_('date de validation'), null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('jalon')
        verbose_name_plural = _('jalons')
        ordering = ['project', 'order']
    
    def __str__(self):
        return f"{self.title}"


class Deliverable(models.Model):
    """Modèle représentant un livrable/document du projet."""
    
    TYPE_CHOICES = [
        ('report', 'Rapport'),
        ('code', 'Code source'),
        ('documentation', 'Documentation'),
        ('presentation', 'Présentation'),
        ('video', 'Vidéo'),
        ('other', 'Autre'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('submitted', 'Soumis'),
        ('reviewed', 'Révisé'),
        ('approved', 'Approuvé'),
        ('rejected', 'Rejeté'),
    ]
    
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='deliverables')
    milestone = models.ForeignKey(Milestone, on_delete=models.SET_NULL, related_name='deliverables', null=True, blank=True)
    title = models.CharField(_('titre'), max_length=200)
    description = models.TextField(_('description'), blank=True)
    type = models.CharField(_('type'), max_length=20, choices=TYPE_CHOICES, default='report')
    file = models.FileField(_('fichier'), upload_to='projects/deliverables/')
    version = models.CharField(_('version'), max_length=20, default='1.0')
    status = models.CharField(_('statut'), max_length=20, choices=STATUS_CHOICES, default='pending')
    submitted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submitted_deliverables')
    submitted_at = models.DateTimeField(_('soumis le'), auto_now_add=True)
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='reviewed_deliverables', null=True, blank=True)
    reviewed_at = models.DateTimeField(_('révisé le'), null=True, blank=True)
    review_comments = models.TextField(_('commentaires'), blank=True)
    rating = models.PositiveIntegerField(_('note'), null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(20)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('livrable')
        verbose_name_plural = _('livrables')
        ordering = ['-submitted_at']
    
    def __str__(self):
        return f"{self.title} (v{self.version})"


class Comment(models.Model):
    """Modèle représentant un commentaire sur un projet."""
    
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='project_comments')
    content = models.TextField(_('contenu'))
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='replies', null=True, blank=True)
    is_private = models.BooleanField(_('privé'), default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('commentaire')
        verbose_name_plural = _('commentaires')
        ordering = ['created_at']
    
    def __str__(self):
        return f"{self.author.get_full_name()} - {self.created_at.strftime('%Y-%m-%d')}"
