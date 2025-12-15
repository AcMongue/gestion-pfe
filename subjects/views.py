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
        filiere = filter_form.cleaned_data.get('filiere')
        type_ = filter_form.cleaned_data.get('type')
        
        if search:
            subjects = subjects.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search) |
                Q(keywords__icontains=search)
            )
        if level:
            subjects = subjects.filter(level=level)
        if filiere:
            subjects = subjects.filter(filiere=filiere)
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
    if not request.user.is_teacher():
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
    if not request.user.is_teacher():
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
def assignment_detail_view(request, pk):
    """Détails d'une affectation."""
    assignment = get_object_or_404(Assignment, pk=pk)
    
    # Vérifier les permissions
    if not (request.user == assignment.student or 
            request.user == assignment.subject.supervisor or 
            request.user.is_admin_staff()):
        messages.error(request, "Vous n'êtes pas autorisé à voir cette affectation.")
        return redirect('subjects:list')
    
    context = {
        'assignment': assignment,
    }
    return render(request, 'subjects/assignment_detail.html', context)


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


# ============= VUES POUR LES AFFECTATIONS (ADMIN) =============

@login_required
def assignments_manage_view(request):
    """Gestion des affectations (admin uniquement)."""
    if not request.user.is_admin_staff():
        messages.error(request, 'Cette page est réservée aux administrateurs.')
        return redirect('users:dashboard')
    
    # Récupérer toutes les candidatures acceptées sans affectation
    pending_applications = Application.objects.filter(
        status='accepted'
    ).select_related('student', 'subject', 'subject__supervisor')
    
    # Vérifier lesquelles n'ont pas encore d'affectation active
    pending_list = []
    for app in pending_applications:
        has_assignment = Assignment.objects.filter(
            student=app.student,
            status='active'
        ).exists()
        if not has_assignment:
            pending_list.append(app)
    
    # Récupérer toutes les affectations existantes
    assignments = Assignment.objects.all().select_related(
        'student', 'subject', 'subject__supervisor', 'assigned_by'
    ).order_by('-created_at')
    
    context = {
        'pending_applications': pending_list,
        'assignments': assignments,
    }
    return render(request, 'subjects/assignments_manage.html', context)


@login_required
def assignment_create_view(request, application_pk):
    """Créer une affectation à partir d'une candidature (admin uniquement)."""
    if not request.user.is_admin_staff():
        messages.error(request, 'Seuls les administrateurs peuvent créer des affectations.')
        return redirect('users:dashboard')
    
    application = get_object_or_404(Application, pk=application_pk)
    
    # Vérifications
    if application.status != 'accepted':
        messages.error(request, 'Seules les candidatures acceptées peuvent être affectées.')
        return redirect('subjects:assignments_manage')
    
    # Vérifier si l'étudiant a déjà une affectation active
    if Assignment.objects.filter(student=application.student, status='active').exists():
        messages.error(request, 'Cet étudiant a déjà un sujet affecté.')
        return redirect('subjects:assignments_manage')
    
    # Vérifier si le sujet est déjà affecté
    if Assignment.objects.filter(subject=application.subject, status='active').exists():
        messages.error(request, 'Ce sujet est déjà affecté à un autre étudiant.')
        return redirect('subjects:assignments_manage')
    
    if request.method == 'POST':
        # Créer l'affectation
        assignment = Assignment.objects.create(
            student=application.student,
            subject=application.subject,
            assigned_by=request.user,
            status='active',
            notes=request.POST.get('notes', '')
        )
        
        # Mettre à jour le statut du sujet
        application.subject.status = 'assigned'
        application.subject.save()
        
        # Rejeter toutes les autres candidatures pour ce sujet
        Application.objects.filter(
            subject=application.subject
        ).exclude(pk=application.pk).update(status='rejected')
        
        messages.success(request, f'Sujet affecté à {application.student.get_full_name()} avec succès !')
        return redirect('subjects:assignments_manage')
    
    context = {'application': application}
    return render(request, 'subjects/assignment_create.html', context)


@login_required
def assignment_cancel_view(request, pk):
    """Annuler une affectation (admin uniquement)."""
    if not request.user.is_admin_staff():
        messages.error(request, 'Seuls les administrateurs peuvent annuler des affectations.')
        return redirect('users:dashboard')
    
    assignment = get_object_or_404(Assignment, pk=pk)
    
    if request.method == 'POST':
        # Mettre à jour le statut
        assignment.status = 'cancelled'
        assignment.save()
        
        # Remettre le sujet en published
        assignment.subject.status = 'published'
        assignment.subject.save()
        
        messages.success(request, 'Affectation annulée avec succès.')
        return redirect('subjects:assignments_manage')
    
    context = {'assignment': assignment}
    return render(request, 'subjects/assignment_cancel.html', context)


# ============= VUES POUR LES PROPOSITIONS D'ÉTUDIANTS =============

@login_required
def student_proposal_create_view(request):
    """Permet à un étudiant de proposer son propre sujet."""
    from .models import StudentProposal
    from .forms import StudentProposalForm
    
    if not request.user.is_student():
        messages.error(request, "Seuls les étudiants peuvent proposer des sujets.")
        return redirect('subjects:list')
    
    # Vérifier si l'étudiant n'a pas déjà une affectation
    if Assignment.objects.filter(student=request.user, status='accepted').exists():
        messages.warning(request, "Vous avez déjà une affectation acceptée.")
        return redirect('subjects:my_applications')
    
    # Vérifier si l'étudiant n'a pas déjà une proposition en attente
    if StudentProposal.objects.filter(student=request.user, status='pending').exists():
        messages.warning(request, "Vous avez déjà une proposition en attente de révision.")
        return redirect('subjects:my_proposals')
    
    if request.method == 'POST':
        form = StudentProposalForm(request.POST)
        if form.is_valid():
            proposal = form.save(commit=False)
            proposal.student = request.user
            proposal.save()
            
            messages.success(
                request,
                f"Votre proposition '{proposal.title}' a été soumise avec succès. "
                f"Les encadreurs sélectionnés seront notifiés."
            )
            return redirect('subjects:my_proposals')
    else:
        form = StudentProposalForm()
    
    context = {
        'form': form,
        'action': 'Créer',
    }
    return render(request, 'subjects/proposal_form.html', context)


@login_required
def student_proposal_list_view(request):
    """Liste des propositions pour l'étudiant."""
    from .models import StudentProposal
    
    if not request.user.is_student():
        messages.error(request, "Accès refusé.")
        return redirect('home')
    
    proposals = StudentProposal.objects.filter(student=request.user).order_by('-created_at')
    
    context = {
        'proposals': proposals,
    }
    return render(request, 'subjects/my_proposals.html', context)


@login_required
def supervisor_proposals_view(request):
    """Liste des propositions pour l'encadreur."""
    from .models import StudentProposal
    
    if not request.user.is_teacher():
        messages.error(request, "Seuls les encadreurs peuvent accéder à cette page.")
        return redirect('home')
    
    # Propositions où l'encadreur est dans les choix
    proposals = StudentProposal.objects.filter(
        Q(preferred_supervisor_1=request.user) |
        Q(preferred_supervisor_2=request.user) |
        Q(preferred_supervisor_3=request.user)
    ).select_related('student').order_by('-created_at')
    
    # Filtrer par statut si spécifié
    status_filter = request.GET.get('status', '')
    if status_filter:
        proposals = proposals.filter(status=status_filter)
    
    context = {
        'proposals': proposals,
        'status_filter': status_filter,
        'total_count': proposals.count(),
    }
    return render(request, 'subjects/supervisor_proposals.html', context)


@login_required
def proposal_detail_view(request, pk):
    """Détail d'une proposition."""
    from .models import StudentProposal
    
    proposal = get_object_or_404(StudentProposal, pk=pk)
    
    # Vérifier les permissions
    if request.user.is_student():
        if proposal.student != request.user:
            messages.error(request, "Vous n'êtes pas autorisé à voir cette proposition.")
            return redirect('subjects:my_proposals')
    elif request.user.is_teacher():
        if request.user not in proposal.get_preferred_supervisors():
            messages.error(request, "Vous n'êtes pas autorisé à voir cette proposition.")
            return redirect('subjects:supervisor_proposals')
    elif not request.user.is_admin_staff():
        messages.error(request, "Accès refusé.")
        return redirect('home')
    
    context = {
        'proposal': proposal,
    }
    return render(request, 'subjects/proposal_detail.html', context)


@login_required
def proposal_accept_view(request, pk):
    """Accepter une proposition d'étudiant."""
    from .models import StudentProposal
    
    proposal = get_object_or_404(StudentProposal, pk=pk)
    
    if not request.user.is_teacher():
        messages.error(request, "Seuls les encadreurs peuvent accepter des propositions.")
        return redirect('home')
    
    if not proposal.can_be_accepted_by(request.user):
        messages.error(request, "Vous ne pouvez pas accepter cette proposition.")
        return redirect('subjects:supervisor_proposals')
    
    if request.method == 'POST':
        comments = request.POST.get('comments', '')
        
        proposal.status = 'accepted'
        proposal.accepted_by = request.user
        proposal.supervisor_comments = comments
        proposal.reviewed_at = timezone.now()
        proposal.save()
        
        messages.success(
            request,
            f"Vous avez accepté d'encadrer le projet '{proposal.title}'. "
            f"Une affectation a été créée automatiquement."
        )
        return redirect('subjects:supervisor_proposals')
    
    context = {
        'proposal': proposal,
        'action': 'accepter',
    }
    return render(request, 'subjects/proposal_review.html', context)


@login_required
def proposal_reject_view(request, pk):
    """Rejeter une proposition d'étudiant."""
    from .models import StudentProposal
    
    proposal = get_object_or_404(StudentProposal, pk=pk)
    
    if not request.user.is_teacher():
        messages.error(request, "Seuls les encadreurs peuvent rejeter des propositions.")
        return redirect('home')
    
    if not proposal.can_be_accepted_by(request.user):
        messages.error(request, "Vous ne pouvez pas rejeter cette proposition.")
        return redirect('subjects:supervisor_proposals')
    
    if request.method == 'POST':
        comments = request.POST.get('comments', '')
        
        # Si c'était le dernier encadreur potentiel, rejeter complètement
        proposal.supervisor_comments = comments
        proposal.reviewed_at = timezone.now()
        
        # Pour l'instant, on ne rejette pas complètement, juste pour cet encadreur
        # On pourrait implémenter un système de rejet par encadreur
        messages.info(
            request,
            f"Vous avez décliné la proposition '{proposal.title}'."
        )
        return redirect('subjects:supervisor_proposals')
    
    context = {
        'proposal': proposal,
        'action': 'rejeter',
    }
    return render(request, 'subjects/proposal_review.html', context)
