from django import forms
from .models import ArchivedProject, Report

class ArchiveProjectForm(forms.ModelForm):
    """Formulaire pour archiver un projet"""
    class Meta:
        model = ArchivedProject
        fields = ['project', 'year', 'semester', 'final_grade', 'archived_by']
        widgets = {
            'project': forms.Select(attrs={'class': 'form-select'}),
            'year': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 2024'}),
            'semester': forms.Select(attrs={'class': 'form-select'}),
            'final_grade': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 20, 'step': 0.5}),
            'archived_by': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'project': 'Projet',
            'year': 'Année académique',
            'semester': 'Semestre',
            'final_grade': 'Note finale (/20)',
            'archived_by': 'Archivé par',
        }


class ReportGenerationForm(forms.Form):
    """Formulaire pour générer un rapport"""
    REPORT_TYPES = [
        ('annual', 'Rapport annuel'),
        ('semester', 'Rapport semestriel'),
        ('supervisor', 'Rapport par encadreur'),
        ('statistics', 'Statistiques générales'),
    ]
    
    report_type = forms.ChoiceField(
        choices=REPORT_TYPES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Type de rapport'
    )
    academic_year = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 2023-2024'}),
        label='Année académique (optionnel)'
    )
    semester = forms.ChoiceField(
        choices=[('', '-- Tous --'), ('S1', 'Semestre 1'), ('S2', 'Semestre 2')],
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Semestre (optionnel)'
    )
