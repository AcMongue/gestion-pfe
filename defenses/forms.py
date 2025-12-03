from django import forms
from .models import Defense, JuryMember, DefenseEvaluation

class DefenseForm(forms.ModelForm):
    """Formulaire pour planifier une soutenance"""
    class Meta:
        model = Defense
        fields = ['project', 'date', 'time', 'room', 'duration', 'status']
        widgets = {
            'project': forms.HiddenInput(),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'room': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Salle A101'}),
            'duration': forms.NumberInput(attrs={'class': 'form-control', 'value': 45, 'min': 15, 'max': 180}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'date': 'Date de soutenance',
            'time': 'Heure',
            'room': 'Salle',
            'duration': 'Durée (minutes)',
            'status': 'Statut',
        }


class JuryMemberForm(forms.ModelForm):
    """Formulaire pour ajouter un membre du jury"""
    class Meta:
        model = JuryMember
        fields = ['user', 'role']
        widgets = {
            'user': forms.Select(attrs={'class': 'form-select'}),
            'role': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'user': 'Membre du jury',
            'role': 'Rôle',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrer pour ne montrer que les encadreurs et jurys
        from users.models import User
        self.fields['user'].queryset = User.objects.filter(
            role__in=['supervisor', 'jury']
        )


class DefenseEvaluationForm(forms.ModelForm):
    """Formulaire pour évaluer une soutenance"""
    class Meta:
        model = DefenseEvaluation
        fields = [
            'presentation_quality', 'content_mastery', 'technical_skills',
            'communication', 'answers_quality', 'overall_impression', 
            'strengths', 'weaknesses', 'recommendations'
        ]
        widgets = {
            'presentation_quality': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 20}),
            'content_mastery': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 20}),
            'technical_skills': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 20}),
            'communication': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 20}),
            'answers_quality': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 20}),
            'overall_impression': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Impression générale...'}),
            'strengths': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Points forts...'}),
            'weaknesses': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Points à améliorer...'}),
            'recommendations': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Recommandations...'}),
        }
        labels = {
            'presentation_quality': 'Qualité de la présentation (/20)',
            'content_mastery': 'Maîtrise du contenu (/20)',
            'technical_skills': 'Compétences techniques (/20)',
            'communication': 'Communication (/20)',
            'answers_quality': 'Qualité des réponses (/20)',
            'overall_impression': 'Impression générale',
            'strengths': 'Points forts',
            'weaknesses': 'Points à améliorer',
            'recommendations': 'Recommandations',
        }
