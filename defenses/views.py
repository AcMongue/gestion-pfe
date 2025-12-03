from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Avg
from .models import Defense, JuryMember, DefenseEvaluation
from .forms import DefenseForm, JuryMemberForm, DefenseEvaluationForm
from projects.models import Project

@login_required
def defense_list_view(request):
    """Liste toutes les soutenances"""
    if request.user.role == 'student':
        # Les étudiants voient seulement leurs propres soutenances
        defenses = Defense.objects.filter(
            project__assignment__student=request.user
        )
    elif request.user.role == 'supervisor':
        # Les encadreurs voient les soutenances de leurs projets
        defenses = Defense.objects.filter(
            project__assignment__subject__supervisor=request.user
        )
    elif request.user.role in ['admin', 'jury']:
        # Admins et jurys voient tout
        defenses = Defense.objects.all()
    else:
        defenses = Defense.objects.none()
    
    defenses = defenses.select_related('project').order_by('-date', '-time')
    
    context = {
        'defenses': defenses,
    }
    return render(request, 'defenses/defense_list.html', context)


@login_required
def defense_detail_view(request, pk):
    """Détails d'une soutenance"""
    defense = get_object_or_404(Defense, pk=pk)
    
    # Vérifier les permissions
    can_view = False
    if request.user.role in ['admin', 'jury']:
        can_view = True
    elif request.user.role == 'student' and defense.project.assignment.student == request.user:
        can_view = True
    elif request.user.role == 'supervisor' and defense.project.assignment.subject.supervisor == request.user:
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
