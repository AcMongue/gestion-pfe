# Ajout des champs pour binômes et modèle ProjectTeam

# À ajouter dans subjects/models.py dans la classe Subject:

"""
    # Support des binômes
    allows_pair = models.BooleanField(
        default=False,
        verbose_name="Accepte un binôme",
        help_text="Le sujet peut être réalisé par 2 étudiants"
    )
    
    max_students = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(2)],
        help_text="1 pour individuel, 2 pour binôme"
    )
"""

# Nouveau modèle à ajouter dans projects/models.py:

from django.db import models
from django.core.exceptions import ValidationError
from users.models import User


class ProjectTeam(models.Model):
    """
    Modèle représentant l'équipe d'un projet (1 ou 2 étudiants).
    Gère les binômes avec validation de filière.
    """
    
    project = models.OneToOneField(
        'Project', 
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


# Extension StudentProposal pour les binômes
# À ajouter dans subjects/models.py:

"""
class StudentProposal(models.Model):
    # Champs existants...
    
    # Nouveaux champs pour binômes
    is_pair_project = models.BooleanField(
        default=False, 
        verbose_name="Projet en binôme",
        help_text="Cochez si vous souhaitez réaliser ce projet en binôme"
    )
    
    partner_student = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='partner_proposals',
        limit_choices_to={'role': 'student'},
        verbose_name="Étudiant partenaire",
        help_text="Sélectionnez votre binôme"
    )
    
    def clean(self):
        super().clean()
        
        # Si binôme, vérifier même filière si non-interdisciplinaire
        if self.is_pair_project and self.partner_student:
            if not self.is_interdisciplinary:
                if self.student.filiere != self.partner_student.filiere:
                    raise ValidationError({
                        'partner_student': "Binôme mono-disciplinaire : les 2 étudiants doivent être de la même filière."
                    })
            
            # Vérifier que le partenaire n'a pas déjà un projet
            if Assignment.objects.filter(student=self.partner_student, status='accepted').exists():
                raise ValidationError({
                    'partner_student': f"{self.partner_student.get_full_name()} a déjà un projet attribué."
                })
"""
