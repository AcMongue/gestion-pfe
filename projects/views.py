from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Project, Milestone, Deliverable, Comment
from .forms import ProjectForm, MilestoneForm, DeliverableForm, CommentForm


@login_required
def project_list_view(request):
    """Liste des projets."""
    if request.user.is_student():
        projects = Project.objects.filter(assignment__student=request.user)
    elif request.user.is_supervisor():
        projects = Project.objects.filter(assignment__subject__supervisor=request.user)
    else:
        projects = Project.objects.all()
    return render(request, 'projects/project_list.html', {'projects': projects})


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
