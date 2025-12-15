from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from datetime import datetime
import re


def validate_matricule(value):
    """
    Valide le format du matricule: xxGxxxxx
    - xx: année d'entrée (2 chiffres)
    - G: lettre obligatoire
    - xxxxx: 5 chiffres
    
    Exemples valides: 21G12345, 23G00001, 19G99999
    
    Logique temporelle (M2 seulement):
    - Entré niveau 1 (L1): peut soutenir après 5 ans (ex: 21G soutient en 2026)
    - Entré niveau 3 (L3): peut soutenir après 3 ans (ex: 23G soutient en 2026)
    
    Formule: Année de soutenance minimum = Année d'entrée + (6 - niveau_entrée)
    """
    if not value:
        return
    
    # Vérifier le format: xxGxxxxx
    pattern = r'^(\d{2})G(\d{5})$'
    match = re.match(pattern, value)
    
    if not match:
        raise ValidationError(
            "Le matricule doit être au format xxGxxxxx où x sont des chiffres. "
            "Exemple: 21G12345"
        )
    
    # Extraire l'année d'entrée
    entry_year_short = int(match.group(1))
    
    # Convertir en année complète (20xx)
    # Si >= 90, c'est 19xx, sinon 20xx
    if entry_year_short >= 90:
        entry_year = 1900 + entry_year_short
    else:
        entry_year = 2000 + entry_year_short
    
    # Vérifier que l'année d'entrée n'est pas dans le futur
    current_year = datetime.now().year
    if entry_year > current_year:
        raise ValidationError(
            f"L'année d'entrée ({entry_year}) ne peut pas être dans le futur."
        )
    
    # Vérifier que l'année d'entrée n'est pas trop ancienne (> 10 ans)
    if current_year - entry_year > 10:
        raise ValidationError(
            f"L'année d'entrée ({entry_year}) est trop ancienne (plus de 10 ans)."
        )


class User(AbstractUser):
    """
    Modèle utilisateur personnalisé pour le système de gestion PFE.
    Supporte différents rôles: étudiant, encadreur, administration, jury.
    """
    
    ROLE_CHOICES = [
        ('student', 'Étudiant'),
        ('teacher', 'Enseignant'),
        ('admin_filiere', 'Administrateur de Filière'),
        ('admin_general', 'Administrateur Général'),
    ]
    
    LEVEL_CHOICES = [
        ('M2', 'Master 2'),
    ]
    
    ENTRY_LEVEL_CHOICES = [
        ('1', 'Niveau 1 (Licence 1)'),
        ('3', 'Niveau 3 (Licence 3)'),
    ]
    
    # Filières de l'ENSPD
    FILIERE_CHOICES = [
        ('GIT', 'Génie Informatique & Télécommunications'),
        ('GESI', 'Génie Électrique et Systèmes Intelligents'),
        ('GQHSEI', 'Génie de la Qualité Hygiène, Sécurité et Environnement Industriel'),
        ('GAM', 'Génie Automobile et Mécatronique'),
        ('GMP', 'Génie Maritime et Portuaire'),
        ('GP', 'Génie des Procédés'),
        ('GE', 'Génie Énergétique'),
        ('GM', 'Génie Mécanique'),
        ('GC', 'Génie Civil'),
    ]
    
    # Titres académiques
    ACADEMIC_TITLE_CHOICES = [
        ('assistant', 'Assistant'),
        ('maitre_assistant', 'Maître Assistant'),
        ('maitre_conference', 'Maître de Conférences'),
        ('professeur', 'Professeur'),
    ]
    
    role = models.CharField(
        _('rôle'),
        max_length=20,
        choices=ROLE_CHOICES,
        default='student'
    )
    
    # Champ pour les administrateurs de filière
    filiere_admin = models.CharField(
        _('filière administrée'),
        max_length=10,
        choices=[(code, nom) for code, nom in [  # Liste dynamique
            ('GIT', 'Génie Informatique & Télécommunications'),
            ('GESI', 'Génie Électrique et Systèmes Intelligents'),
            ('GQHSEI', 'Génie de la Qualité Hygiène, Sécurité et Environnement Industriel'),
            ('GAM', 'Génie Automobile et Mécatronique'),
            ('GMP', 'Génie Maritime et Portuaire'),
            ('GP', 'Génie des Procédés'),
            ('GE', 'Génie Énergétique'),
            ('GM', 'Génie Mécanique'),
            ('GC', 'Génie Civil'),
        ]],
        blank=True,
        null=True,
        help_text='Filière gérée (pour admin_filiere uniquement)'
    )
    
    # Champs spécifiques aux étudiants
    matricule = models.CharField(
        _('matricule'),
        max_length=20,
        blank=True,
        unique=True,
        null=True,
        validators=[validate_matricule],
        help_text="Format: xxGxxxxx (ex: 21G12345)"
    )
    
    entry_level = models.CharField(
        _('niveau d\'entrée'),
        max_length=1,
        choices=ENTRY_LEVEL_CHOICES,
        blank=True,
        null=True,
        help_text="Niveau auquel vous êtes entré à l'ENSPD"
    )
    
    level = models.CharField(
        _('niveau actuel'),
        max_length=3,
        choices=LEVEL_CHOICES,
        blank=True,
        null=True,
        help_text="Niveau actuel (M2 pour soutenance)"
    )
    
    filiere = models.CharField(
        _('filière'),
        max_length=10,
        choices=FILIERE_CHOICES,
        blank=True,
        help_text="Filière d'appartenance (obligatoire pour étudiants, encadreurs et admins)"
    )
    
    # Champs communs
    phone = models.CharField(
        _('téléphone'),
        max_length=20,
        blank=True
    )
    
    avatar = models.ImageField(
        _('photo de profil'),
        upload_to='avatars/',
        blank=True,
        null=True
    )
    
    bio = models.TextField(
        _('biographie'),
        blank=True
    )
    
    # Champs spécifiques aux encadreurs
    specialite = models.CharField(
        _('spécialité'),
        max_length=200,
        blank=True
    )
    
    grade = models.CharField(
        _('grade'),
        max_length=100,
        blank=True,
        help_text="Ancien champ - utiliser academic_title"
    )
    
    academic_title = models.CharField(
        _('titre académique'),
        max_length=50,
        choices=ACADEMIC_TITLE_CHOICES,
        blank=True,
        help_text="Titre académique (obligatoire pour encadreurs)"
    )
    
    max_students = models.PositiveIntegerField(
        _('nombre maximum d\'étudiants'),
        default=5,
        help_text="Nombre maximum d'étudiants pouvant être encadrés simultanément"
    )
    
    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('utilisateur')
        verbose_name_plural = _('utilisateurs')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.get_role_display()})"
    
    def get_full_name(self):
        """Retourne le nom complet de l'utilisateur."""
        return f"{self.first_name} {self.last_name}".strip() or self.username
    
    def is_student(self):
        """Vérifie si l'utilisateur est un étudiant."""
        return self.role == 'student'
    
    def is_teacher(self):
        """Vérifie si l'utilisateur est un enseignant."""
        return self.role == 'teacher'
    
    def is_admin_staff(self):
        """Vérifie si l'utilisateur est de l'administration (tous types)."""
        return self.role in ['admin_filiere', 'admin_general']
    
    def is_admin_filiere(self):
        """Vérifie si l'utilisateur est un administrateur de filière."""
        return self.role == 'admin_filiere'
    
    def is_admin_general(self):
        """Vérifie si l'utilisateur est un administrateur général."""
        return self.role == 'admin_general'
    
    def can_manage_filiere(self, filiere_code):
        """Vérifie si l'admin peut gérer une filière donnée."""
        if self.is_admin_general():
            return True  # Admin général gère tout
        if self.is_admin_filiere():
            return self.filiere_admin == filiere_code
        return False
    
    @property
    def can_be_jury_president(self):
        """Vérifie si l'enseignant peut être président de jury (uniquement les Professeurs)."""
        return self.is_teacher() and self.academic_title == 'professeur'
    
    @property
    def current_supervision_count(self):
        """Compte le nombre d'étudiants actuellement encadrés."""
        if not self.is_teacher():
            return 0
        from projects.models import Project
        return Project.objects.filter(
            supervisor=self,
            status__in=['pending', 'in_progress']
        ).count()
    
    def can_supervise_more(self):
        """Vérifie si l'encadreur peut prendre plus d'étudiants."""
        return self.current_supervision_count < self.max_students
    
    def get_available_slots(self):
        """Retourne le nombre de places disponibles."""
        return max(0, self.max_students - self.current_supervision_count)


class Profile(models.Model):
    """
    Informations de profil supplémentaires pour les utilisateurs.
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    
    date_of_birth = models.DateField(
        _('date de naissance'),
        blank=True,
        null=True
    )
    
    address = models.TextField(
        _('adresse'),
        blank=True
    )
    
    city = models.CharField(
        _('ville'),
        max_length=100,
        blank=True
    )
    
    country = models.CharField(
        _('pays'),
        max_length=100,
        default='Cameroun'
    )
    
    linkedin_url = models.URLField(
        _('profil LinkedIn'),
        blank=True
    )
    
    github_url = models.URLField(
        _('profil GitHub'),
        blank=True
    )
    
    website = models.URLField(
        _('site web'),
        blank=True
    )
    
    # Paramètres de notification
    email_notifications = models.BooleanField(
        _('notifications par email'),
        default=True
    )
    
    sms_notifications = models.BooleanField(
        _('notifications par SMS'),
        default=False
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('profil')
        verbose_name_plural = _('profils')
    
    def __str__(self):
        return f"Profil de {self.user.get_full_name()}"
