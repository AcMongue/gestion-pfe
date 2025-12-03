from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Project, Milestone, Deliverable, Comment


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
