from django import forms
from django.db.models import Q
from .models import Defense, JuryMember, DefenseEvaluation, DefenseChangeRequest, Room


class RoomForm(forms.ModelForm):
    """Formulaire pour créer/modifier une salle (liste déroulante)"""
    
    class Meta:
        model = Room
        fields = ['name', 'filiere', 'capacity', 'is_available']
        widgets = {
            'name': forms.Select(attrs={
                'class': 'form-select',
                'placeholder': 'Sélectionnez une salle'
            }),
            'filiere': forms.Select(attrs={'class': 'form-select'}),
            'capacity': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'placeholder': 'Nombre de places'
            }),
            'is_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'name': '<i class="fas fa-door-closed"></i> Salle',
            'filiere': '<i class="fas fa-university"></i> Filière prioritaire',
            'capacity': '<i class="fas fa-chair"></i> Capacité',
            'is_available': '<i class="fas fa-toggle-on"></i> Disponible',
        }
        help_texts = {
            'name': 'Sélectionnez une salle dans la liste (BS = Bloc des Spécialités, BP = Bloc Pédagogique)',
            'filiere': 'Filière qui utilisera prioritairement cette salle',
            'capacity': 'Nombre de places assises disponibles',
        }
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Si admin de filière, limiter les choix de filière
        if self.user and self.user.is_admin_filiere():
            self.fields['filiere'].choices = [
                (self.user.filiere_admin, dict(Room.FILIERE_CHOICES)[self.user.filiere_admin])
            ]
            self.fields['filiere'].initial = self.user.filiere_admin
            self.fields['filiere'].widget.attrs['readonly'] = True


class DefenseForm(forms.ModelForm):
    """Formulaire pour planifier une soutenance"""
    
    room_obj = forms.ModelChoiceField(
        queryset=Room.objects.filter(is_available=True),
        required=False,
        label='Salle',
        widget=forms.Select(attrs={'class': 'form-select'}),
        help_text='Sélectionnez une salle disponible'
    )
    
    class Meta:
        model = Defense
        fields = ['project', 'date', 'time', 'room', 'room_obj', 'duration', 'status']
        widgets = {
            'project': forms.HiddenInput(),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'room': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Salle A101 (obsolète)'}),
            'duration': forms.NumberInput(attrs={'class': 'form-control', 'value': 45, 'min': 15, 'max': 180}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'date': '<i class="far fa-calendar"></i> Date de soutenance',
            'time': '<i class="far fa-clock"></i> Heure',
            'room': '<i class="fas fa-location-dot"></i> Salle (texte libre - obsolète)',
            'duration': '<i class="fas fa-stopwatch"></i> Durée (minutes)',
            'status': '<i class="fas fa-flag"></i> Statut',
        }
    
    def __init__(self, *args, **kwargs):
        filiere = kwargs.pop('filiere', None)
        super().__init__(*args, **kwargs)
        
        # Filtrer les salles par filière si fourni
        if filiere:
            self.fields['room_obj'].queryset = Room.objects.filter(
                is_available=True
            ).filter(
                Q(filiere=filiere) | Q(filiere='GENERAL')
            ).order_by('filiere', 'name')
        else:
            self.fields['room_obj'].queryset = Room.objects.filter(
                is_available=True
            ).order_by('filiere', 'name')
    
    def clean(self):
        cleaned_data = super().clean()
        room_obj = cleaned_data.get('room_obj')
        date = cleaned_data.get('date')
        time = cleaned_data.get('time')
        duration = cleaned_data.get('duration')
        
        # Vérifier la disponibilité de la salle
        if room_obj and date and time and duration:
            if not room_obj.is_available_for_defense(date, time, duration):
                raise forms.ValidationError(
                    f"La salle {room_obj.name} n'est pas disponible pour ce créneau horaire."
                )
        
        return cleaned_data


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
            'user': '<i class="fas fa-user-graduate"></i> Membre du jury',
            'role': '<i class="fas fa-id-badge"></i> Rôle',
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
            'presentation_quality': '<i class="fas fa-chalkboard-user"></i> Qualité de la présentation (/20)',
            'content_mastery': '<i class="fas fa-book-open"></i> Maîtrise du contenu (/20)',
            'technical_skills': '<i class="fas fa-laptop-code"></i> Compétences techniques (/20)',
            'communication': '<i class="fas fa-message"></i> Communication (/20)',
            'answers_quality': '<i class="fas fa-circle-question"></i> Qualité des réponses (/20)',
            'overall_impression': '<i class="far fa-star"></i> Impression générale',
            'strengths': '<i class="fas fa-circle-check"></i> Points forts',
            'weaknesses': '<i class="fas fa-triangle-exclamation"></i> Points à améliorer',
            'recommendations': '<i class="far fa-lightbulb"></i> Recommandations',
        }


class DefenseUpdateForm(forms.ModelForm):
    """Formulaire pour modifier une soutenance (admin)"""
    class Meta:
        model = Defense
        fields = ['date', 'time', 'room_obj', 'duration', 'status']
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'room_obj': forms.Select(attrs={'class': 'form-select'}),
            'duration': forms.NumberInput(attrs={'class': 'form-control', 'min': 15, 'max': 180}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'room_obj': 'Salle',
        }


class DefenseChangeRequestForm(forms.ModelForm):
    """Formulaire pour suggérer une modification de soutenance"""
    class Meta:
        model = DefenseChangeRequest
        fields = ['proposed_date', 'proposed_time', 'proposed_location', 'reason']
        widgets = {
            'proposed_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'placeholder': 'Laisser vide pour ne pas changer'
            }),
            'proposed_time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time',
                'placeholder': 'Laisser vide pour ne pas changer'
            }),
            'proposed_location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nouvelle salle (optionnel)'
            }),
            'reason': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Expliquez pourquoi vous souhaitez modifier la soutenance...',
                'required': True
            }),
        }
        labels = {
            'proposed_date': '<i class="far fa-calendar-plus"></i> Nouvelle date proposée (optionnel)',
            'proposed_time': '<i class="far fa-clock"></i> Nouvelle heure proposée (optionnel)',
            'proposed_location': '<i class="fas fa-location-dot"></i> Nouveau lieu proposé (optionnel)',
            'reason': '<i class="fas fa-pen-to-square"></i> Motif de la demande',
        }


class DefenseChangeReviewForm(forms.ModelForm):
    """Formulaire pour examiner une demande de modification"""
    class Meta:
        model = DefenseChangeRequest
        fields = ['status', 'review_comment']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
            'review_comment': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Commentaire (optionnel)...'
            }),
        }
        labels = {
            'status': '<i class="fas fa-scale-balanced"></i> Décision',
            'review_comment': '<i class="far fa-comment"></i> Commentaire',
        }
