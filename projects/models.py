from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator, FileExtensionValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
from users.models import User
from subjects.models import Assignment


class AcademicYear(models.Model):
    """Modèle représentant une année académique avec dates importantes."""
    
    year = models.CharField(
        _('année académique'),
        max_length=9,
        unique=True,
        help_text='Format: 2025-2026'
    )
    
    start_date = models.DateField(
        _('date de début'),
        help_text='Date de début de l\'année académique'
    )
    
    end_date = models.DateField(
        _('date de fin'),
        help_text='Date de fin de l\'année académique'
    )
    
    thesis_submission_deadline = models.DateField(
        _('date limite de dépôt des mémoires'),
        help_text='Date limite pour la soumission des mémoires de PFE'
    )
    
    is_active = models.BooleanField(
        _('année active'),
        default=False,
        help_text='Une seule année peut être active à la fois'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('année académique')
        verbose_name_plural = _('années académiques')
        ordering = ['-start_date']
    
    def __str__(self):
        return self.year
    
    def clean(self):
        """Validation: une seule année active à la fois."""
        super().clean()
        
        if self.is_active:
            # Vérifier qu'il n'y a pas déjà une année active
            existing_active = AcademicYear.objects.filter(is_active=True)
            if self.pk:
                existing_active = existing_active.exclude(pk=self.pk)
            
            if existing_active.exists():
                raise ValidationError({
                    'is_active': 'Une autre année académique est déjà active. '
                                'Désactivez-la d\'abord.'
                })
        
        # Vérifier que la date de fin est après la date de début
        if self.end_date <= self.start_date:
            raise ValidationError({
                'end_date': 'La date de fin doit être après la date de début.'
            })
        
        # Vérifier que la deadline est entre le début et la fin
        if not (self.start_date <= self.thesis_submission_deadline <= self.end_date):
            raise ValidationError({
                'thesis_submission_deadline': 'La date limite doit être entre '
                                             'le début et la fin de l\'année académique.'
            })
    
    def save(self, *args, **kwargs):
        self.full_clean()
        
        # Si on active cette année, désactiver les autres
        if self.is_active:
            AcademicYear.objects.filter(is_active=True).exclude(pk=self.pk).update(is_active=False)
        
        super().save(*args, **kwargs)
    
    @classmethod
    def get_active_year(cls):
        """Retourne l'année académique active."""
        return cls.objects.filter(is_active=True).first()


class Project(models.Model):
    """Modèle représentant un projet de PFE en cours."""
    
    STATUS_CHOICES = [
        ('awaiting_kickoff', 'En attente de cadrage'),
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
    
    # Champs pour la gestion du mémoire
    thesis_file = models.FileField(
        _('mémoire de PFE'),
        upload_to='projects/thesis/',
        null=True,
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])],
        help_text='Fichier PDF du mémoire final'
    )
    
    thesis_submitted_at = models.DateTimeField(
        _('date de soumission du mémoire'),
        null=True,
        blank=True
    )
    
    thesis_approved_by_supervisor = models.BooleanField(
        _('mémoire approuvé par l\'encadreur'),
        default=False,
        help_text='L\'encadreur doit approuver le mémoire avant distribution au jury'
    )
    
    thesis_approval_date = models.DateTimeField(
        _('date d\'approbation du mémoire'),
        null=True,
        blank=True
    )
    
    thesis_distributed_to_jury = models.BooleanField(
        _('mémoire distribué au jury'),
        default=False
    )
    
    thesis_distribution_date = models.DateTimeField(
        _('date de distribution au jury'),
        null=True,
        blank=True
    )
    
    academic_year = models.ForeignKey(
        AcademicYear,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='projects',
        verbose_name=_('année académique')
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('projet')
        verbose_name_plural = _('projets')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title}"
    
    @property
    def progress(self):
        """
        Calcule automatiquement le pourcentage d'avancement basé sur les jalons validés.
        Si aucun jalon n'existe, retourne le pourcentage manuel.
        """
        total_milestones = self.milestones.count()
        
        if total_milestones == 0:
            # Pas de jalons définis, utiliser le pourcentage manuel
            return self.progress_percentage
        
        # Calculer basé sur les jalons validés
        validated_milestones = self.milestones.filter(validated_by_supervisor=True).count()
        calculated_progress = int((validated_milestones / total_milestones) * 100)
        
        return calculated_progress
    
    def update_progress_from_milestones(self):
        """
        Met à jour le champ progress_percentage basé sur les jalons validés.
        Utile pour la compatibilité avec le code existant.
        """
        self.progress_percentage = self.progress
        self.save(update_fields=['progress_percentage'])
    
    def status_badge_class(self):
        """Retourne la classe CSS Bootstrap pour le badge de statut."""
        status_classes = {
            'in_progress': 'primary',
            'submitted': 'info',
            'under_review': 'warning',
            'approved': 'success',
            'rejected': 'danger',
            'completed': 'success',
        }
        return status_classes.get(self.status, 'secondary')
    
    @property
    def is_thesis_submitted(self):
        """Vérifie si le mémoire a été soumis."""
        return self.thesis_file and self.thesis_submitted_at is not None
    
    @property
    def is_thesis_late(self):
        """Vérifie si la soumission du mémoire est en retard."""
        if not self.academic_year or self.is_thesis_submitted:
            return False
        return timezone.now().date() > self.academic_year.thesis_submission_deadline
    
    @property
    def days_until_thesis_deadline(self):
        """Nombre de jours restants jusqu'à la deadline du mémoire."""
        if not self.academic_year:
            return None
        delta = self.academic_year.thesis_submission_deadline - timezone.now().date()
        return delta.days
    
    def submit_thesis(self, thesis_file):
        """Soumet le mémoire."""
        self.thesis_file = thesis_file
        self.thesis_submitted_at = timezone.now()
        self.save()
    
    def approve_thesis(self, approved_by):
        """Approuve le mémoire (par l'encadreur)."""
        if not self.is_thesis_submitted:
            raise ValidationError("Le mémoire doit d'abord être soumis.")
        
        self.thesis_approved_by_supervisor = True
        self.thesis_approval_date = timezone.now()
        self.save()
        
        # Optionnel: distribuer automatiquement au jury
        # self.distribute_thesis_to_jury()
    
    def distribute_thesis_to_jury(self):
        """Distribue le mémoire aux membres du jury par email."""
        if not self.thesis_approved_by_supervisor:
            raise ValidationError("Le mémoire doit être approuvé par l'encadreur.")
        
        if not hasattr(self, 'defense') or not self.defense:
            raise ValidationError("Aucune soutenance programmée pour ce projet.")
        
        # Importer ici pour éviter les imports circulaires
        from communications.email_utils import distribute_thesis_to_jury
        
        distribute_thesis_to_jury(self)
        
        self.thesis_distributed_to_jury = True
        self.thesis_distribution_date = timezone.now()
        self.save()


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


class ProjectTeam(models.Model):
    """
    Modèle représentant l'équipe d'un projet (1 ou 2 étudiants).
    Gère les binômes avec validation de filière.
    """
    
    project = models.OneToOneField(
        Project, 
        on_delete=models.CASCADE, 
        related_name='team',
        verbose_name='Projet'
    )
    
    student1 = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='projects_as_student1',
        verbose_name='Étudiant 1 (principal)',
        limit_choices_to={'role': 'student'}
    )
    
    student2 = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='projects_as_student2',
        verbose_name='Étudiant 2 (binôme)',
        null=True,
        blank=True,
        limit_choices_to={'role': 'student'}
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Équipe de projet'
        verbose_name_plural = 'Équipes de projet'
    
    def __str__(self):
        if self.student2:
            return f"{self.student1.get_full_name()} & {self.student2.get_full_name()}"
        return f"{self.student1.get_full_name()}"
    
    def clean(self):
        """Valide la composition du binôme."""
        super().clean()
        
        # Vérifier que les 2 étudiants sont différents
        if self.student2 and self.student1 == self.student2:
            raise ValidationError({
                'student2': "Les deux étudiants doivent être différents."
            })
        
        # Vérifier même filière si projet non-interdisciplinaire
        if self.student2:
            subject = self.project.assignment.subject
            
            if not subject.is_interdisciplinary:
                if self.student1.filiere != self.student2.filiere:
                    raise ValidationError({
                        'student2': f"Les 2 étudiants doivent être de la même filière pour un sujet mono-disciplinaire. "
                                    f"{self.student1.get_full_name()} est en {self.student1.get_filiere_display()}, "
                                    f"{self.student2.get_full_name()} est en {self.student2.get_filiere_display()}."
                    })
        
        # Vérifier que le sujet accepte les binômes si student2 existe
        if self.student2:
            subject = self.project.assignment.subject
            if not subject.allows_pair:
                raise ValidationError({
                    'student2': "Ce sujet n'accepte pas les binômes."
                })
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    
    @property
    def is_pair(self):
        """Indique si c'est un binôme."""
        return self.student2 is not None
    
    @property
    def student_count(self):
        """Nombre d'étudiants dans l'équipe."""
        return 2 if self.student2 else 1
    
    def get_all_students(self):
        """Retourne la liste de tous les étudiants."""
        if self.student2:
            return [self.student1, self.student2]
        return [self.student1]


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


class Meeting(models.Model):
    """Modèle représentant une réunion de suivi entre étudiant et encadreur."""
    
    TYPE_CHOICES = [
        ('kickoff', 'Réunion de cadrage'),
        ('follow_up', 'Réunion de suivi'),
        ('milestone_review', 'Revue de jalon'),
        ('final_review', 'Revue finale'),
        ('emergency', 'Réunion d\'urgence'),
    ]
    
    STATUS_CHOICES = [
        ('scheduled', 'Planifiée'),
        ('completed', 'Complétée'),
        ('cancelled', 'Annulée'),
        ('rescheduled', 'Reportée'),
    ]
    
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='meetings',
        verbose_name=_('projet')
    )
    
    type = models.CharField(
        _('type'),
        max_length=20,
        choices=TYPE_CHOICES,
        default='follow_up'
    )
    
    title = models.CharField(
        _('titre'),
        max_length=200
    )
    
    description = models.TextField(
        _('description'),
        help_text='Ordre du jour / Sujets à discuter',
        blank=True
    )
    
    scheduled_date = models.DateTimeField(
        _('date prévue')
    )
    
    duration_minutes = models.PositiveIntegerField(
        _('durée (minutes)'),
        default=60,
        validators=[MinValueValidator(15), MaxValueValidator(240)]
    )
    
    location = models.CharField(
        _('lieu'),
        max_length=200,
        help_text='Bureau, salle, ou lien visioconférence',
        blank=True
    )
    
    status = models.CharField(
        _('statut'),
        max_length=20,
        choices=STATUS_CHOICES,
        default='scheduled'
    )
    
    # Compte-rendu
    minutes = models.TextField(
        _('compte-rendu'),
        help_text='Résumé de la réunion',
        blank=True
    )
    
    topics_discussed = models.TextField(
        _('points discutés'),
        blank=True
    )
    
    decisions_made = models.TextField(
        _('décisions prises'),
        blank=True
    )
    
    action_items = models.TextField(
        _('actions à réaliser'),
        help_text='Actions décidées avec responsables',
        blank=True
    )
    
    student_notes = models.TextField(
        _('notes de l\'étudiant'),
        blank=True
    )
    
    supervisor_notes = models.TextField(
        _('notes de l\'encadreur'),
        blank=True
    )
    
    # Prochaine réunion
    next_meeting_date = models.DateTimeField(
        _('date de la prochaine réunion'),
        null=True,
        blank=True
    )
    
    # Participants
    student_attended = models.BooleanField(
        _('étudiant présent'),
        default=True
    )
    
    supervisor_attended = models.BooleanField(
        _('encadreur présent'),
        default=True
    )
    
    # Documents attachés
    attachments = models.FileField(
        _('pièces jointes'),
        upload_to='meetings/attachments/',
        blank=True,
        null=True
    )
    
    # Métadonnées
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='created_meetings',
        null=True
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(
        _('complétée le'),
        null=True,
        blank=True
    )
    
    class Meta:
        verbose_name = _('réunion')
        verbose_name_plural = _('réunions')
        ordering = ['-scheduled_date']
        indexes = [
            models.Index(fields=['project', 'status']),
            models.Index(fields=['scheduled_date']),
        ]
    
    def __str__(self):
        return f"{self.get_type_display()} - {self.project.title} - {self.scheduled_date.strftime('%Y-%m-%d')}"
    
    def is_upcoming(self):
        """Vérifie si la réunion est à venir."""
        return self.status == 'scheduled' and self.scheduled_date > timezone.now()
    
    def is_past(self):
        """Vérifie si la réunion est passée."""
        return self.scheduled_date < timezone.now()
    
    def mark_completed(self):
        """Marque la réunion comme complétée."""
        self.status = 'completed'
        self.completed_at = timezone.now()
        self.save()


class WorkLog(models.Model):
    """Journal de bord pour le suivi quotidien du travail sur un projet."""
    
    project = models.ForeignKey(
        Project, 
        on_delete=models.CASCADE, 
        related_name='work_logs',
        verbose_name=_('projet')
    )
    
    date = models.DateField(
        _('date'),
        default=timezone.now,
        help_text="Date de l'activité"
    )
    
    duration_hours = models.DecimalField(
        _('durée (heures)'),
        max_digits=4,
        decimal_places=1,
        validators=[MinValueValidator(0.5)],
        help_text="Nombre d'heures travaillées"
    )
    
    activities = models.TextField(
        _('activités réalisées'),
        help_text="Décrivez en détail ce qui a été fait"
    )
    
    achievements = models.TextField(
        _('réalisations/résultats'),
        blank=True,
        help_text="Objectifs atteints, livrables produits"
    )
    
    difficulties = models.TextField(
        _('difficultés rencontrées'),
        blank=True,
        help_text="Problèmes, blocages, questions"
    )
    
    next_steps = models.TextField(
        _('prochaines étapes'),
        blank=True,
        help_text="Ce qui est prévu pour la prochaine session"
    )
    
    resources_used = models.TextField(
        _('ressources utilisées'),
        blank=True,
        help_text="Documentation, tutoriels, outils utilisés"
    )
    
    # Visibilité
    is_visible_to_supervisor = models.BooleanField(
        _('visible par l\'encadreur'),
        default=True,
        help_text="L'encadreur peut voir cette entrée"
    )
    
    # Feedback de l'encadreur
    supervisor_feedback = models.TextField(
        _('commentaires de l\'encadreur'),
        blank=True
    )
    
    supervisor_read_at = models.DateTimeField(
        _('lu par l\'encadreur le'),
        null=True,
        blank=True
    )
    
    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('entrée du journal de bord')
        verbose_name_plural = _('journal de bord')
        ordering = ['-date', '-created_at']
        unique_together = [['project', 'date']]  # Une seule entrée par jour par projet
    
    def __str__(self):
        return f"{self.project.title} - {self.date.strftime('%d/%m/%Y')}"
    
    def mark_as_read_by_supervisor(self, supervisor):
        """Marque l'entrée comme lue par l'encadreur."""
        if not self.supervisor_read_at:
            self.supervisor_read_at = timezone.now()
            self.save()
    
    @property
    def total_hours_this_week(self):
        """Calcule le total d'heures travaillées cette semaine."""
        from datetime import timedelta
        week_start = self.date - timedelta(days=self.date.weekday())
        week_end = week_start + timedelta(days=6)
        
        return WorkLog.objects.filter(
            project=self.project,
            date__range=[week_start, week_end]
        ).aggregate(
            total=models.Sum('duration_hours')
        )['total'] or 0
    
    @property
    def is_recent(self):
        """Vérifie si l'entrée date de moins de 7 jours."""
        from datetime import timedelta
        return self.date >= (timezone.now().date() - timedelta(days=7))
