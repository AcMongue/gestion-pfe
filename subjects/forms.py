from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Subject, Application, Assignment


class SubjectCreateForm(forms.ModelForm):
    """Formulaire de création d'un sujet par un encadreur."""
    
    class Meta:
        model = Subject
        fields = [
            'title', 'description', 'objectives', 'prerequisites',
            'keywords', 'domain', 'type', 'level', 'co_supervisor',
            'max_students', 'status', 'available_from', 'available_until'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Titre du sujet'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Description détaillée du sujet'
            }),
            'objectives': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Objectifs du projet'
            }),
            'prerequisites': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Connaissances et compétences requises'
            }),
            'keywords': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Python, Django, Machine Learning'
            }),
            'domain': forms.Select(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
            'level': forms.Select(attrs={'class': 'form-control'}),
            'co_supervisor': forms.Select(attrs={'class': 'form-control'}),
            'max_students': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'max': '3'
            }),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'available_from': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'available_until': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
        }
        help_texts = {
            'status': _('Brouillon = non visible par les étudiants, Publié = visible dans le catalogue'),
        }


class SubjectUpdateForm(forms.ModelForm):
    """Formulaire de mise à jour d'un sujet."""
    
    class Meta:
        model = Subject
        fields = [
            'title', 'description', 'objectives', 'prerequisites',
            'keywords', 'domain', 'type', 'level', 'co_supervisor',
            'max_students', 'status', 'available_from', 'available_until'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'objectives': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'prerequisites': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'keywords': forms.TextInput(attrs={'class': 'form-control'}),
            'domain': forms.Select(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
            'level': forms.Select(attrs={'class': 'form-control'}),
            'co_supervisor': forms.Select(attrs={'class': 'form-control'}),
            'max_students': forms.NumberInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'available_from': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'available_until': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


class SubjectFilterForm(forms.Form):
    """Formulaire de filtrage des sujets."""
    
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Rechercher un sujet...'
        })
    )
    
    level = forms.ChoiceField(
        required=False,
        choices=[('', 'Tous les niveaux')] + Subject.LEVEL_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    domain = forms.ChoiceField(
        required=False,
        choices=[('', 'Tous les domaines')] + Subject.DOMAIN_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    type = forms.ChoiceField(
        required=False,
        choices=[('', 'Tous les types')] + Subject.TYPE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )


class ApplicationForm(forms.ModelForm):
    """Formulaire de candidature à un sujet."""
    
    PRIORITY_CHOICES = [
        (1, '1 - Priorité maximale (choix préféré)'),
        (2, '2 - Haute priorité'),
        (3, '3 - Priorité moyenne'),
        (4, '4 - Basse priorité'),
        (5, '5 - Priorité minimale'),
    ]
    
    priority = forms.ChoiceField(
        choices=PRIORITY_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label=_('Priorité de cette candidature'),
        help_text=_('Indiquez à quel point ce sujet vous intéresse'),
        initial=1
    )
    
    class Meta:
        model = Application
        fields = ['motivation_letter', 'cv_file', 'priority']
        widgets = {
            'motivation_letter': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': 'Expliquez pourquoi vous souhaitez travailler sur ce sujet, vos compétences et votre motivation...'
            }),
            'cv_file': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.doc,.docx'
            }),
        }
        labels = {
            'motivation_letter': _('Lettre de motivation'),
            'cv_file': _('CV (facultatif)'),
        }


class ApplicationReviewForm(forms.ModelForm):
    """Formulaire d'évaluation d'une candidature par l'encadreur."""
    
    class Meta:
        model = Application
        fields = ['status', 'review_notes']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
            'review_notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Notes sur la candidature...'
            }),
        }


class AssignmentForm(forms.ModelForm):
    """Formulaire de création d'une affectation."""
    
    class Meta:
        model = Assignment
        fields = ['subject', 'student', 'start_date', 'expected_end_date', 'notes']
        widgets = {
            'subject': forms.Select(attrs={'class': 'form-control'}),
            'student': forms.Select(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'expected_end_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
        }
