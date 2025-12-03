from django.db import models
from django.utils.translation import gettext_lazy as _
from users.models import User
from projects.models import Project


class ArchivedProject(models.Model):
    """Modèle représentant un projet archivé."""
    
    project = models.OneToOneField(Project, on_delete=models.CASCADE, related_name='archive', verbose_name=_('projet'))
    archived_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='archived_projects', null=True, verbose_name=_('archivé par'))
    archived_at = models.DateTimeField(auto_now_add=True, verbose_name=_('archivé le'))
    year = models.PositiveIntegerField(_('année académique'))
    semester = models.CharField(_('semestre'), max_length=2, choices=[('S1', 'Semestre 1'), ('S2', 'Semestre 2')])
    final_grade = models.DecimalField(_('note finale'), max_digits=4, decimal_places=2, null=True, blank=True)
    keywords = models.CharField(_('mots-clés'), max_length=500, blank=True)
    summary = models.TextField(_('résumé'), blank=True)
    achievements = models.TextField(_('réalisations'), blank=True)
    is_public = models.BooleanField(_('visible publiquement'), default=True)
    views_count = models.PositiveIntegerField(_('nombre de vues'), default=0)
    
    class Meta:
        verbose_name = _('projet archivé')
        verbose_name_plural = _('projets archivés')
        ordering = ['-year', '-archived_at']
    
    def __str__(self):
        return f"{self.project.title} ({self.year})"


class Report(models.Model):
    """Modèle représentant un rapport statistique."""
    
    TYPE_CHOICES = [
        ('monthly', 'Mensuel'),
        ('semester', 'Semestriel'),
        ('annual', 'Annuel'),
        ('custom', 'Personnalisé'),
    ]
    
    title = models.CharField(_('titre'), max_length=200)
    type = models.CharField(_('type'), max_length=20, choices=TYPE_CHOICES)
    period_start = models.DateField(_('début période'))
    period_end = models.DateField(_('fin période'))
    generated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name=_('généré par'))
    generated_at = models.DateTimeField(auto_now_add=True, verbose_name=_('généré le'))
    content = models.JSONField(_('contenu'), help_text='Données statistiques en JSON')
    file = models.FileField(_('fichier PDF'), upload_to='reports/', null=True, blank=True)
    
    class Meta:
        verbose_name = _('rapport')
        verbose_name_plural = _('rapports')
        ordering = ['-generated_at']
    
    def __str__(self):
        return f"{self.title} - {self.get_type_display()}"
