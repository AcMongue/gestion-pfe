from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Project, Milestone, Deliverable, Comment
from .forms import ProjectForm, MilestoneForm, DeliverableForm, CommentForm


@login_required
def project_list_view(request):
    """Liste des projets avec statistiques."""
    from django.db.models import Q, Count, Avg
    from subjects.models import Assignment
    
    # Filtrer les projets selon le rôle
    if request.user.is_student():
        projects = Project.objects.filter(assignment__student=request.user)
        is_global_view = False
    elif request.user.is_teacher():
        projects = Project.objects.filter(assignment__subject__supervisor=request.user)
        is_global_view = False
    else:
        # Admin voit tous les projets
        projects = Project.objects.all()
        is_global_view = True
    
    # Appliquer les filtres pour l'admin
    status_filter = request.GET.get('status')
    supervisor_filter = request.GET.get('supervisor')
    
    if status_filter:
        projects = projects.filter(status=status_filter)
    if supervisor_filter:
        projects = projects.filter(assignment__subject__supervisor_id=supervisor_filter)
    
    # Sélectionner les relations nécessaires
    projects = projects.select_related(
        'assignment__student',
        'assignment__subject__supervisor'
    ).order_by('-created_at')
    
    # Statistiques pour l'admin
    context = {
        'projects': projects,
        'is_global_view': is_global_view,
    }
    
    if is_global_view:
        # Statistiques globales
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        total_projects = Project.objects.count()
        projects_by_status = {
            'in_progress': Project.objects.filter(status='in_progress').count(),
            'completed': Project.objects.filter(status='completed').count(),
            'pending': Project.objects.filter(status='pending').count(),
        }
        
        # Projets avec/sans soutenance
        projects_with_defense = Project.objects.filter(defense__isnull=False).count()
        projects_without_defense = total_projects - projects_with_defense
        
        # Liste des superviseurs pour filtre
        supervisors = User.objects.filter(
            role='teacher',
            proposed_subjects__assignments__project__isnull=False
        ).distinct().order_by('last_name', 'first_name')
        
        context.update({
            'total_projects': total_projects,
            'projects_by_status': projects_by_status,
            'projects_with_defense': projects_with_defense,
            'projects_without_defense': projects_without_defense,
            'supervisors': supervisors,
            'selected_status': status_filter,
            'selected_supervisor': supervisor_filter,
        })
    
    return render(request, 'projects/project_list.html', context)


@login_required
def project_detail_view(request, pk):
    """Détails d'un projet."""
    project = get_object_or_404(Project, pk=pk)
    
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.project = project
            comment.author = request.user
            comment.save()
            messages.success(request, "Commentaire ajouté.")
            return redirect('projects:detail', pk=pk)
    else:
        comment_form = CommentForm()
    
    return render(request, 'projects/project_detail.html', {
        'project': project,
        'comment_form': comment_form,
    })


@login_required
def project_update_view(request, pk):
    """Modification d'un projet."""
    project = get_object_or_404(Project, pk=pk)
    
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, "Projet mis à jour.")
            return redirect('projects:detail', pk=pk)
    else:
        form = ProjectForm(instance=project)
    
    return render(request, 'projects/project_form.html', {'form': form, 'project': project})


@login_required
def milestone_create_view(request, project_pk):
    """Création d'un jalon."""
    project = get_object_or_404(Project, pk=project_pk)
    
    if request.method == 'POST':
        form = MilestoneForm(request.POST)
        if form.is_valid():
            milestone = form.save(commit=False)
            milestone.project = project
            milestone.save()
            messages.success(request, "Jalon créé.")
            return redirect('projects:detail', pk=project_pk)
    else:
        form = MilestoneForm()
    
    return render(request, 'projects/milestone_form.html', {'form': form, 'project': project})


@login_required
def deliverable_submit_view(request, project_pk):
    """Soumission d'un livrable."""
    project = get_object_or_404(Project, pk=project_pk)
    
    if request.method == 'POST':
        form = DeliverableForm(request.POST, request.FILES)
        if form.is_valid():
            deliverable = form.save(commit=False)
            deliverable.project = project
            deliverable.submitted_by = request.user
            deliverable.save()
            messages.success(request, "Livrable soumis.")
            return redirect('projects:detail', pk=project_pk)
    else:
        form = DeliverableForm()
    
    return render(request, 'projects/deliverable_form.html', {'form': form, 'project': project})


@login_required
def my_projects_view(request):
    """Mes projets (étudiant ou encadreur)."""
    if request.user.is_student():
        projects = Project.objects.filter(assignment__student=request.user)
    elif request.user.is_teacher():
        projects = Project.objects.filter(assignment__subject__supervisor=request.user)
    else:
        projects = Project.objects.all()
    
    return render(request, 'projects/my_projects.html', {'projects': projects})


@login_required
def project_create_view(request):
    """Création d'un nouveau projet (admin/encadreur/étudiant)."""
    from subjects.models import Assignment
    
    # Récupérer l'affectation depuis l'URL si fournie
    assignment_id = request.GET.get('assignment')
    assignment = None
    initial_data = {}
    
    if assignment_id:
        assignment = get_object_or_404(Assignment, id=assignment_id)
        
        # Vérifier les permissions
        if request.user.is_student():
            if assignment.student != request.user:
                messages.error(request, "Cette affectation ne vous appartient pas.")
                return redirect('subjects:my_applications')
        elif request.user.is_teacher():
            if assignment.subject.supervisor != request.user:
                messages.error(request, "Vous n'encadrez pas ce sujet.")
                return redirect('subjects:my_subjects')
        
        # Pré-remplir avec les données de l'affectation
        initial_data = {
            'assignment': assignment,
            'title': assignment.subject.title,
            'description': assignment.subject.description,
            'objectives': assignment.subject.description,  # Peut être personnalisé
        }
    elif not (request.user.is_admin_staff() or request.user.is_teacher()):
        messages.error(request, "Vous devez avoir une affectation pour créer un projet.")
        return redirect('subjects:my_applications')
    
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, initial=initial_data)
        if form.is_valid():
            project = form.save()
            messages.success(request, f"Projet '{project.title}' créé avec succès.")
            
            # Créer des jalons par défaut
            if not project.milestones.exists():
                default_milestones = [
                    {'title': 'Analyse et spécification', 'description': 'Analyse des besoins et rédaction du cahier des charges', 'order': 1},
                    {'title': 'Conception', 'description': 'Architecture et conception détaillée du système', 'order': 2},
                    {'title': 'Développement', 'description': 'Implémentation des fonctionnalités principales', 'order': 3},
                    {'title': 'Tests et validation', 'description': 'Tests unitaires, d\'intégration et validation', 'order': 4},
                    {'title': 'Documentation et finalisation', 'description': 'Rédaction de la documentation et préparation de la soutenance', 'order': 5},
                ]
                
                from django.utils import timezone
                from datetime import timedelta
                start_date = project.start_date or timezone.now().date()
                
                for i, milestone_data in enumerate(default_milestones):
                    Milestone.objects.create(
                        project=project,
                        title=milestone_data['title'],
                        description=milestone_data['description'],
                        order=milestone_data['order'],
                        due_date=start_date + timedelta(days=30 * (i + 1)),  # Un mois par jalon
                        status='pending'
                    )
                
                messages.info(request, "5 jalons par défaut ont été créés. Vous pouvez les modifier.")
            
            return redirect('projects:detail', pk=project.pk)
    else:
        form = ProjectForm(initial=initial_data)
    
    context = {
        'form': form,
        'action': 'Créer',
        'assignment': assignment,
    }
    
    return render(request, 'projects/project_form.html', context)


@login_required
def deliverable_create_view(request, project_pk):
    """Création d'un livrable pour un projet."""
    project = get_object_or_404(Project, pk=project_pk)
    
    if request.method == 'POST':
        form = DeliverableForm(request.POST, request.FILES)
        if form.is_valid():
            deliverable = form.save(commit=False)
            deliverable.project = project
            deliverable.submitted_by = request.user
            deliverable.save()
            messages.success(request, "Livrable créé avec succès.")
            return redirect('projects:detail', pk=project_pk)
    else:
        form = DeliverableForm()
    
    return render(request, 'projects/deliverable_form.html', {'form': form, 'project': project})


@login_required
def deliverable_review_view(request, deliverable_pk):
    """Révision d'un livrable par le superviseur."""
    from .forms import DeliverableReviewForm
    from django.utils import timezone
    
    deliverable = get_object_or_404(Deliverable, pk=deliverable_pk)
    project = deliverable.project
    
    # Vérifier que l'utilisateur est le superviseur du projet
    if request.user != project.assignment.subject.supervisor and not request.user.is_admin_staff():
        messages.error(request, "Vous n'êtes pas autorisé à réviser ce livrable.")
        return redirect('projects:detail', pk=project.pk)
    
    if request.method == 'POST':
        form = DeliverableReviewForm(request.POST, instance=deliverable)
        if form.is_valid():
            deliverable = form.save(commit=False)
            deliverable.reviewed_by = request.user
            deliverable.reviewed_at = timezone.now()
            deliverable.save()
            messages.success(request, "Livrable révisé avec succès.")
            return redirect('projects:detail', pk=project.pk)
    else:
        form = DeliverableReviewForm(instance=deliverable)
    
    context = {
        'form': form,
        'deliverable': deliverable,
        'project': project,
    }
    return render(request, 'projects/deliverable_review.html', context)


@login_required
def milestone_validate_view(request, milestone_pk):
    """Validation d'un jalon par le superviseur."""
    from django.utils import timezone
    
    milestone = get_object_or_404(Milestone, pk=milestone_pk)
    project = milestone.project
    
    # Vérifier que l'utilisateur est le superviseur du projet
    if request.user != project.assignment.subject.supervisor and not request.user.is_admin_staff():
        messages.error(request, "Vous n'êtes pas autorisé à valider ce jalon.")
        return redirect('projects:detail', pk=project.pk)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        notes = request.POST.get('notes', '')
        
        if action == 'validate':
            milestone.validated_by_supervisor = True
            milestone.validation_date = timezone.now()
            milestone.status = 'completed'
            if notes:
                milestone.notes = notes
            milestone.save()
            messages.success(request, f"Jalon '{milestone.title}' validé avec succès.")
        elif action == 'reject':
            milestone.validated_by_supervisor = False
            milestone.validation_date = None
            milestone.status = 'in_progress'
            if notes:
                milestone.notes = notes
            milestone.save()
            messages.warning(request, f"Jalon '{milestone.title}' rejeté.")
        
        return redirect('projects:detail', pk=project.pk)
    
    context = {
        'milestone': milestone,
        'project': project,
    }
    return render(request, 'projects/milestone_validate.html', context)


@login_required
def milestone_update_view(request, milestone_pk):
    """Modification d'un jalon."""
    milestone = get_object_or_404(Milestone, pk=milestone_pk)
    project = milestone.project
    
    # Vérifier les permissions
    if not (request.user == project.assignment.student or 
            request.user == project.assignment.subject.supervisor or 
            request.user.is_admin_staff()):
        messages.error(request, "Vous n'êtes pas autorisé à modifier ce jalon.")
        return redirect('projects:detail', pk=project.pk)
    
    if request.method == 'POST':
        form = MilestoneForm(request.POST, instance=milestone)
        if form.is_valid():
            form.save()
            messages.success(request, "Jalon mis à jour avec succès.")
            return redirect('projects:detail', pk=project.pk)
    else:
        form = MilestoneForm(instance=milestone)
    
    context = {
        'form': form,
        'milestone': milestone,
        'project': project,
    }
    return render(request, 'projects/milestone_form.html', context)


@login_required
def supervisor_students_view(request):
    """Vue 'Mes Étudiants' pour l'encadreur."""
    if not request.user.is_teacher():
        messages.error(request, "Vous n'êtes pas autorisé à accéder à cette page.")
        return redirect('home')
    
    from django.db.models import Avg, Count, Q
    from subjects.models import Assignment
    
    # Récupérer tous les projets encadrés
    projects = Project.objects.filter(
        assignment__subject__supervisor=request.user
    ).select_related(
        'assignment__student',
        'assignment__subject'
    ).prefetch_related(
        'milestones',
        'deliverables'
    ).order_by('-updated_at')
    
    # Statistiques
    students_count = projects.count()
    active_projects_count = projects.filter(status='in_progress').count()
    
    # Calculer les items en attente
    pending_milestones = 0
    pending_deliverables = 0
    delayed_milestones = 0
    
    from django.utils import timezone
    today = timezone.now().date()
    
    for project in projects:
        # Jalons non validés mais complétés
        pending_milestones += project.milestones.filter(
            status='completed',
            validated_by_supervisor=False
        ).count()
        
        # Jalons en retard
        delayed_milestones += project.milestones.filter(
            due_date__lt=today
        ).exclude(status='completed').count()
        
        # Livrables soumis non révisés
        pending_deliverables += project.deliverables.filter(
            status='submitted'
        ).count()
    
    pending_items_count = pending_milestones + pending_deliverables
    
    # Progression moyenne
    average_progress = projects.aggregate(Avg('progress_percentage'))['progress_percentage__avg'] or 0
    
    # Annoter les projets avec des flags et compteurs
    for project in projects:
        project.milestones_pending = project.milestones.filter(
            status='completed',
            validated_by_supervisor=False
        ).exists()
        project.deliverables_pending = project.deliverables.filter(
            status='submitted'
        ).exists()
        # Ajouter les compteurs pour le template
        project.validated_milestones_count = project.milestones.filter(
            validated_by_supervisor=True
        ).count()
        project.approved_deliverables_count = project.deliverables.filter(
            status='approved'
        ).count()
    
    context = {
        'projects': projects,
        'students_count': students_count,
        'active_projects_count': active_projects_count,
        'pending_items_count': pending_items_count,
        'pending_milestones_count': pending_milestones,
        'pending_deliverables_count': pending_deliverables,
        'delayed_milestones': delayed_milestones,
        'average_progress': average_progress,
    }
    
    return render(request, 'projects/supervisor_students.html', context)


@login_required
def supervisor_student_detail_view(request, student_id):
    """Détail du suivi d'un étudiant par son encadreur."""
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    if not request.user.is_teacher():
        messages.error(request, "Vous n'êtes pas autorisé à accéder à cette page.")
        return redirect('home')
    
    student = get_object_or_404(User, id=student_id, role='student')
    
    # Vérifier que c'est bien un étudiant encadré
    project = get_object_or_404(
        Project,
        assignment__student=student,
        assignment__subject__supervisor=request.user
    )
    
    # Récupérer les données
    milestones = project.milestones.all().order_by('order', 'due_date')
    deliverables = project.deliverables.all().order_by('-submitted_at')
    comments = Comment.objects.filter(project=project).order_by('-created_at')[:10]
    
    # Statistiques
    total_milestones_count = milestones.count()
    validated_milestones_count = milestones.filter(validated_by_supervisor=True).count()
    pending_milestones_count = milestones.filter(
        status='completed',
        validated_by_supervisor=False
    ).count()
    
    total_deliverables_count = deliverables.count()
    approved_deliverables_count = deliverables.filter(status='approved').count()
    pending_deliverables_count = deliverables.filter(status='submitted').count()
    
    comments_count = Comment.objects.filter(project=project).count()
    
    # Activités récentes (simplifiée)
    recent_activities = []
    
    # Jalons récemment complétés
    for milestone in milestones.filter(status='completed').order_by('-completed_date')[:3]:
        recent_activities.append({
            'type': 'milestone',
            'type_class': 'primary',
            'description': f"Jalon complété: {milestone.title}",
            'created_at': milestone.completed_date or milestone.updated_at,
        })
    
    # Livrables récemment soumis
    for deliverable in deliverables[:3]:
        recent_activities.append({
            'type': 'deliverable',
            'type_class': 'success',
            'description': f"Livrable soumis: {deliverable.title}",
            'created_at': deliverable.submitted_at,
        })
    
    # Trier par date
    recent_activities = sorted(recent_activities, key=lambda x: x['created_at'], reverse=True)[:5]
    
    # Annoter les jalons
    from django.utils import timezone
    today = timezone.now().date()
    for milestone in milestones:
        if milestone.due_date < today and milestone.status != 'completed':
            milestone.is_overdue = True
            milestone.status_color = 'danger'
        elif milestone.validated_by_supervisor:
            milestone.status_color = 'success'
        elif milestone.status == 'completed':
            milestone.status_color = 'warning'
        else:
            milestone.status_color = 'secondary'
    
    context = {
        'student': student,
        'project': project,
        'milestones': milestones,
        'deliverables': deliverables,
        'comments': comments,
        'total_milestones_count': total_milestones_count,
        'validated_milestones_count': validated_milestones_count,
        'pending_milestones_count': pending_milestones_count,
        'total_deliverables_count': total_deliverables_count,
        'approved_deliverables_count': approved_deliverables_count,
        'pending_deliverables_count': pending_deliverables_count,
        'comments_count': comments_count,
        'recent_activities': recent_activities,
    }
    
    return render(request, 'projects/supervisor_student_detail.html', context)


@login_required
def project_evaluate_view(request, pk):
    """Évaluation du projet par l'encadreur."""
    project = get_object_or_404(Project, pk=pk)
    
    if not request.user.is_teacher() or project.assignment.subject.supervisor != request.user:
        messages.error(request, "Vous n'êtes pas autorisé à évaluer ce projet.")
        return redirect('projects:detail', pk=pk)
    
    if request.method == 'POST':
        supervisor_rating = request.POST.get('supervisor_rating')
        supervisor_notes = request.POST.get('supervisor_notes')
        
        if supervisor_rating:
            try:
                rating = float(supervisor_rating)
                if 0 <= rating <= 20:
                    project.supervisor_rating = rating
                else:
                    messages.error(request, "La note doit être entre 0 et 20.")
                    return redirect('projects:supervisor_student_detail', student_id=project.assignment.student.id)
            except ValueError:
                messages.error(request, "Note invalide.")
                return redirect('projects:supervisor_student_detail', student_id=project.assignment.student.id)
        
        project.supervisor_notes = supervisor_notes
        project.save()
        
        messages.success(request, "Évaluation enregistrée avec succès.")
        return redirect('projects:supervisor_student_detail', student_id=project.assignment.student.id)
    
    return redirect('projects:supervisor_student_detail', student_id=project.assignment.student.id)


@login_required
def project_kickoff_view(request, project_id):
    """Réunion de cadrage pour démarrer le projet."""
    from .models import Meeting
    from .forms import MilestoneForm
    
    project = get_object_or_404(Project, pk=project_id)
    
    # Vérifier les permissions
    if request.user.is_student():
        if project.assignment.student != request.user:
            messages.error(request, "Vous n'avez pas accès à ce projet.")
            return redirect('projects:my_projects')
    elif request.user.is_teacher():
        if project.assignment.subject.supervisor != request.user:
            messages.error(request, "Vous n'avez pas accès à ce projet.")
            return redirect('projects:supervisor_students')
    else:
        messages.error(request, "Accès non autorisé.")
        return redirect('home')
    
    # Vérifier que le projet est en attente de cadrage
    if project.status != 'awaiting_kickoff':
        messages.warning(request, "Ce projet a déjà été cadré.")
        return redirect('projects:detail', pk=project.id)
    
    if request.method == 'POST':
        # Seul l'encadreur peut finaliser le cadrage
        if not request.user.is_teacher():
            messages.error(request, "Seul l'encadreur peut finaliser le cadrage.")
            return redirect('projects:kickoff', project_id=project.id)
        
        # Créer la réunion de cadrage
        meeting_date = request.POST.get('meeting_date')
        meeting_location = request.POST.get('meeting_location')
        meeting_minutes = request.POST.get('meeting_minutes')
        decisions = request.POST.get('decisions')
        action_items = request.POST.get('action_items')
        next_meeting = request.POST.get('next_meeting')
        
        # Créer la réunion
        meeting = Meeting.objects.create(
            project=project,
            type='kickoff',
            scheduled_date=meeting_date,
            location=meeting_location,
            duration_minutes=60,
            minutes=meeting_minutes,
            decisions_made=decisions,
            action_items=action_items,
            next_meeting_date=next_meeting,
            status='completed'
        )
        
        # Passer le projet en cours
        project.status = 'in_progress'
        project.save()
        
        messages.success(request, "Réunion de cadrage enregistrée. Le projet est maintenant en cours!")
        
        # Notifier l'étudiant
        from communications.models import Notification
        Notification.objects.create(
            recipient=project.assignment.student,
            title="Projet démarré",
            message=f"Votre projet '{project.title}' est maintenant en cours!",
            type='project_update',
            related_object_type='project',
            related_object_id=project.id
        )
        
        return redirect('projects:detail', pk=project.id)
    
    # Afficher le formulaire
    context = {
        'project': project,
        'student': project.assignment.student,
        'supervisor': project.assignment.subject.supervisor,
    }
    
    return render(request, 'projects/kickoff_meeting.html', context)
