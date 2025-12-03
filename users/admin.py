from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User, Profile


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Administration personnalisée pour le modèle User."""
    
    list_display = ['username', 'email', 'first_name', 'last_name', 'role', 'matricule', 'is_active']
    list_filter = ['role', 'level', 'is_active', 'is_staff', 'created_at']
    search_fields = ['username', 'email', 'first_name', 'last_name', 'matricule']
    ordering = ['-created_at']
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Informations personnelles'), {
            'fields': ('first_name', 'last_name', 'email', 'phone', 'avatar', 'bio')
        }),
        (_('Rôle et statut'), {
            'fields': ('role', 'is_active', 'is_staff', 'is_superuser')
        }),
        (_('Informations étudiant'), {
            'fields': ('matricule', 'level', 'filiere'),
            'classes': ('collapse',)
        }),
        (_('Informations encadreur'), {
            'fields': ('specialite', 'grade'),
            'classes': ('collapse',)
        }),
        (_('Permissions'), {
            'fields': ('groups', 'user_permissions'),
            'classes': ('collapse',)
        }),
        (_('Dates importantes'), {
            'fields': ('last_login', 'date_joined', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at', 'last_login', 'date_joined']
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'role'),
        }),
    )


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Administration pour le modèle Profile."""
    
    list_display = ['user', 'city', 'country', 'email_notifications']
    list_filter = ['country', 'email_notifications', 'sms_notifications']
    search_fields = ['user__username', 'user__email', 'city']
    ordering = ['-created_at']
    
    fieldsets = (
        (_('Utilisateur'), {
            'fields': ('user',)
        }),
        (_('Informations personnelles'), {
            'fields': ('date_of_birth', 'address', 'city', 'country')
        }),
        (_('Réseaux sociaux'), {
            'fields': ('linkedin_url', 'github_url', 'website')
        }),
        (_('Paramètres de notification'), {
            'fields': ('email_notifications', 'sms_notifications')
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']
