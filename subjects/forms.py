from django import forms
from django.utils.translation import gettext_lazy as _
from users.models import User
from .models import Subject, Application, Assignment


class SubjectCreateForm(forms.ModelForm):
    """Formulaire de création d'un sujet par un encadreur."""
    
    # Champ pour les filières additionnelles (projets interdisciplinaires)
    additional_filieres = forms.MultipleChoiceField(
        choices=User.FILIERE_CHOICES,
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label='Filières additionnelles',
        help_text='Sélectionnez les autres filières pouvant candidater (projets interdisciplinaires)'
    )
    
    class Meta:
        model = Subject
        fields = [
            'title', 'description', 'objectives', 'prerequisites',
            'keywords', 'filiere', 'type', 'level', 'is_interdisciplinary',
            'co_supervisor', 'max_students', 'status', 
            'available_from', 'available_until'
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
            'filiere': forms.Select(attrs={
                'class': 'form-control',
                'readonly': 'readonly'
            }),
            'type': forms.Select(attrs={'class': 'form-control'}),
            'level': forms.Select(attrs={'class': 'form-control'}),
            'is_interdisciplinary': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
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
            'filiere': _('Filière héritée de votre département'),
            'is_interdisciplinary': _('Cochez pour ouvrir le sujet à d\'autres filières'),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # La filière est automatiquement celle de l'encadreur
        if hasattr(self, 'instance') and hasattr(self.instance, 'supervisor'):
            self.fields['filiere'].initial = self.instance.supervisor.filiere
    
    def save(self, commit=True):
        subject = super().save(commit=False)
        # Sauvegarder les filières additionnelles
        if 'additional_filieres' in self.cleaned_data:
            subject.additional_filieres = self.cleaned_data['additional_filieres']
        if commit:
            subject.save()
        return subject


class SubjectUpdateForm(forms.ModelForm):
    """Formulaire de mise à jour d'un sujet."""
    
    # Champ pour les filières additionnelles (projets interdisciplinaires)
    additional_filieres = forms.MultipleChoiceField(
        choices=User.FILIERE_CHOICES,
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label='Filières additionnelles',
        help_text='Sélectionnez les autres filières pouvant candidater (projets interdisciplinaires)'
    )
    
    class Meta:
        model = Subject
        fields = [
            'title', 'description', 'objectives', 'prerequisites',
            'keywords', 'filiere', 'type', 'level', 'is_interdisciplinary',
            'co_supervisor', 'max_students', 'status', 
            'available_from', 'available_until'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'objectives': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'prerequisites': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'keywords': forms.TextInput(attrs={'class': 'form-control'}),
            'filiere': forms.Select(attrs={
                'class': 'form-control',
                'readonly': 'readonly'
            }),
            'type': forms.Select(attrs={'class': 'form-control'}),
            'level': forms.Select(attrs={'class': 'form-control'}),
            'is_interdisciplinary': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'co_supervisor': forms.Select(attrs={'class': 'form-control'}),
            'max_students': forms.NumberInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'available_from': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'available_until': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Pré-remplir les filières additionnelles si elles existent
        if self.instance and self.instance.additional_filieres:
            self.fields['additional_filieres'].initial = self.instance.additional_filieres
    
    def save(self, commit=True):
        subject = super().save(commit=False)
        # Sauvegarder les filières additionnelles
        if 'additional_filieres' in self.cleaned_data:
            subject.additional_filieres = self.cleaned_data['additional_filieres']
        if commit:
            subject.save()
        return subject


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
    
    filiere = forms.ChoiceField(
        required=False,
        choices=[('', 'Toutes les filières')] + Subject.FILIERE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Filière'
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


class StudentProposalForm(forms.ModelForm):
    """Formulaire pour qu'un étudiant propose son propre sujet."""
    
    class Meta:
        from .models import StudentProposal
        model = StudentProposal
        
        fields = [
            'title', 'description', 'objectives', 'methodology',
            'technologies', 'filiere', 'type',
            'preferred_supervisor_1', 'preferred_supervisor_2', 'preferred_supervisor_3',
            'supervisor_justification'
        ]
        
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Titre de votre projet',
                'required': True
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Décrivez votre idée de projet en détail...',
                'required': True
            }),
            'objectives': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Quels sont les objectifs que vous visez avec ce projet ?',
                'required': True
            }),
            'methodology': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Comment comptez-vous réaliser ce projet ? Quelle méthodologie ?'
            }),
            'technologies': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Python, Django, React, PostgreSQL, Docker'
            }),
            'filiere': forms.Select(attrs={'class': 'form-select'}),
            'type': forms.Select(attrs={'class': 'form-select'}),
            'preferred_supervisor_1': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'preferred_supervisor_2': forms.Select(attrs={'class': 'form-select'}),
            'preferred_supervisor_3': forms.Select(attrs={'class': 'form-select'}),
            'supervisor_justification': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Pourquoi avez-vous choisi ces encadreurs pour votre projet ?'
            }),
        }
        
        labels = {
            'title': 'Titre du projet',
            'description': 'Description détaillée',
            'objectives': 'Objectifs du projet',
            'methodology': 'Méthodologie envisagée',
            'technologies': 'Technologies à utiliser',
            'filiere': 'Filière',
            'type': 'Type de projet',
            'preferred_supervisor_1': '1er choix d\'encadreur (obligatoire)',
            'preferred_supervisor_2': '2ème choix d\'encadreur (optionnel)',
            'preferred_supervisor_3': '3ème choix d\'encadreur (optionnel)',
            'supervisor_justification': 'Pourquoi ces encadreurs ?',
        }
        
        help_texts = {
            'title': 'Donnez un titre clair et concis à votre projet',
            'description': 'Expliquez en détail votre idée, le contexte et les motivations',
            'objectives': 'Listez les objectifs concrets que vous souhaitez atteindre',
            'methodology': 'Décrivez les étapes que vous prévoyez de suivre',
            'technologies': 'Listez les technologies que vous comptez utiliser',
            'preferred_supervisor_1': 'Choisissez au moins un encadreur',
            'supervisor_justification': 'Expliquez pourquoi vous pensez que ces encadreurs sont adaptés à votre projet',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Limiter les choix aux enseignants uniquement
        from users.models import User
        teachers = User.objects.filter(role='teacher', is_active=True)
        self.fields['preferred_supervisor_1'].queryset = teachers
        self.fields['preferred_supervisor_2'].queryset = teachers
        self.fields['preferred_supervisor_3'].queryset = teachers
    
    def clean(self):
        cleaned_data = super().clean()
        sup1 = cleaned_data.get('preferred_supervisor_1')
        sup2 = cleaned_data.get('preferred_supervisor_2')
        sup3 = cleaned_data.get('preferred_supervisor_3')
        
        # Vérifier que les encadreurs sont différents
        supervisors = [sup for sup in [sup1, sup2, sup3] if sup]
        if len(supervisors) != len(set(supervisors)):
            raise forms.ValidationError("Vous devez choisir des encadreurs différents.")
        
        return cleaned_data
