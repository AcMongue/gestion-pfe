from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import CreateView
from django.urls import reverse_lazy
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
        # Tableau de bord étudiant
        return render(request, 'users/dashboard_student.html', context)
    elif user.is_supervisor():
        # Tableau de bord encadreur
        return render(request, 'users/dashboard_supervisor.html', context)
    elif user.is_admin_staff():
        # Tableau de bord administration
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


def home_view(request):
    """Vue de la page d'accueil."""
    if request.user.is_authenticated:
        return redirect('users:dashboard')
    return render(request, 'home.html')
