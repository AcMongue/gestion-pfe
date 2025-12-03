from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from django.utils import timezone
from .models import Subject, Application, Assignment
from .forms import (
    SubjectCreateForm, SubjectUpdateForm, SubjectFilterForm,
    ApplicationForm, ApplicationReviewForm, AssignmentForm
)


# ============= VUES POUR LES SUJETS =============

@login_required
def subject_list_view(request):
    """Liste des sujets disponibles avec filtres."""
    subjects = Subject.objects.filter(status='published').select_related('supervisor', 'co_supervisor')
    
    # Filtrage
    filter_form = SubjectFilterForm(request.GET)
    if filter_form.is_valid():
        search = filter_form.cleaned_data.get('search')
        level = filter_form.cleaned_data.get('level')
        domain = filter_form.cleaned_data.get('domain')
        type_ = filter_form.cleaned_data.get('type')
        
        if search:
            subjects = subjects.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search) |
                Q(keywords__icontains=search)
            )
        if level:
            subjects = subjects.filter(level=level)
        if domain:
            subjects = subjects.filter(domain=domain)
        if type_:
            subjects = subjects.filter(type=type_)
    
    # Filtrer par niveau de l'étudiant si c'est un étudiant
    if request.user.is_student():
        if request.user.level:
            subjects = subjects.filter(level=request.user.level)
        # Si pas de niveau défini, montrer tous les sujets avec un message
    
    # Annoter avec le nombre de candidatures
    subjects = subjects.annotate(applications_count=Count('applications'))
    
    context = {
        'subjects': subjects,
        'filter_form': filter_form,
        'total_count': subjects.count()
    }
    return render(request, 'subjects/subject_list.html', context)


@login_required
def subject_detail_view(request, pk):
    """Détails d'un sujet."""
    subject = get_object_or_404(Subject, pk=pk)
    
    # Vérifier si l'utilisateur a déjà candidaté
    has_applied = False
    user_application = None
    if request.user.is_student():
        has_applied = Application.objects.filter(
            subject=subject,
            student=request.user
        ).exists()
        if has_applied:
            user_application = Application.objects.get(subject=subject, student=request.user)
    
    # Vérifier si l'étudiant a déjà une affectation
    has_assignment = False
    if request.user.is_student():
        has_assignment = Assignment.objects.filter(
            student=request.user,
            status='active'
        ).exists()
    
    context = {
        'subject': subject,
        'has_applied': has_applied,
        'user_application': user_application,
        'has_assignment': has_assignment
    }
    return render(request, 'subjects/subject_detail.html', context)


@login_required
def subject_create_view(request):
    """Création d'un nouveau sujet (encadreurs uniquement)."""
    if not request.user.is_supervisor():
        messages.error(request, 'Seuls les encadreurs peuvent proposer des sujets.')
        return redirect('subjects:list')
    
    if request.method == 'POST':
        form = SubjectCreateForm(request.POST)
        if form.is_valid():
            subject = form.save(commit=False)
            subject.supervisor = request.user
            subject.save()
            messages.success(request, 'Sujet créé avec succès !')
            return redirect('subjects:my_subjects')
    else:
        form = SubjectCreateForm()
    
    context = {'form': form}
    return render(request, 'subjects/subject_form.html', context)


@login_required
def subject_update_view(request, pk):
    """Mise à jour d'un sujet (propriétaire uniquement)."""
    subject = get_object_or_404(Subject, pk=pk)
    
    # Vérifier que l'utilisateur est le superviseur
    if subject.supervisor != request.user:
        messages.error(request, 'Vous ne pouvez modifier que vos propres sujets.')
        return redirect('subjects:detail', pk=pk)
    
    if request.method == 'POST':
        form = SubjectUpdateForm(request.POST, instance=subject)
        if form.is_valid():
            form.save()
            messages.success(request, 'Sujet mis à jour avec succès !')
            return redirect('subjects:detail', pk=pk)
    else:
        form = SubjectUpdateForm(instance=subject)
    
    context = {'form': form, 'subject': subject}
    return render(request, 'subjects/subject_form.html', context)


@login_required
def subject_delete_view(request, pk):
    """Suppression d'un sujet (propriétaire uniquement)."""
    subject = get_object_or_404(Subject, pk=pk)
    
    if subject.supervisor != request.user:
        messages.error(request, 'Vous ne pouvez supprimer que vos propres sujets.')
        return redirect('subjects:detail', pk=pk)
    
    if request.method == 'POST':
        subject.delete()
        messages.success(request, 'Sujet supprimé avec succès !')
        return redirect('subjects:my_subjects')
    
    context = {'subject': subject}
    return render(request, 'subjects/subject_confirm_delete.html', context)


@login_required
def my_subjects_view(request):
    """Liste des sujets de l'encadreur connecté."""
    if not request.user.is_supervisor():
        messages.error(request, 'Cette page est réservée aux encadreurs.')
        return redirect('subjects:list')
    
    subjects = Subject.objects.filter(
        supervisor=request.user
    ).annotate(
        applications_count=Count('applications', filter=Q(applications__status='pending'))
    ).order_by('-created_at')
    
    context = {'subjects': subjects}
    return render(request, 'subjects/my_subjects.html', context)


# ============= VUES POUR LES CANDIDATURES =============

@login_required
def application_create_view(request, subject_pk):
    """Candidature à un sujet (étudiants uniquement)."""
    if not request.user.is_student():
        messages.error(request, 'Seuls les étudiants peuvent candidater.')
        return redirect('subjects:detail', pk=subject_pk)
    
    subject = get_object_or_404(Subject, pk=subject_pk)
    
    # Vérifications
    if not subject.is_available():
        messages.error(request, 'Ce sujet n\'est plus disponible.')
        return redirect('subjects:detail', pk=subject_pk)
    
    if Application.objects.filter(subject=subject, student=request.user).exists():
        messages.warning(request, 'Vous avez déjà candidaté à ce sujet.')
        return redirect('subjects:detail', pk=subject_pk)
    
    if Assignment.objects.filter(student=request.user, status='active').exists():
        messages.error(request, 'Vous avez déjà un sujet affecté.')
        return redirect('subjects:detail', pk=subject_pk)
    
    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.subject = subject
            application.student = request.user
            application.save()
            messages.success(request, 'Votre candidature a été envoyée avec succès !')
            return redirect('subjects:my_applications')
    else:
        form = ApplicationForm()
    
    context = {'form': form, 'subject': subject}
    return render(request, 'subjects/application_form.html', context)


@login_required
def my_applications_view(request):
    """Liste des candidatures de l'étudiant connecté."""
    if not request.user.is_student():
        messages.error(request, 'Cette page est réservée aux étudiants.')
        return redirect('subjects:list')
    
    applications = Application.objects.filter(
        student=request.user
    ).select_related('subject', 'subject__supervisor').order_by('-created_at')
    
    context = {'applications': applications}
    return render(request, 'subjects/my_applications.html', context)


@login_required
def application_withdraw_view(request, pk):
    """Retirer une candidature."""
    application = get_object_or_404(Application, pk=pk)
    
    if application.student != request.user:
        messages.error(request, 'Vous ne pouvez retirer que vos propres candidatures.')
        return redirect('subjects:my_applications')
    
    if application.status != 'pending':
        messages.error(request, 'Cette candidature ne peut plus être retirée.')
        return redirect('subjects:my_applications')
    
    if request.method == 'POST':
        application.status = 'withdrawn'
        application.save()
        messages.success(request, 'Candidature retirée avec succès.')
        return redirect('subjects:my_applications')
    
    context = {'application': application}
    return render(request, 'subjects/application_confirm_withdraw.html', context)


@login_required
def subject_applications_view(request, subject_pk):
    """Liste des candidatures pour un sujet (encadreur uniquement)."""
    subject = get_object_or_404(Subject, pk=subject_pk)
    
    if subject.supervisor != request.user:
        messages.error(request, 'Vous ne pouvez voir que les candidatures pour vos sujets.')
        return redirect('subjects:detail', pk=subject_pk)
    
    applications = Application.objects.filter(
        subject=subject
    ).select_related('student').order_by('status', '-priority', '-created_at')
    
    context = {'subject': subject, 'applications': applications}
    return render(request, 'subjects/subject_applications.html', context)


@login_required
def application_review_view(request, pk):
    """Évaluation d'une candidature (encadreur uniquement)."""
    application = get_object_or_404(Application, pk=pk)
    
    if application.subject.supervisor != request.user:
        messages.error(request, 'Vous ne pouvez évaluer que les candidatures pour vos sujets.')
        return redirect('subjects:my_subjects')
    
    if request.method == 'POST':
        form = ApplicationReviewForm(request.POST, instance=application)
        if form.is_valid():
            app = form.save(commit=False)
            app.reviewed_by = request.user
            app.reviewed_at = timezone.now()
            app.save()
            messages.success(request, 'Évaluation enregistrée avec succès !')
            return redirect('subjects:subject_applications', subject_pk=application.subject.pk)
    else:
        form = ApplicationReviewForm(instance=application)
    
    context = {'form': form, 'application': application}
    return render(request, 'subjects/application_review.html', context)
