from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Subject, Application, Assignment


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    """Administration pour le modèle Subject."""
    
    list_display = [
        'title', 'supervisor', 'level', 'filiere', 'type', 
        'status', 'max_students', 'get_applications_count', 'created_at'
    ]
    list_filter = ['status', 'level', 'filiere', 'type', 'is_interdisciplinary', 'created_at']
    search_fields = ['title', 'description', 'keywords', 'supervisor__username']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        (_('Informations générales'), {
            'fields': ('title', 'description', 'objectives', 'prerequisites', 'keywords')
        }),
        (_('Classification'), {
            'fields': ('filiere', 'type', 'level', 'is_interdisciplinary', 'additional_filieres')
        }),
        (_('Encadrement'), {
            'fields': ('supervisor', 'co_supervisor', 'max_students')
        }),
        (_('Disponibilité'), {
            'fields': ('status', 'available_from', 'available_until')
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']
    
    def get_applications_count(self, obj):
        """Affiche le nombre de candidatures."""
        return obj.get_applications_count()
    get_applications_count.short_description = 'Candidatures'
    
    def get_queryset(self, request):
        """Personnalise le queryset selon l'utilisateur."""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        # Les encadreurs voient uniquement leurs sujets
        if request.user.role == 'teacher':
            return qs.filter(supervisor=request.user)
        return qs


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    """Administration pour le modèle Application."""
    
    list_display = [
        'student', 'subject', 'status', 'priority', 
        'reviewed_by', 'created_at'
    ]
    list_filter = ['status', 'priority', 'created_at', 'reviewed_at']
    search_fields = [
        'student__username', 'student__first_name', 'student__last_name',
        'subject__title'
    ]
    ordering = ['-created_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        (_('Candidature'), {
            'fields': ('subject', 'student', 'motivation_letter', 'cv_file', 'priority')
        }),
        (_('Évaluation'), {
            'fields': ('status', 'reviewed_by', 'reviewed_at', 'review_notes')
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']
    
    def get_queryset(self, request):
        """Personnalise le queryset selon l'utilisateur."""
        qs = super().get_queryset(request)
        if request.user.is_superuser or request.user.role == 'admin':
            return qs
        # Les encadreurs voient les candidatures pour leurs sujets
        if request.user.role == 'teacher':
            return qs.filter(subject__supervisor=request.user)
        # Les étudiants voient leurs propres candidatures
        if request.user.role == 'student':
            return qs.filter(student=request.user)
        return qs


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    """Administration pour le modèle Assignment."""
    
    list_display = [
        'student', 'subject', 'status', 'assigned_by', 
        'start_date', 'expected_end_date', 'created_at'
    ]
    list_filter = ['status', 'start_date', 'created_at']
    search_fields = [
        'student__username', 'student__first_name', 'student__last_name',
        'subject__title'
    ]
    ordering = ['-created_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        (_('Affectation'), {
            'fields': ('subject', 'student', 'application', 'status')
        }),
        (_('Dates'), {
            'fields': ('start_date', 'expected_end_date')
        }),
        (_('Informations complémentaires'), {
            'fields': ('assigned_by', 'notes')
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']
    
    def get_queryset(self, request):
        """Personnalise le queryset selon l'utilisateur."""
        qs = super().get_queryset(request)
        if request.user.is_superuser or request.user.role == 'admin':
            return qs
        # Les encadreurs voient les affectations pour leurs sujets
        if request.user.role == 'teacher':
            return qs.filter(subject__supervisor=request.user)
        # Les étudiants voient leur propre affectation
        if request.user.role == 'student':
            return qs.filter(student=request.user)
        return qs
