from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Project, Milestone, Deliverable, Comment, WorkLog


class ProjectForm(forms.ModelForm):
    """Formulaire de création/modification de projet."""
    
    class Meta:
        model = Project
        fields = ['title', 'description', 'objectives', 'methodology', 'technologies', 
                  'repository_url', 'documentation_url', 'expected_end_date']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'objectives': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'methodology': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'technologies': forms.TextInput(attrs={'class': 'form-control'}),
            'repository_url': forms.URLInput(attrs={'class': 'form-control'}),
            'documentation_url': forms.URLInput(attrs={'class': 'form-control'}),
            'expected_end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


class MilestoneForm(forms.ModelForm):
    """Formulaire de création/modification de jalon."""
    
    class Meta:
        model = Milestone
        fields = ['title', 'description', 'due_date', 'order']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'due_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class DeliverableForm(forms.ModelForm):
    """Formulaire de soumission de livrable."""
    
    class Meta:
        model = Deliverable
        fields = ['title', 'description', 'type', 'file', 'version', 'milestone']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'type': forms.Select(attrs={'class': 'form-control'}),
            'file': forms.FileInput(attrs={'class': 'form-control'}),
            'version': forms.TextInput(attrs={'class': 'form-control'}),
            'milestone': forms.Select(attrs={'class': 'form-control'}),
        }


class CommentForm(forms.ModelForm):
    """Formulaire de commentaire."""
    
    class Meta:
        model = Comment
        fields = ['content', 'is_private']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Votre commentaire...'}),
            'is_private': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class DeliverableReviewForm(forms.ModelForm):
    """Formulaire de révision de livrable par le superviseur."""
    
    class Meta:
        model = Deliverable
        fields = ['status', 'rating', 'review_comments']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
            'rating': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 20, 'step': 0.5}),
            'review_comments': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Vos commentaires sur ce livrable...'}),
        }
        labels = {
            'status': 'Statut',
            'rating': 'Note (/20)',
            'review_comments': 'Commentaires',
        }


class WorkLogForm(forms.ModelForm):
    """Formulaire pour ajouter une entrée au journal de bord."""
    
    class Meta:
        model = WorkLog
        fields = [
            'date', 'duration_hours', 'activities', 'achievements',
            'difficulties', 'next_steps', 'resources_used', 'is_visible_to_supervisor'
        ]
        widgets = {
            'date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'duration_hours': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.5',
                'min': '0.5',
                'placeholder': 'Ex: 2.5'
            }),
            'activities': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Décrivez en détail ce que vous avez fait aujourd\'hui...'
            }),
            'achievements': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Objectifs atteints, résultats obtenus...'
            }),
            'difficulties': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Problèmes rencontrés, blocages, questions...'
            }),
            'next_steps': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Ce que vous prévoyez de faire ensuite...'
            }),
            'resources_used': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Documentation consultée, tutoriels, outils utilisés...'
            }),
            'is_visible_to_supervisor': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
        labels = {
            'date': 'Date',
            'duration_hours': 'Durée (heures)',
            'activities': 'Activités réalisées',
            'achievements': 'Réalisations / Résultats',
            'difficulties': 'Difficultés rencontrées',
            'next_steps': 'Prochaines étapes',
            'resources_used': 'Ressources utilisées',
            'is_visible_to_supervisor': 'Visible par mon encadreur',
        }
        help_texts = {
            'duration_hours': 'Nombre d\'heures travaillées (minimum 0.5h)',
            'is_visible_to_supervisor': 'Cochez pour partager cette entrée avec votre encadreur',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Date par défaut = aujourd'hui
        if not self.instance.pk:
            from django.utils import timezone
            self.initial['date'] = timezone.now().date()
            self.initial['is_visible_to_supervisor'] = True


class SupervisorFeedbackForm(forms.ModelForm):
    """Formulaire pour l'encadreur pour commenter une entrée du journal."""
    
    class Meta:
        model = WorkLog
        fields = ['supervisor_feedback']
        widgets = {
            'supervisor_feedback': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Vos commentaires et conseils pour l\'étudiant...'
            }),
        }
        labels = {
            'supervisor_feedback': 'Vos commentaires',
        }
