from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from users.models import User
from projects.models import Project


class Defense(models.Model):
    """Modèle représentant une soutenance de PFE."""
    
    STATUS_CHOICES = [
        ('scheduled', 'Planifiée'),
        ('in_progress', 'En cours'),
        ('completed', 'Terminée'),
        ('cancelled', 'Annulée'),
        ('rescheduled', 'Reportée'),
    ]
    
    project = models.OneToOneField(Project, on_delete=models.CASCADE, related_name='defense', verbose_name=_('projet'))
    date = models.DateField(_('date'))
    time = models.TimeField(_('heure'))
    duration = models.PositiveIntegerField(_('durée (minutes)'), default=30)
    room = models.CharField(_('salle'), max_length=100)
    building = models.CharField(_('bâtiment'), max_length=100, blank=True)
    status = models.CharField(_('statut'), max_length=20, choices=STATUS_CHOICES, default='scheduled')
    presentation_duration = models.PositiveIntegerField(_('durée présentation (min)'), default=15)
    questions_duration = models.PositiveIntegerField(_('durée questions (min)'), default=15)
    final_grade = models.DecimalField(_('note finale'), max_digits=4, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(20)])
    jury_comments = models.TextField(_('commentaires du jury'), blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('soutenance')
        verbose_name_plural = _('soutenances')
        ordering = ['date', 'time']
    
    def __str__(self):
        return f"{self.project.title} - {self.date} {self.time}"


class JuryMember(models.Model):
    """Modèle représentant un membre du jury pour une soutenance."""
    
    ROLE_CHOICES = [
        ('president', 'Président'),
        ('examiner', 'Examinateur'),
        ('supervisor', 'Encadreur'),
    ]
    
    defense = models.ForeignKey(Defense, on_delete=models.CASCADE, related_name='jury_members', verbose_name=_('soutenance'))
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='jury_assignments', verbose_name=_('membre'))
    role = models.CharField(_('rôle'), max_length=20, choices=ROLE_CHOICES)
    grade = models.DecimalField(_('note'), max_digits=4, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(20)])
    comments = models.TextField(_('commentaires'), blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _('membre du jury')
        verbose_name_plural = _('membres du jury')
        unique_together = ['defense', 'user']
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.get_role_display()}"


class DefenseEvaluation(models.Model):
    """Modèle représentant l'évaluation détaillée d'une soutenance."""
    
    defense = models.OneToOneField(Defense, on_delete=models.CASCADE, related_name='evaluation', verbose_name=_('soutenance'))
    presentation_quality = models.PositiveIntegerField(_('qualité présentation'), validators=[MinValueValidator(0), MaxValueValidator(20)], null=True, blank=True)
    content_mastery = models.PositiveIntegerField(_('maîtrise du contenu'), validators=[MinValueValidator(0), MaxValueValidator(20)], null=True, blank=True)
    technical_skills = models.PositiveIntegerField(_('compétences techniques'), validators=[MinValueValidator(0), MaxValueValidator(20)], null=True, blank=True)
    communication = models.PositiveIntegerField(_('communication'), validators=[MinValueValidator(0), MaxValueValidator(20)], null=True, blank=True)
    answers_quality = models.PositiveIntegerField(_('qualité des réponses'), validators=[MinValueValidator(0), MaxValueValidator(20)], null=True, blank=True)
    overall_impression = models.TextField(_('impression générale'), blank=True)
    strengths = models.TextField(_('points forts'), blank=True)
    weaknesses = models.TextField(_('points à améliorer'), blank=True)
    recommendations = models.TextField(_('recommandations'), blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('évaluation de soutenance')
        verbose_name_plural = _('évaluations de soutenance')
    
    def __str__(self):
        return f"Évaluation - {self.defense.project.title}"
