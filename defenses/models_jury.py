# defenses/models.py - Extension pour le nouveau système de jury

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator, DecimalValidator
from django.core.exceptions import ValidationError
from datetime import datetime, timedelta, date
from users.models import User
from projects.models import Project


# Ajout de ces nouveaux modèles dans defenses/models.py

class DefenseJury(models.Model):
    """
    Modèle représentant un membre du jury d'une soutenance.
    Les membres du jury sont des enseignants (role='teacher') avec différents rôles.
    """
    
    ROLE_CHOICES = [
        ('president', 'Président'),
        ('examiner', 'Examinateur'),
        ('rapporteur', 'Rapporteur'),
    ]
    
    defense = models.ForeignKey(
        'Defense', 
        on_delete=models.CASCADE, 
        related_name='jury_members',
        verbose_name='Soutenance'
    )
    
    teacher = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'teacher'},
        verbose_name='Enseignant'
    )
    
    role = models.CharField(
        max_length=20, 
        choices=ROLE_CHOICES,
        verbose_name='Rôle dans le jury'
    )
    
    grade = models.DecimalField(
        max_digits=4, 
        decimal_places=2,
        null=True, 
        blank=True,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(20)
        ],
        verbose_name='Note sur 20',
        help_text='Note attribuée par ce membre du jury'
    )
    
    comments = models.TextField(
        blank=True,
        verbose_name='Commentaires',
        help_text='Observations et commentaires sur le projet'
    )
    
    graded_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Date de notation'
    )
    
    class Meta:
        verbose_name = 'Membre du jury'
        verbose_name_plural = 'Membres du jury'
        unique_together = ['defense', 'teacher']
        ordering = ['role', 'teacher']
    
    def __str__(self):
        return f"{self.teacher.get_full_name()} - {self.get_role_display()} ({self.defense})"
    
    def clean(self):
        """Validation des contraintes sur les membres du jury."""
        super().clean()
        
        # 1. Vérifier que l'enseignant a le rôle 'teacher'
        if self.teacher.role != 'teacher':
            raise ValidationError({
                'teacher': "Seuls les enseignants peuvent être membres d'un jury."
            })
        
        # 2. Seuls les Professeurs peuvent être présidents
        if self.role == 'president' and self.teacher.academic_title != 'professeur':
            raise ValidationError({
                'role': "Seul un Professeur peut être président de jury. "
                        f"{self.teacher.get_full_name()} est {self.teacher.get_academic_title_display()}."
            })
        
        # 3. Vérifier la limite de 4 présidences par jour et par département
        if self.role == 'president' and self.defense.date:
            defense_date = self.defense.date.date() if hasattr(self.defense.date, 'date') else self.defense.date
            department = self.defense.project.assignment.subject.filiere
            
            presidencies_today = DefenseJury.objects.filter(
                teacher=self.teacher,
                role='president',
                defense__date__date=defense_date,
                defense__project__assignment__subject__filiere=department
            ).exclude(pk=self.pk).count()
            
            if presidencies_today >= 4:
                raise ValidationError({
                    'teacher': f"Le professeur {self.teacher.get_full_name()} a déjà 4 présidences "
                               f"prévues ce jour dans le département {department}."
                })
        
        # 4. Un enseignant ne peut avoir qu'un seul rôle dans une soutenance
        if self.pk is None:  # Nouvelle instance uniquement
            existing = DefenseJury.objects.filter(
                defense=self.defense,
                teacher=self.teacher
            ).exists()
            
            if existing:
                raise ValidationError({
                    'teacher': f"{self.teacher.get_full_name()} est déjà membre de ce jury."
                })
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    
    @property
    def can_grade(self):
        """Vérifie si ce membre peut noter (soutenance passée)."""
        if not self.defense.date:
            return False
        return self.defense.date <= datetime.now()


# Extension du modèle Defense existant - à ajouter aux méthodes

def calculate_final_grade(defense):
    """
    Calcule la note finale comme moyenne simple des notes du jury.
    
    Args:
        defense: Instance de Defense
    
    Returns:
        float ou None: Note finale sur 20 ou None si toutes les notes ne sont pas saisies
    """
    jury_members = defense.jury_members.all()
    
    if not jury_members.exists():
        return None
    
    # Vérifier que tous les membres ont noté
    grades = [member.grade for member in jury_members if member.grade is not None]
    
    if len(grades) != jury_members.count():
        return None  # Toutes les notes pas encore saisies
    
    # Moyenne simple
    return round(sum(grades) / len(grades), 2)


def validate_jury_composition(defense):
    """
    Valide la composition du jury selon les règles:
    - Standard: 1 président, 2 examinateurs, 1 rapporteur
    - Interdisciplinaire: 1 président, 2 examinateurs, 2 rapporteurs
    
    Args:
        defense: Instance de Defense
    
    Returns:
        tuple: (is_valid, errors_list)
    """
    jury_members = defense.jury_members.all()
    errors = []
    
    # Compter par rôle
    president_count = jury_members.filter(role='president').count()
    examiner_count = jury_members.filter(role='examiner').count()
    rapporteur_count = jury_members.filter(role='rapporteur').count()
    
    # Vérification président (toujours 1)
    if president_count == 0:
        errors.append("Un président est requis.")
    elif president_count > 1:
        errors.append("Un seul président est autorisé.")
    
    # Vérifier si projet interdisciplinaire
    project = defense.project
    is_interdisciplinary = project.assignment.subject.is_interdisciplinary
    
    if is_interdisciplinary:
        # Jury élargi: 2 examinateurs, 2 rapporteurs
        if examiner_count < 2:
            errors.append("Un projet interdisciplinaire nécessite 2 examinateurs (un par filière).")
        if rapporteur_count < 2:
            errors.append("Un projet interdisciplinaire nécessite 2 rapporteurs (les 2 encadreurs).")
    else:
        # Jury standard: 2 examinateurs, 1 rapporteur
        if examiner_count < 2:
            errors.append("Au moins 2 examinateurs sont requis.")
        if rapporteur_count != 1:
            errors.append("Exactement 1 rapporteur est requis (l'encadreur principal).")
    
    return (len(errors) == 0, errors)


def check_president_availability(teacher, defense_date, department):
    """
    Vérifie si un professeur peut encore présider une soutenance ce jour dans ce département.
    Limite: 4 présidences maximum par jour et par département.
    
    Args:
        teacher: User instance (Professeur)
        defense_date: date de la soutenance
        department: code filière
    
    Returns:
        tuple: (available, count, message)
    """
    if teacher.academic_title != 'professeur':
        return (False, 0, "Seul un Professeur peut présider un jury.")
    
    presidencies_count = DefenseJury.objects.filter(
        teacher=teacher,
        role='president',
        defense__date__date=defense_date,
        defense__project__assignment__subject__filiere=department
    ).count()
    
    available = presidencies_count < 4
    remaining = 4 - presidencies_count
    
    if available:
        message = f"{teacher.get_full_name()} peut encore présider {remaining} soutenance(s) ce jour."
    else:
        message = f"{teacher.get_full_name()} a atteint la limite de 4 présidences ce jour dans ce département."
    
    return (available, presidencies_count, message)


# Ajouter ces méthodes à la classe Defense existante:
# 
# @property
# def final_grade(self):
#     """Calcule automatiquement la note finale."""
#     return calculate_final_grade(self)
# 
# def validate_jury(self):
#     """Valide la composition du jury."""
#     return validate_jury_composition(self)
# 
# @property
# def is_fully_graded(self):
#     """Vérifie si tous les membres du jury ont noté."""
#     return self.final_grade is not None
