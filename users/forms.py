from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils.translation import gettext_lazy as _
from .models import User, Profile


class UserRegistrationForm(UserCreationForm):
    """Formulaire d'inscription des utilisateurs avec support ENSPD."""
    
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email'
        })
    )
    
    first_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Prénom'
        })
    )
    
    last_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nom'
        })
    )
    
    # Choix de rôles limités pour l'inscription publique (pas d'admin)
    PUBLIC_ROLE_CHOICES = [
        ('student', 'Étudiant'),
        ('teacher', 'Enseignant'),
    ]
    
    role = forms.ChoiceField(
        choices=PUBLIC_ROLE_CHOICES,
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'id_role'
        }),
        help_text='Les comptes administrateurs sont créés par les administrateurs existants.'
    )
    
    # Champ filière pour tous (étudiants/encadreurs = département)
    filiere = forms.ChoiceField(
        choices=[('', 'Sélectionnez une filière/département')] + list(User.FILIERE_CHOICES),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_filiere'})
    )
    
    # Champ filière administrée pour admin_filiere
    filiere_admin = forms.ChoiceField(
        choices=[('', 'Sélectionnez la filière à gérer')] + list(User.FILIERE_CHOICES),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_filiere_admin'}),
        label="Filière administrée"
    )
    
    # Champ titre académique pour encadreurs
    academic_title = forms.ChoiceField(
        choices=[('', 'Sélectionnez un grade académique')] + list(User.ACADEMIC_TITLE_CHOICES),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_academic_title'})
    )
    
    # Champ spécialité pour encadreurs
    specialite = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Spécialité', 'id': 'id_specialite'})
    )
    
    # Champ matricule pour étudiants
    matricule = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ex: 21G12345', 'id': 'id_matricule'})
    )
    
    # Champ niveau d'entrée pour étudiants
    entry_level = forms.ChoiceField(
        choices=[('', 'Sélectionnez votre niveau d\'entrée')] + list(User.ENTRY_LEVEL_CHOICES),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_entry_level'}),
        label="Niveau d'entrée à l'ENSPD"
    )
    
    # Champ niveau actuel pour étudiants (fixé à M2)
    level = forms.ChoiceField(
        choices=[('', 'Sélectionnez votre niveau actuel')] + list(User.LEVEL_CHOICES),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_level'}),
        label="Niveau actuel"
    )
    
    # Nombre maximum d'étudiants supervisés (pour encadreurs)
    max_students = forms.IntegerField(
        initial=5,
        min_value=1,
        max_value=10,
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'id': 'id_max_students'})
    )
    
    class Meta:
        model = User
        fields = [
            'username', 'email', 'first_name', 'last_name', 'role', 
            'matricule', 'entry_level', 'level', 'filiere', 'filiere_admin',
            'academic_title', 'specialite', 'max_students',
            'password1', 'password2'
        ]
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom d\'utilisateur'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Mot de passe'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirmer le mot de passe'
        })
    
    def clean_email(self):
        """Valider que l'email est unique."""
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Cette adresse email est déjà utilisée.')
        return email
    
    def clean(self):
        """Validation selon le rôle."""
        cleaned_data = super().clean()
        role = cleaned_data.get('role')
        
        if role == 'student':
            # Validation pour étudiants
            matricule = cleaned_data.get('matricule')
            entry_level = cleaned_data.get('entry_level')
            level = cleaned_data.get('level')
            
            if not matricule:
                self.add_error('matricule', 'Le matricule est obligatoire pour les étudiants.')
            if not entry_level:
                self.add_error('entry_level', 'Le niveau d\'entrée est obligatoire pour les étudiants.')
            if not level:
                self.add_error('level', 'Le niveau actuel est obligatoire pour les étudiants.')
            if not cleaned_data.get('filiere'):
                self.add_error('filiere', 'La filière est obligatoire pour les étudiants.')
            
            # Vérifier que le niveau actuel est M2 (seul niveau de soutenance)
            if level and level != 'M2':
                self.add_error('level', 'Seuls les étudiants de M2 peuvent s\'inscrire pour une soutenance.')
            
            # Vérifier la cohérence entre matricule, niveau d'entrée et année actuelle
            if matricule and entry_level:
                import re
                from datetime import datetime
                
                match = re.match(r'^(\d{2})G\d{5}$', matricule)
                if match:
                    entry_year_short = int(match.group(1))
                    # Convertir en année complète
                    entry_year = 2000 + entry_year_short if entry_year_short < 90 else 1900 + entry_year_short
                    current_year = datetime.now().year
                    years_since_entry = current_year - entry_year
                    
                    # Calculer l'année minimum de soutenance selon la formule:
                    # Année de soutenance min = Année d'entrée + (6 - niveau_entrée)
                    # - Entré niveau 1: 6 - 1 = 5 ans (ex: 21G soutient min en 2026)
                    # - Entré niveau 3: 6 - 3 = 3 ans (ex: 23G soutient min en 2026)
                    
                    # Année académique: Septembre année N à Juillet année N+1
                    # Un étudiant s'inscrit en année N pour soutenir en année N+1
                    # Donc on permet l'inscription 1 an avant la soutenance
                    
                    entry_level_num = int(entry_level)
                    min_years_required = 6 - entry_level_num
                    min_defense_year = entry_year + min_years_required
                    min_registration_year = min_defense_year - 1  # Inscription 1 an avant
                    
                    if current_year < min_registration_year:
                        self.add_error('matricule',
                            f'Avec un matricule {entry_year} et une entrée niveau {entry_level_num}, '
                            f'vous soutiendrez en {min_defense_year}. '
                            f'Vous pouvez vous inscrire à partir de {min_registration_year} (année académique {min_registration_year}-{min_defense_year}). '
                            f'(Année actuelle: {current_year})')
                    elif years_since_entry > 8:
                        self.add_error('matricule',
                            f'Le matricule {entry_year} est trop ancien ({years_since_entry} ans). '
                            f'Maximum: 8 ans.')
        
        elif role == 'teacher':
            # Validation pour enseignants
            if not cleaned_data.get('filiere'):
                self.add_error('filiere', 'Le département est obligatoire pour les enseignants.')
            if not cleaned_data.get('academic_title'):
                self.add_error('academic_title', 'Le grade académique est obligatoire pour les enseignants.')
            if not cleaned_data.get('specialite'):
                self.add_error('specialite', 'La spécialité est obligatoire pour les enseignants.')
        
        elif role == 'admin_filiere':
            # Validation pour admin de filière
            if not cleaned_data.get('filiere_admin'):
                self.add_error('filiere_admin', 'La filière administrée est obligatoire.')
        
        elif role == 'admin_general':
            # Admin général : pas de validation additionnelle
            pass
        
        return cleaned_data
    
    def save(self, commit=True):
        """Sauvegarder l'utilisateur avec le rôle et les champs ENSPD."""
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.role = self.cleaned_data['role']
        
        # Affecter les champs selon le rôle
        if user.role == 'student':
            user.matricule = self.cleaned_data.get('matricule')
            user.entry_level = self.cleaned_data.get('entry_level')
            user.level = self.cleaned_data.get('level')
            user.filiere = self.cleaned_data.get('filiere')
        
        elif user.role == 'teacher':
            user.filiere = self.cleaned_data.get('filiere')  # département
            user.academic_title = self.cleaned_data.get('academic_title')
            user.specialite = self.cleaned_data.get('specialite')
            user.max_students = self.cleaned_data.get('max_students', 5)
        
        elif user.role == 'admin_filiere':
            user.filiere_admin = self.cleaned_data.get('filiere_admin')
        
        elif user.role == 'admin_general':
            # Admin général : pas de champs additionnels
            pass
        
        if commit:
            user.save()
            # Le signal post_save créera automatiquement le profil
        return user


class UserLoginForm(AuthenticationForm):
    """Formulaire de connexion des utilisateurs."""
    
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nom d\'utilisateur'
        })
    )
    
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Mot de passe'
        })
    )


class UserUpdateForm(forms.ModelForm):
    """Formulaire de mise à jour du profil utilisateur."""
    
    # Redéfinir les champs avec des choix
    filiere = forms.ChoiceField(
        choices=User.FILIERE_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    academic_title = forms.ChoiceField(
        choices=User.ACADEMIC_TITLE_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    level = forms.ChoiceField(
        choices=User.LEVEL_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'email', 'phone', 
            'avatar', 'bio', 'matricule', 'level', 'filiere',
            'academic_title', 'specialite', 'max_students'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'avatar': forms.FileInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'matricule': forms.TextInput(attrs={'class': 'form-control'}),
            'specialite': forms.TextInput(attrs={'class': 'form-control'}),
            'max_students': forms.NumberInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = kwargs.get('instance')
        
        # Rendre certains champs conditionnels selon le rôle
        if user:
            if user.is_student():
                # Étudiants: matricule, level, filiere
                self.fields['academic_title'].widget = forms.HiddenInput()
                self.fields['specialite'].widget = forms.HiddenInput()
                self.fields['max_students'].widget = forms.HiddenInput()
            
            elif user.is_teacher():
                # Encadreurs: filiere (département), academic_title, specialite, max_students
                self.fields['matricule'].widget = forms.HiddenInput()
                self.fields['level'].widget = forms.HiddenInput()
            
            elif user.is_admin_filiere() or user.is_admin_general():
                # Admins: filiere (département) seulement
                self.fields['matricule'].widget = forms.HiddenInput()
                self.fields['level'].widget = forms.HiddenInput()
                self.fields['academic_title'].widget = forms.HiddenInput()
                self.fields['specialite'].widget = forms.HiddenInput()
                self.fields['max_students'].widget = forms.HiddenInput()


class ProfileUpdateForm(forms.ModelForm):
    """Formulaire de mise à jour des informations de profil."""
    
    class Meta:
        model = Profile
        fields = [
            'date_of_birth', 'address', 'city', 'country',
            'linkedin_url', 'github_url', 'website',
            'email_notifications', 'sms_notifications'
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'linkedin_url': forms.URLInput(attrs={'class': 'form-control'}),
            'github_url': forms.URLInput(attrs={'class': 'form-control'}),
            'website': forms.URLInput(attrs={'class': 'form-control'}),
            'email_notifications': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'sms_notifications': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
