from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.db.models import Q
from django.core.mail import send_mail, BadHeaderError, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.http import HttpResponse
from .forms import UserRegistrationForm, UserLoginForm, UserUpdateForm, ProfileUpdateForm
from .models import User, Profile


def register_view(request):
    """Vue pour l'inscription d'un nouvel utilisateur."""
    if request.user.is_authenticated:
        return redirect('users:dashboard')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Créer automatiquement un profil pour l'utilisateur
            Profile.objects.create(user=user)
            messages.success(request, 'Compte créé avec succès ! Vous pouvez maintenant vous connecter.')
            return redirect('users:login')
        else:
            # DEBUG: Afficher les erreurs dans la console
            print("\n" + "="*80)
            print("ERREURS DE VALIDATION DU FORMULAIRE D'INSCRIPTION")
            print("="*80)
            print(f"Données POST reçues: {dict(request.POST)}")
            print(f"\nErreurs du formulaire:")
            for field, errors in form.errors.items():
                print(f"  - Champ '{field}': {errors}")
            if form.non_field_errors():
                print(f"\nErreurs générales: {form.non_field_errors()}")
            print("="*80 + "\n")
    else:
        form = UserRegistrationForm()
    
    return render(request, 'users/register.html', {'form': form})


def login_view(request):
    """Vue pour la connexion d'un utilisateur."""
    if request.user.is_authenticated:
        return redirect('users:dashboard')
    
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Bienvenue, {user.get_full_name()} !')
                return redirect('users:dashboard')
    else:
        form = UserLoginForm()
    
    return render(request, 'users/login.html', {'form': form})


@login_required
def logout_view(request):
    """Vue pour la déconnexion d'un utilisateur."""
    logout(request)
    messages.info(request, 'Vous avez été déconnecté avec succès.')
    return redirect('users:login')


@login_required
def dashboard_view(request):
    """Vue du tableau de bord principal selon le rôle de l'utilisateur."""
    user = request.user
    context = {
        'user': user
    }
    
    if user.is_student():
        # Tableau de bord étudiant - Ajouter les données nécessaires
        from subjects.models import Subject, Application, Assignment
        from projects.models import Project
        from communications.models import Message, Notification
        
        # Affectation de l'étudiant
        assignment = Assignment.objects.filter(student=user).first()
        
        # Sujets disponibles
        available_subjects = Subject.objects.filter(status='available')
        
        # Candidatures de l'étudiant
        applications = Application.objects.filter(student=user)
        
        # Notifications non lues
        unread_notifications = Notification.objects.filter(user=user, is_read=False).count()
        
        context.update({
            'assignment': assignment,
            'available_subjects_count': available_subjects.count(),
            'applications': applications,
            'applications_count': applications.count(),
            'unread_notifications': unread_notifications,
        })
        
        return render(request, 'users/dashboard_student.html', context)
        
    elif user.is_teacher():
        # Tableau de bord enseignant - Ajouter les données nécessaires
        from subjects.models import Subject, Application, Assignment
        from projects.models import Project
        from communications.models import Message, Notification
        
        # Sujets proposés par l'encadreur
        my_subjects = Subject.objects.filter(supervisor=user)
        
        # Candidatures en attente sur mes sujets
        pending_applications = Application.objects.filter(
            subject__supervisor=user,
            status='pending'
        )
        
        # Projets encadrés
        supervised_projects = Project.objects.filter(assignment__subject__supervisor=user)
        
        # Messages non lus
        unread_messages = Message.objects.filter(recipient=user, is_read=False).count()
        
        # Propositions reçues en attente
        from subjects.models import StudentProposal
        pending_proposals = StudentProposal.objects.filter(
            status='pending'
        ).filter(
            Q(preferred_supervisor_1=user) |
            Q(preferred_supervisor_2=user) |
            Q(preferred_supervisor_3=user)
        )
        
        context.update({
            'my_subjects': my_subjects,
            'my_subjects_count': my_subjects.count(),
            'pending_applications': pending_applications,
            'pending_applications_count': pending_applications.count(),
            'supervised_projects': supervised_projects,
            'supervised_projects_count': supervised_projects.count(),
            'unread_messages': unread_messages,
            'pending_proposals_count': pending_proposals.count(),
        })
        
        return render(request, 'users/dashboard_supervisor.html', context)
        
    elif user.is_admin_staff():
        # Tableau de bord administration - Ajouter les statistiques globales
        from subjects.models import Subject, Application, Assignment
        from projects.models import Project
        from defenses.models import Defense
        
        # Statistiques globales
        total_users = User.objects.count()
        total_students = User.objects.filter(role='student').count()
        total_supervisors = User.objects.filter(role='supervisor').count()
        total_subjects = Subject.objects.count()
        total_applications = Application.objects.count()
        pending_applications = Application.objects.filter(status='pending').count()
        total_assignments = Assignment.objects.count()
        total_projects = Project.objects.count()
        total_defenses = Defense.objects.count()
        
        context.update({
            'total_users': total_users,
            'total_students': total_students,
            'total_supervisors': total_supervisors,
            'total_subjects': total_subjects,
            'total_applications': total_applications,
            'pending_applications': pending_applications,
            'total_assignments': total_assignments,
            'total_projects': total_projects,
            'total_defenses': total_defenses,
        })
        
        return render(request, 'users/dashboard_admin.html', context)
    elif user.is_jury_member():
        # Tableau de bord jury
        return render(request, 'users/dashboard_jury.html', context)
    else:
        return render(request, 'users/dashboard.html', context)


@login_required
def profile_view(request):
    """Vue pour afficher le profil de l'utilisateur."""
    # Créer un profil s'il n'existe pas
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    context = {
        'user': request.user,
        'profile': profile
    }
    return render(request, 'users/profile.html', context)


@login_required
def profile_edit_view(request):
    """Vue pour modifier le profil de l'utilisateur."""
    # Créer un profil s'il n'existe pas
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, instance=profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Votre profil a été mis à jour avec succès !')
            return redirect('users:profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=profile)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'users/profile_edit.html', context)


@login_required
def user_list_view(request):
    """Liste moderne des utilisateurs avec filtres et recherche."""
    if not (request.user.is_admin_staff() or request.user.is_superuser):
        messages.error(request, "Vous n'avez pas accès à cette page.")
        return redirect('users:dashboard')
    
    # Récupérer les paramètres de filtre
    role_filter = request.GET.get('role', '')
    filiere_filter = request.GET.get('filiere', '')
    search_query = request.GET.get('search', '')
    status_filter = request.GET.get('status', '')
    
    # Base queryset
    users = User.objects.all().select_related('profile')
    
    # Filtrer par rôle
    if role_filter:
        users = users.filter(role=role_filter)
    
    # Filtrer par filière (pour étudiants et enseignants)
    if filiere_filter:
        users = users.filter(filiere=filiere_filter) | users.filter(filiere_admin=filiere_filter)
    
    # Filtrer par statut actif/inactif
    if status_filter == 'active':
        users = users.filter(is_active=True)
    elif status_filter == 'inactive':
        users = users.filter(is_active=False)
    
    # Recherche par nom, email, username
    if search_query:
        from django.db.models import Q
        users = users.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(username__icontains=search_query) |
            Q(matricule__icontains=search_query)
        )
    
    # Statistiques
    stats = {
        'total': User.objects.count(),
        'students': User.objects.filter(role='student').count(),
        'teachers': User.objects.filter(role='teacher').count(),
        'admin_filiere': User.objects.filter(role='admin_filiere').count(),
        'admin_general': User.objects.filter(role='admin_general').count(),
        'active': User.objects.filter(is_active=True).count(),
        'inactive': User.objects.filter(is_active=False).count(),
    }
    
    # Ordre par date de création (plus récent en premier)
    users = users.order_by('-created_at')
    
    context = {
        'users': users,
        'stats': stats,
        'role_filter': role_filter,
        'filiere_filter': filiere_filter,
        'search_query': search_query,
        'status_filter': status_filter,
        'filiere_choices': User.FILIERE_CHOICES,
        'role_choices': User.ROLE_CHOICES,
    }
    return render(request, 'users/user_list.html', context)


@login_required
def user_detail_view(request, pk):
    """Détails d'un utilisateur."""
    user = get_object_or_404(User, pk=pk)
    profile = Profile.objects.get_or_create(user=user)[0]
    
    context = {
        'viewed_user': user,
        'profile': profile
    }
    return render(request, 'users/user_detail.html', context)


def home_view(request):
    """Vue de la page d'accueil."""
    if request.user.is_authenticated:
        return redirect('users:dashboard')
    return render(request, 'home.html')


@login_required
def create_admin_user_view(request):
    """Création d'un compte administrateur (admin_general uniquement)."""
    if not request.user.is_admin_general():
        messages.error(request, "Seuls les administrateurs généraux peuvent créer des comptes administrateurs.")
        return redirect('users:user_list')
    
    if request.method == 'POST':
        role = request.POST.get('role')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        filiere_admin = request.POST.get('filiere_admin')
        
        # Validation
        if not all([role, first_name, last_name, email, username]):
            messages.error(request, "Tous les champs sont obligatoires.")
            return render(request, 'users/create_admin_user.html', {
                'filiere_choices': User.FILIERE_CHOICES
            })
        
        # Vérifier que le rôle est bien admin
        if role not in ['admin_filiere', 'admin_general']:
            messages.error(request, "Vous ne pouvez créer que des comptes administrateurs.")
            return render(request, 'users/create_admin_user.html', {
                'filiere_choices': User.FILIERE_CHOICES
            })
        
        # Vérifier l'unicité
        if User.objects.filter(username=username).exists():
            messages.error(request, f"Le nom d'utilisateur '{username}' existe déjà.")
            return render(request, 'users/create_admin_user.html', {
                'filiere_choices': User.FILIERE_CHOICES
            })
        
        if User.objects.filter(email=email).exists():
            messages.error(request, f"L'email '{email}' est déjà utilisé.")
            return render(request, 'users/create_admin_user.html', {
                'filiere_choices': User.FILIERE_CHOICES
            })
        
        # Valider filiere_admin pour admin_filiere
        if role == 'admin_filiere' and not filiere_admin:
            messages.error(request, "La filière administrée est obligatoire pour un admin de filière.")
            return render(request, 'users/create_admin_user.html', {
                'filiere_choices': User.FILIERE_CHOICES
            })
        
        try:
            # Générer un mot de passe temporaire
            import secrets
            import string
            alphabet = string.ascii_letters + string.digits
            temp_password = ''.join(secrets.choice(alphabet) for _ in range(12))
            
            # Créer l'utilisateur
            user = User.objects.create_user(
                username=username,
                email=email,
                password=temp_password,
                first_name=first_name,
                last_name=last_name,
                role=role
            )
            
            # Assigner la filière pour admin_filiere
            if role == 'admin_filiere':
                user.filiere_admin = filiere_admin
                user.save()
            
            messages.success(
                request,
                f"✅ Compte créé avec succès !\n"
                f"Username: {username}\n"
                f"Mot de passe temporaire: {temp_password}\n"
                f"⚠️ Notez ce mot de passe, il ne sera plus affiché."
            )
            
            # TODO: Envoyer un email avec les identifiants
            
            return redirect('users:user_list')
            
        except Exception as e:
            messages.error(request, f"Erreur lors de la création: {e}")
    
    context = {
        'filiere_choices': User.FILIERE_CHOICES
    }
    return render(request, 'users/create_admin_user.html', context)


@login_required
def toggle_user_active_view(request, pk):
    """Activer/désactiver un utilisateur."""
    if not request.user.is_admin_general():
        messages.error(request, "Seuls les administrateurs généraux peuvent activer/désactiver des comptes.")
        return redirect('users:user_list')
    
    user = get_object_or_404(User, pk=pk)
    
    # Empêcher de se désactiver soi-même
    if user == request.user:
        messages.error(request, "Vous ne pouvez pas désactiver votre propre compte.")
        return redirect('users:user_list')
    
    # Toggle
    user.is_active = not user.is_active
    user.save()
    
    status = "activé" if user.is_active else "désactivé"
    messages.success(request, f"Le compte de {user.get_full_name()} a été {status}.")
    
    return redirect('users:user_list')


@login_required
def reset_user_password_view(request, pk):
    """Réinitialiser le mot de passe d'un utilisateur."""
    if not request.user.is_admin_general():
        messages.error(request, "Seuls les administrateurs généraux peuvent réinitialiser les mots de passe.")
        return redirect('users:user_list')
    
    user = get_object_or_404(User, pk=pk)
    
    if request.method == 'POST':
        # Générer un nouveau mot de passe temporaire
        import secrets
        import string
        alphabet = string.ascii_letters + string.digits
        new_password = ''.join(secrets.choice(alphabet) for _ in range(12))
        
        user.set_password(new_password)
        user.save()
        
        messages.success(
            request,
            f"✅ Mot de passe réinitialisé pour {user.get_full_name()} !\n"
            f"Nouveau mot de passe: {new_password}\n"
            f"⚠️ Notez ce mot de passe, il ne sera plus affiché."
        )
        
        # TODO: Envoyer un email avec le nouveau mot de passe
        
        return redirect('users:user_list')
    
    context = {'viewed_user': user}
    return render(request, 'users/reset_password_confirm.html', context)


def password_reset_request(request):
    """Formulaire de demande de réinitialisation de mot de passe."""
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        
        if not username or not email:
            messages.error(request, "Veuillez remplir tous les champs.")
            return render(request, 'users/password_reset.html')
        
        # SÉCURITÉ : Chercher un compte avec username ET email correspondants
        # Cela identifie de manière unique le compte même si l'email est partagé
        try:
            user = User.objects.get(username=username, email=email)
            
            # Générer et envoyer l'email de réinitialisation
            subject = "Réinitialisation de mot de passe - GradEase"
            context = {
                "email": user.email,
                'domain': request.META.get('HTTP_HOST', 'localhost:8000'),
                'site_name': 'GradEase',
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "user": user,
                'token': default_token_generator.make_token(user),
                'protocol': 'https' if request.is_secure() else 'http',
                'username': user.username,
            }
            
            # Créer la version texte
            text_content = render_to_string("users/password_reset_email.txt", context)
            # Créer la version HTML
            html_content = render_to_string("users/password_reset_email.html", context)
            
            try:
                from django.conf import settings
                # Créer un email multipart (texte + HTML)
                email_message = EmailMultiAlternatives(
                    subject,
                    text_content,
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email]
                )
                email_message.attach_alternative(html_content, "text/html")
                email_message.send(fail_silently=False)
                
                print(f"✅ Email de réinitialisation envoyé à {user.email} (compte: {user.username})")
            except Exception as e:
                print(f"❌ Erreur lors de l'envoi de l'email: {e}")
                import traceback
                print(traceback.format_exc())
        
        except User.DoesNotExist:
            # SÉCURITÉ : Ne pas révéler si le username ou l'email n'existe pas
            # Afficher le même message de succès pour éviter l'énumération
            pass
        except User.MultipleObjectsReturned:
            # Cas impossible normalement car username est unique
            print(f"⚠️ ERREUR CRITIQUE: Plusieurs comptes avec username={username}")
        
        # TOUJOURS afficher le même message de succès
        # Que le compte existe ou non, pour des raisons de sécurité
        messages.success(
            request,
            "Si un compte correspond à ces informations, vous recevrez un lien de réinitialisation."
        )
        return redirect('users:password_reset_done')
    
    return render(request, 'users/password_reset.html')


@login_required
def change_password_view(request):
    """Permet à un utilisateur de changer son propre mot de passe."""
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # Important : garder l'utilisateur connecté après changement de mot de passe
            update_session_auth_hash(request, user)
            messages.success(
                request, 
                '✅ Votre mot de passe a été changé avec succès !'
            )
            return redirect('users:profile')
        else:
            messages.error(
                request, 
                '❌ Erreur lors du changement de mot de passe. Vérifiez les informations saisies.'
            )
    else:
        form = PasswordChangeForm(request.user)
    
    context = {'form': form}
    return render(request, 'users/change_password.html', context)
