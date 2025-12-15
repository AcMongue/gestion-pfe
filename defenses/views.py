from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Avg
from django.utils import timezone
from datetime import datetime
from .models import Defense, JuryMember, DefenseEvaluation, DefenseChangeRequest, Room
from .forms import (DefenseForm, JuryMemberForm, DefenseEvaluationForm,
                    DefenseUpdateForm, DefenseChangeRequestForm, DefenseChangeReviewForm, RoomForm)
from projects.models import Project

@login_required
def defense_list_view(request):
    """Liste toutes les soutenances avec filtres par salle et date"""
    if request.user.role == 'student':
        # Les étudiants voient seulement leurs propres soutenances
        defenses = Defense.objects.filter(
            project__assignment__student=request.user
        )
    elif request.user.role == 'teacher':
        # Les encadreurs voient les soutenances de leurs projets
        defenses = Defense.objects.filter(
            project__assignment__subject__supervisor=request.user
        )
    elif request.user.role in ['admin_filiere', 'admin_general', 'jury']:
        # Admins et jurys voient tout
        defenses = Defense.objects.all()
    else:
        defenses = Defense.objects.none()
    
    # Filtres GET
    room_id = request.GET.get('room')
    date_filter = request.GET.get('date')
    status_filter = request.GET.get('status')
    
    if room_id:
        defenses = defenses.filter(room_obj_id=room_id)
    
    if date_filter:
        try:
            filter_date = datetime.strptime(date_filter, '%Y-%m-%d').date()
            defenses = defenses.filter(date=filter_date)
        except ValueError:
            pass
    
    if status_filter:
        defenses = defenses.filter(status=status_filter)
    
    defenses = defenses.select_related('project', 'room_obj').order_by('-date', '-time')
    
    # Listes pour les filtres
    rooms = Room.objects.filter(is_available=True).order_by('filiere', 'name')
    
    context = {
        'defenses': defenses,
        'rooms': rooms,
        'selected_room': room_id,
        'selected_date': date_filter,
        'selected_status': status_filter,
    }
    return render(request, 'defenses/defense_list.html', context)


@login_required
def defense_detail_view(request, pk):
    """Détails d'une soutenance"""
    defense = get_object_or_404(Defense, pk=pk)
    
    # Vérifier les permissions
    can_view = False
    if request.user.role in ['admin_filiere', 'admin_general', 'jury']:
        can_view = True
    elif request.user.role == 'student' and defense.project.assignment.student == request.user:
        can_view = True
    elif request.user.role == 'teacher' and defense.project.assignment.subject.supervisor == request.user:
        can_view = True
    
    if not can_view:
        messages.error(request, "Vous n'êtes pas autorisé à voir cette soutenance.")
        return redirect('defenses:list')
    
    jury_members = defense.jury_members.all()
    
    # Récupérer l'évaluation si elle existe
    try:
        evaluation = defense.evaluation
    except DefenseEvaluation.DoesNotExist:
        evaluation = None
    
    # Calculer la note moyenne des membres du jury
    jury_grades = [jm.grade for jm in jury_members if jm.grade is not None]
    avg_grade = sum(jury_grades) / len(jury_grades) if jury_grades else None
    
    context = {
        'defense': defense,
        'jury_members': jury_members,
        'evaluation': evaluation,
        'avg_grade': avg_grade,
    }
    return render(request, 'defenses/defense_detail.html', context)


@login_required
def defense_create_view(request, project_id):
    """Créer une nouvelle soutenance (admin uniquement)"""
    if request.user.role != 'admin':
        messages.error(request, "Seuls les administrateurs peuvent créer des soutenances.")
        return redirect('defenses:list')
    
    project = get_object_or_404(Project, pk=project_id)
    
    # Vérifier qu'il n'y a pas déjà une soutenance pour ce projet
    if hasattr(project, 'defense'):
        messages.warning(request, "Ce projet a déjà une soutenance planifiée.")
        return redirect('defenses:detail', pk=project.defense.pk)
    
    if request.method == 'POST':
        form = DefenseForm(request.POST)
        if form.is_valid():
            defense = form.save()
            messages.success(request, "Soutenance planifiée avec succès.")
            return redirect('defenses:detail', pk=defense.pk)
    else:
        form = DefenseForm(initial={'project': project})
    
    context = {
        'form': form,
        'project': project,
    }
    return render(request, 'defenses/defense_form.html', context)


@login_required
def jury_member_add_view(request, defense_id):
    """Ajouter un membre au jury (admin uniquement)"""
    if request.user.role != 'admin':
        messages.error(request, "Seuls les administrateurs peuvent gérer les jurys.")
        return redirect('defenses:list')
    
    defense = get_object_or_404(Defense, pk=defense_id)
    
    if request.method == 'POST':
        form = JuryMemberForm(request.POST)
        if form.is_valid():
            jury_member = form.save(commit=False)
            jury_member.defense = defense
            
            # Vérifier que ce membre n'est pas déjà dans le jury
            if JuryMember.objects.filter(defense=defense, user=jury_member.user).exists():
                messages.warning(request, "Ce membre fait déjà partie du jury.")
            else:
                jury_member.save()
                messages.success(request, f"{jury_member.user.get_full_name()} a été ajouté au jury.")
            
            return redirect('defenses:detail', pk=defense.pk)
    else:
        form = JuryMemberForm()
    
    context = {
        'form': form,
        'defense': defense,
    }
    return render(request, 'defenses/jury_member_form.html', context)


@login_required
def evaluation_create_view(request, defense_id):
    """Créer/modifier une évaluation (admin ou président de jury)"""
    defense = get_object_or_404(Defense, pk=defense_id)
    
    # Vérifier les permissions
    if request.user.role != 'admin':
        # Vérifier si l'utilisateur est président du jury
        try:
            jury_member = JuryMember.objects.get(defense=defense, user=request.user, role='president')
        except JuryMember.DoesNotExist:
            messages.error(request, "Seul le président du jury peut créer l'évaluation globale.")
            return redirect('defenses:detail', pk=defense.pk)
    
    # Récupérer ou créer l'évaluation
    evaluation, created = DefenseEvaluation.objects.get_or_create(
        defense=defense
    )
    
    if request.method == 'POST':
        form = DefenseEvaluationForm(request.POST, instance=evaluation)
        if form.is_valid():
            form.save()
            messages.success(request, "Évaluation enregistrée avec succès.")
            return redirect('defenses:detail', pk=defense.pk)
    else:
        form = DefenseEvaluationForm(instance=evaluation)
    
    context = {
        'form': form,
        'defense': defense,
        'evaluation': evaluation,
    }
    return render(request, 'defenses/evaluation_form.html', context)


@login_required
def defense_calendar_view(request):
    """Calendrier des soutenances"""
    defenses = Defense.objects.select_related('project').order_by('date', 'time')
    
    context = {
        'defenses': defenses,
    }
    return render(request, 'defenses/defense_calendar.html', context)


@login_required
def defense_planning_view(request):
    """Interface de planification des soutenances (admin et encadreurs)"""
    from subjects.models import Assignment
    
    # Vérifier les permissions
    if request.user.role not in ['admin_filiere', 'admin_general', 'teacher']:
        messages.error(request, "Vous n'êtes pas autorisé à accéder à cette page.")
        return redirect('defenses:list')
    
    is_admin = request.user.is_admin_staff()
    
    # TOUS voient le planning global des soutenances
    all_defenses = Defense.objects.select_related(
        'project', 'project__assignment', 'project__assignment__student',
        'project__assignment__subject__supervisor'
    ).order_by('date', 'time')
    
    # Admin voit tous les projets, encadreur voit seulement les siens pour la gestion détaillée
    if is_admin:
        active_assignments = Assignment.objects.filter(
            status='active'
        ).select_related('student', 'subject', 'subject__supervisor')
        
        pending_requests = DefenseChangeRequest.objects.filter(
            status='pending'
        ).select_related('defense', 'requested_by').order_by('-created_at')
    else:
        # Encadreur: seulement ses propres projets pour la section "Mes projets"
        active_assignments = Assignment.objects.filter(
            status='active',
            subject__supervisor=request.user
        ).select_related('student', 'subject', 'subject__supervisor')
        
        # Toutes les demandes pour information
        pending_requests = DefenseChangeRequest.objects.filter(
            status='pending'
        ).select_related('defense', 'requested_by').order_by('-created_at')
    
    # Créer une liste avec les projets et leur statut de soutenance (pour la section admin/mes projets)
    projects_data = []
    for assignment in active_assignments:
        # Vérifier si un projet existe
        try:
            project = assignment.project
            has_project = True
        except:
            project = None
            has_project = False
        
        # Vérifier si une soutenance existe
        has_defense = False
        defense = None
        if has_project and project:
            try:
                defense = project.defense
                has_defense = True
            except:
                pass
        
        projects_data.append({
            'assignment': assignment,
            'project': project,
            'has_project': has_project,
            'defense': defense,
            'has_defense': has_defense,
        })
    
    context = {
        'projects_data': projects_data,
        'all_defenses': all_defenses,
        'pending_requests': pending_requests,
        'is_admin': is_admin,
        'is_supervisor': request.user.role == 'teacher',
    }
    return render(request, 'defenses/defense_planning.html', context)


@login_required
def defense_update_view(request, pk):
    """Modifier une soutenance (admin uniquement)"""
    if request.user.role != 'admin':
        messages.error(request, "Seuls les administrateurs peuvent modifier les soutenances.")
        return redirect('defenses:detail', pk=pk)
    
    defense = get_object_or_404(Defense, pk=pk)
    
    if request.method == 'POST':
        form = DefenseUpdateForm(request.POST, instance=defense)
        if form.is_valid():
            form.save()
            messages.success(request, "Soutenance modifiée avec succès.")
            return redirect('defenses:detail', pk=defense.pk)
    else:
        form = DefenseUpdateForm(instance=defense)
    
    context = {
        'form': form,
        'defense': defense,
    }
    return render(request, 'defenses/defense_update.html', context)


@login_required
def defense_change_request_create_view(request, defense_id):
    """Créer une demande de modification de soutenance"""
    defense = get_object_or_404(Defense, pk=defense_id)
    
    # Vérifier les permissions (étudiant concerné ou encadreur)
    can_request = False
    if request.user.role == 'student' and defense.project.assignment.student == request.user:
        can_request = True
    elif request.user.role == 'teacher' and defense.project.assignment.subject.supervisor == request.user:
        can_request = True
    
    if not can_request:
        messages.error(request, "Vous n'êtes pas autorisé à demander une modification.")
        return redirect('defenses:detail', pk=defense_id)
    
    # Vérifier s'il y a déjà une demande en attente
    existing_request = DefenseChangeRequest.objects.filter(
        defense=defense,
        requested_by=request.user,
        status='pending'
    ).first()
    
    if existing_request:
        messages.warning(request, "Vous avez déjà une demande en attente pour cette soutenance.")
        return redirect('defenses:detail', pk=defense_id)
    
    if request.method == 'POST':
        form = DefenseChangeRequestForm(request.POST)
        if form.is_valid():
            change_request = form.save(commit=False)
            change_request.defense = defense
            change_request.requested_by = request.user
            change_request.save()
            messages.success(request, "Demande de modification envoyée avec succès.")
            return redirect('defenses:detail', pk=defense_id)
    else:
        form = DefenseChangeRequestForm(initial={
            'proposed_date': defense.date,
            'proposed_time': defense.time,
            'proposed_location': defense.room
        })
    
    context = {
        'form': form,
        'defense': defense,
    }
    return render(request, 'defenses/defense_change_request.html', context)


@login_required
def defense_change_request_review_view(request, pk):
    """Examiner une demande de modification (admin uniquement)"""
    if request.user.role != 'admin':
        messages.error(request, "Seuls les administrateurs peuvent examiner les demandes.")
        return redirect('defenses:list')
    
    change_request = get_object_or_404(DefenseChangeRequest, pk=pk)
    
    if change_request.status != 'pending':
        messages.warning(request, "Cette demande a déjà été traitée.")
        return redirect('defenses:planning')
    
    if request.method == 'POST':
        form = DefenseChangeReviewForm(request.POST, instance=change_request)
        if form.is_valid():
            change_request = form.save(commit=False)
            change_request.reviewed_by = request.user
            change_request.reviewed_at = timezone.now()
            change_request.save()
            
            # Si approuvé, appliquer les modifications
            if change_request.status == 'approved':
                defense = change_request.defense
                if change_request.proposed_date:
                    defense.date = change_request.proposed_date
                if change_request.proposed_time:
                    defense.time = change_request.proposed_time
                if change_request.proposed_location:
                    defense.room = change_request.proposed_location
                defense.save()
                messages.success(request, "Demande approuvée et soutenance modifiée.")
            else:
                messages.info(request, "Demande rejetée.")
            
            return redirect('defenses:planning')
    else:
        form = DefenseChangeReviewForm(instance=change_request)
    
    context = {
        'form': form,
        'change_request': change_request,
    }
    return render(request, 'defenses/defense_change_review.html', context)


@login_required
def grade_defense_view(request, pk):
    """
    Interface de notation pour les membres du jury.
    Chaque membre du jury peut attribuer une note et des commentaires.
    """
    defense = get_object_or_404(Defense, pk=pk)
    
    # Vérifier que l'utilisateur est bien membre du jury
    from .models import DefenseJury
    
    try:
        jury_member = DefenseJury.objects.get(
            defense=defense,
            teacher=request.user
        )
    except DefenseJury.DoesNotExist:
        messages.error(request, "Vous n'êtes pas membre du jury de cette soutenance.")
        return redirect('defenses:defense_detail', pk=pk)
    
    # Vérifier que la soutenance est passée
    if not defense.can_be_graded:
        messages.warning(request, "La soutenance n'a pas encore eu lieu.")
        return redirect('defenses:defense_detail', pk=pk)
    
    # Vérifier si déjà noté
    if jury_member.grade is not None:
        messages.info(request, "Vous avez déjà noté cette soutenance. Vous pouvez modifier votre note.")
    
    if request.method == 'POST':
        grade = request.POST.get('grade')
        comments = request.POST.get('comments', '')
        
        try:
            grade_value = float(grade)
            if not (0 <= grade_value <= 20):
                messages.error(request, "La note doit être entre 0 et 20.")
            else:
                jury_member.grade = grade_value
                jury_member.comments = comments
                jury_member.graded_at = timezone.now()
                jury_member.save()
                
                messages.success(request, f"Note enregistrée : {grade_value}/20")
                
                # Vérifier si tous les membres ont noté
                if defense.is_fully_graded:
                    # Calculer la note finale
                    final_grade = defense.calculate_final_grade()
                    
                return redirect('defenses:defense_detail', pk=pk)
        except ValueError:
            messages.error(request, "Note invalide.")
    
    context = {
        'defense': defense,
        'jury_member': jury_member,
    }
    return render(request, 'defenses/grade_defense.html', context)


@login_required
def room_schedule_view(request):
    """Affiche le planning des soutenances par salle et par jour"""
    
    # Filtres GET
    room_id = request.GET.get('room')
    date_filter = request.GET.get('date')
    
    # Query de base
    defenses = Defense.objects.select_related('project', 'room_obj').filter(
        room_obj__isnull=False
    )
    
    # Filtre par salle
    selected_room = None
    if room_id:
        defenses = defenses.filter(room_obj_id=room_id)
        selected_room = Room.objects.filter(id=room_id).first()
    
    # Filtre par date
    selected_date = None
    if date_filter:
        try:
            selected_date = datetime.strptime(date_filter, '%Y-%m-%d').date()
            defenses = defenses.filter(date=selected_date)
        except ValueError:
            pass
    
    # Trier par date et heure
    defenses = defenses.order_by('date', 'time')
    
    # Grouper par salle et par date
    schedule = {}
    for defense in defenses:
        room_key = defense.room_obj.id
        date_key = defense.date
        
        if room_key not in schedule:
            schedule[room_key] = {
                'room': defense.room_obj,
                'dates': {}
            }
        
        if date_key not in schedule[room_key]['dates']:
            schedule[room_key]['dates'][date_key] = []
        
        schedule[room_key]['dates'][date_key].append(defense)
    
    # Listes pour les filtres
    rooms = Room.objects.filter(is_available=True).order_by('filiere', 'name')
    
    # Dates disponibles (soutenances planifiées)
    available_dates = Defense.objects.filter(
        room_obj__isnull=False
    ).values_list('date', flat=True).distinct().order_by('date')
    
    context = {
        'schedule': schedule,
        'rooms': rooms,
        'available_dates': available_dates,
        'selected_room': selected_room,
        'selected_date': selected_date,
    }
    return render(request, 'defenses/room_schedule.html', context)


@login_required
def room_list_view(request):
    """Liste toutes les salles avec interface simple"""
    # Vérifier permissions admin
    if not (request.user.is_admin_filiere() or request.user.is_admin_general()):
        messages.error(request, "Vous n'avez pas les permissions pour gérer les salles.")
        return redirect('users:dashboard')
    
    # Filtrer selon le rôle
    if request.user.is_admin_general():
        rooms = Room.objects.all()
    else:
        rooms = Room.objects.filter(filiere=request.user.filiere_admin)
    
    # Trier uniquement par les champs réels (name contient déjà building et floor)
    rooms = rooms.order_by('filiere', 'name')
    
    context = {
        'rooms': rooms,
        'is_general_admin': request.user.is_admin_general(),
    }
    return render(request, 'defenses/room_list.html', context)


@login_required
def room_create_view(request):
    """Créer une nouvelle salle"""
    # Vérifier permissions
    if not (request.user.is_admin_filiere() or request.user.is_admin_general()):
        messages.error(request, "Vous n'avez pas les permissions pour créer une salle.")
        return redirect('users:dashboard')
    
    if request.method == 'POST':
        form = RoomForm(request.POST, user=request.user)
        if form.is_valid():
            room = form.save()
            messages.success(request, f"Salle '{room.name}' créée avec succès.")
            return redirect('defenses:room_list')
    else:
        form = RoomForm(user=request.user)
    
    context = {
        'form': form,
        'title': 'Créer une salle',
    }
    return render(request, 'defenses/room_form.html', context)


@login_required
def room_edit_view(request, pk):
    """Modifier une salle existante"""
    room = get_object_or_404(Room, pk=pk)
    
    # Vérifier permissions
    if request.user.is_admin_general():
        can_edit = True
    elif request.user.is_admin_filiere():
        can_edit = request.user.can_manage_filiere(room.filiere)
    else:
        can_edit = False
    
    if not can_edit:
        messages.error(request, "Vous n'avez pas les permissions pour modifier cette salle.")
        return redirect('defenses:room_list')
    
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room, user=request.user)
        if form.is_valid():
            room = form.save()
            messages.success(request, f"Salle '{room.name}' modifiée avec succès.")
            return redirect('defenses:room_list')
    else:
        form = RoomForm(instance=room, user=request.user)
    
    context = {
        'form': form,
        'room': room,
        'title': 'Modifier la salle',
    }
    return render(request, 'defenses/room_form.html', context)


@login_required
def room_delete_view(request, pk):
    """Supprimer une salle"""
    room = get_object_or_404(Room, pk=pk)
    
    # Vérifier permissions
    if request.user.is_admin_general():
        can_delete = True
    elif request.user.is_admin_filiere():
        can_delete = request.user.can_manage_filiere(room.filiere)
    else:
        can_delete = False
    
    if not can_delete:
        messages.error(request, "Vous n'avez pas les permissions pour supprimer cette salle.")
        return redirect('defenses:room_list')
    
    # Vérifier si la salle est utilisée
    defenses_count = Defense.objects.filter(room_obj=room).count()
    
    if request.method == 'POST':
        if defenses_count > 0:
            messages.error(request, f"Cette salle ne peut pas être supprimée car elle est utilisée par {defenses_count} soutenance(s).")
        else:
            room_name = room.name
            room.delete()
            messages.success(request, f"Salle '{room_name}' supprimée avec succès.")
        return redirect('defenses:room_list')
    
    context = {
        'room': room,
        'defenses_count': defenses_count,
    }
    return render(request, 'defenses/room_delete.html', context)
