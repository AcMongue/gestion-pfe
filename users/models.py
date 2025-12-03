from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """
    Modèle utilisateur personnalisé pour le système de gestion PFE.
    Supporte différents rôles: étudiant, encadreur, administration, jury.
    """
    
    ROLE_CHOICES = [
        ('student', 'Étudiant'),
        ('supervisor', 'Encadreur'),
        ('admin', 'Administration'),
        ('jury', 'Membre du jury'),
    ]
    
    LEVEL_CHOICES = [
        ('L3', 'Licence 3'),
        ('M2', 'Master 2'),
        ('DOC', 'Doctorat'),
    ]
    
    role = models.CharField(
        _('rôle'),
        max_length=20,
        choices=ROLE_CHOICES,
        default='student'
    )
    
    # Champs spécifiques aux étudiants
    matricule = models.CharField(
        _('matricule'),
        max_length=20,
        blank=True,
        unique=True,
        null=True
    )
    
    level = models.CharField(
        _('niveau'),
        max_length=3,
        choices=LEVEL_CHOICES,
        blank=True,
        null=True
    )
    
    filiere = models.CharField(
        _('filière'),
        max_length=100,
        blank=True
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
        blank=True
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
    
    def is_supervisor(self):
        """Vérifie si l'utilisateur est un encadreur."""
        return self.role == 'supervisor'
    
    def is_admin_staff(self):
        """Vérifie si l'utilisateur est de l'administration."""
        return self.role == 'admin'
    
    def is_jury_member(self):
        """Vérifie si l'utilisateur est membre du jury."""
        return self.role == 'jury'


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
