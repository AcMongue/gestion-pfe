from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from users.models import User


class Subject(models.Model):
    """
    Modèle représentant un sujet de PFE proposé par un encadreur.
    """
    
    STATUS_CHOICES = [
        ('draft', 'Brouillon'),
        ('published', 'Publié'),
        ('assigned', 'Attribué'),
        ('archived', 'Archivé'),
    ]
    
    LEVEL_CHOICES = [
        ('L3', 'Licence 3'),
        ('M2', 'Master 2'),
        ('DOC', 'Doctorat'),
    ]
    
    # Utiliser les filières ENSPD au lieu des domaines informatiques
    FILIERE_CHOICES = User.FILIERE_CHOICES
    
    TYPE_CHOICES = [
        ('research', 'Recherche'),
        ('development', 'Développement'),
        ('mixed', 'Mixte'),
    ]
    
    title = models.CharField(
        _('titre'),
        max_length=200
    )
    
    description = models.TextField(
        _('description'),
        help_text='Description détaillée du sujet'
    )
    
    objectives = models.TextField(
        _('objectifs'),
        help_text='Objectifs du projet',
        blank=True
    )
    
    prerequisites = models.TextField(
        _('prérequis'),
        help_text='Connaissances requises',
        blank=True
    )
    
    keywords = models.CharField(
        _('mots-clés'),
        max_length=200,
        help_text='Séparer par des virgules',
        blank=True
    )
    
    # Filière principale du sujet (automatiquement celle de l'encadreur)
    filiere = models.CharField(
        _('filière'),
        max_length=10,
        choices=FILIERE_CHOICES,
        default='GIT',
        help_text='Filière principale du sujet'
    )
    
    type = models.CharField(
        _('type'),
        max_length=20,
        choices=TYPE_CHOICES,
        default='mixed'
    )
    
    level = models.CharField(
        _('niveau'),
        max_length=3,
        choices=LEVEL_CHOICES
    )
    
    supervisor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='proposed_subjects',
        verbose_name=_('encadreur'),
        limit_choices_to={'role': 'supervisor'}
    )
    
    co_supervisor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='co_supervised_subjects',
        verbose_name=_('co-encadreur'),
        null=True,
        blank=True,
        limit_choices_to={'role': 'supervisor'}
    )
    
    max_students = models.PositiveIntegerField(
        _('nombre maximum d\'étudiants'),
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(3)]
    )
    
    status = models.CharField(
        _('statut'),
        max_length=20,
        choices=STATUS_CHOICES,
        default='published'
    )
    
    available_from = models.DateField(
        _('disponible à partir du'),
        null=True,
        blank=True
    )
    
    available_until = models.DateField(
        _('disponible jusqu\'au'),
        null=True,
        blank=True
    )
    
    # Support des binômes
    allows_pair = models.BooleanField(
        default=False,
        verbose_name="Accepte un binôme",
        help_text="Le sujet peut être réalisé par 2 étudiants"
    )
    
    # Champs pour projets interdisciplinaires
    is_interdisciplinary = models.BooleanField(
        _('projet interdisciplinaire'),
        default=False,
        help_text='Cochez si ce projet implique plusieurs filières'
    )
    
    # Filières additionnelles pour projets interdisciplinaires
    additional_filieres = models.JSONField(
        _('filières additionnelles'),
        default=list,
        blank=True,
        help_text='Autres filières pouvant candidater (projets interdisciplinaires)'
    )
    
    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('sujet')
        verbose_name_plural = _('sujets')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', 'level']),
            models.Index(fields=['filiere']),
        ]
    
    def __str__(self):
        return f"{self.title} - {self.get_level_display()}"
    
    def is_available(self):
        """Vérifie si le sujet est disponible pour candidature."""
        return self.status == 'published'
    
    def get_applications_count(self):
        """Retourne le nombre de candidatures pour ce sujet."""
        return self.applications.filter(status='pending').count()
    
    def get_assigned_students_count(self):
        """Retourne le nombre d'étudiants déjà affectés."""
        return self.assignments.filter(status='active').count()
    
    def has_available_slots(self):
        """Vérifie s'il reste des places disponibles."""
        return self.get_assigned_students_count() < self.max_students


class Application(models.Model):
    """
    Modèle représentant une candidature d'un étudiant pour un sujet.
    """
    
    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('accepted', 'Acceptée'),
        ('rejected', 'Rejetée'),
        ('withdrawn', 'Retirée'),
    ]
    
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name='applications',
        verbose_name=_('sujet')
    )
    
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='applications',
        verbose_name=_('étudiant'),
        limit_choices_to={'role': 'student'}
    )
    
    motivation_letter = models.TextField(
        _('lettre de motivation'),
        help_text='Expliquez pourquoi vous souhaitez travailler sur ce sujet'
    )
    
    cv_file = models.FileField(
        _('CV'),
        upload_to='applications/cv/',
        null=True,
        blank=True
    )
    
    status = models.CharField(
        _('statut'),
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    
    priority = models.PositiveIntegerField(
        _('priorité'),
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text='1 = priorité maximale, 5 = priorité minimale'
    )
    
    reviewed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='reviewed_applications',
        verbose_name=_('évalué par'),
        null=True,
        blank=True
    )
    
    reviewed_at = models.DateTimeField(
        _('évalué le'),
        null=True,
        blank=True
    )
    
    review_notes = models.TextField(
        _('notes d\'évaluation'),
        blank=True
    )
    
    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('candidature')
        verbose_name_plural = _('candidatures')
        ordering = ['-created_at']
        unique_together = ['subject', 'student']
        indexes = [
            models.Index(fields=['status', 'priority']),
        ]
    
    def __str__(self):
        return f"{self.student.get_full_name()} - {self.subject.title}"


class Assignment(models.Model):
    """
    Modèle représentant l'affectation d'un étudiant à un sujet.
    """
    
    STATUS_CHOICES = [
        ('active', 'Actif'),
        ('completed', 'Terminé'),
        ('cancelled', 'Annulé'),
    ]
    
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name='assignments',
        verbose_name=_('sujet')
    )
    
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='assignment',
        verbose_name=_('étudiant'),
        limit_choices_to={'role': 'student'}
    )
    
    application = models.OneToOneField(
        Application,
        on_delete=models.SET_NULL,
        related_name='assignment',
        verbose_name=_('candidature'),
        null=True,
        blank=True
    )
    
    status = models.CharField(
        _('statut'),
        max_length=20,
        choices=STATUS_CHOICES,
        default='active'
    )
    
    assigned_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='made_assignments',
        verbose_name=_('affecté par'),
        null=True,
        blank=True,
        limit_choices_to={'role': 'admin'}
    )
    
    start_date = models.DateField(
        _('date de début'),
        null=True,
        blank=True
    )
    
    expected_end_date = models.DateField(
        _('date de fin prévue'),
        null=True,
        blank=True
    )
    
    notes = models.TextField(
        _('notes'),
        blank=True
    )
    
    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('affectation')
        verbose_name_plural = _('affectations')
        ordering = ['-created_at']
        unique_together = ['student']
        indexes = [
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"{self.student.get_full_name()} → {self.subject.title}"


class StudentProposal(models.Model):
    """
    Modèle représentant une proposition de sujet initiée par un étudiant.
    L'étudiant propose son idée de projet et choisit des encadreurs potentiels.
    """
    
    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('accepted', 'Acceptée'),
        ('rejected', 'Rejetée'),
        ('withdrawn', 'Retirée'),
    ]
    
    FILIERE_CHOICES = Subject.FILIERE_CHOICES
    TYPE_CHOICES = Subject.TYPE_CHOICES
    
    # Informations de l'étudiant
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='proposals',
        verbose_name=_('étudiant'),
        limit_choices_to={'role': 'student'}
    )
    
    # Proposition de sujet
    title = models.CharField(
        _('titre du projet'),
        max_length=200,
        help_text='Titre de votre projet proposé'
    )
    
    description = models.TextField(
        _('description'),
        help_text='Description détaillée de votre idée de projet'
    )
    
    objectives = models.TextField(
        _('objectifs'),
        help_text='Quels sont les objectifs de ce projet ?'
    )
    
    methodology = models.TextField(
        _('méthodologie envisagée'),
        help_text='Comment comptez-vous réaliser ce projet ?',
        blank=True
    )
    
    technologies = models.CharField(
        _('technologies'),
        max_length=500,
        help_text='Technologies que vous prévoyez d\'utiliser',
        blank=True
    )
    
    filiere = models.CharField(
        _('filière'),
        max_length=10,
        choices=FILIERE_CHOICES,
        default='GIT',
        help_text='Filière de votre projet'
    )
    
    type = models.CharField(
        _('type'),
        max_length=20,
        choices=TYPE_CHOICES,
        default='development'
    )
    
    # Choix d'encadreurs (jusqu'à 3)
    preferred_supervisor_1 = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='proposals_as_choice_1',
        verbose_name=_('1er choix d\'encadreur'),
        null=True,
        limit_choices_to={'role': 'supervisor'}
    )
    
    preferred_supervisor_2 = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='proposals_as_choice_2',
        verbose_name=_('2ème choix d\'encadreur'),
        null=True,
        blank=True,
        limit_choices_to={'role': 'supervisor'}
    )
    
    preferred_supervisor_3 = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='proposals_as_choice_3',
        verbose_name=_('3ème choix d\'encadreur'),
        null=True,
        blank=True,
        limit_choices_to={'role': 'supervisor'}
    )
    
    # Justification du choix d'encadreurs
    supervisor_justification = models.TextField(
        _('justification du choix des encadreurs'),
        help_text='Pourquoi avez-vous choisi ces encadreurs ?',
        blank=True
    )
    
    # Statut
    status = models.CharField(
        _('statut'),
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    
    # Encadreur qui a accepté (si acceptée)
    accepted_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='accepted_proposals',
        verbose_name=_('acceptée par'),
        null=True,
        blank=True,
        limit_choices_to={'role': 'supervisor'}
    )
    
    # Notes de l'encadreur
    supervisor_comments = models.TextField(
        _('commentaires de l\'encadreur'),
        blank=True
    )
    
    # Champs pour projets interdisciplinaires
    is_interdisciplinary = models.BooleanField(
        _('projet interdisciplinaire'),
        default=False,
        help_text='Mon projet concerne plusieurs filières'
    )
    
    related_filieres = models.JSONField(
        _('filières associées'),
        default=list,
        blank=True,
        help_text='Autres filières concernées par ce projet'
    )
    
    # Dates
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    reviewed_at = models.DateTimeField(
        _('date de révision'),
        null=True,
        blank=True
    )
    
    class Meta:
        verbose_name = _('proposition d\'étudiant')
        verbose_name_plural = _('propositions d\'étudiants')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', 'student']),
            models.Index(fields=['status', 'preferred_supervisor_1']),
        ]
    
    def __str__(self):
        return f"{self.title} - {self.student.get_full_name()}"
    
    def get_preferred_supervisors(self):
        """Retourne la liste des encadreurs choisis."""
        supervisors = []
        if self.preferred_supervisor_1:
            supervisors.append(self.preferred_supervisor_1)
        if self.preferred_supervisor_2:
            supervisors.append(self.preferred_supervisor_2)
        if self.preferred_supervisor_3:
            supervisors.append(self.preferred_supervisor_3)
        return supervisors
    
    def is_pending(self):
        """Vérifie si la proposition est en attente."""
        return self.status == 'pending'
    
    def can_be_accepted_by(self, supervisor):
        """Vérifie si un encadreur peut accepter cette proposition."""
        return (
            self.status == 'pending' and
            supervisor in self.get_preferred_supervisors()
        )
