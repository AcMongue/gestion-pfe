from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Avg, Count, Q
from .models import ArchivedProject, Report
from .forms import ArchiveProjectForm, ReportGenerationForm
from projects.models import Project
import json
from datetime import datetime

@login_required
def archive_list_view(request):
    """Liste des projets archivés"""
    if request.user.role not in ['admin', 'supervisor']:
        messages.error(request, "Vous n'êtes pas autorisé à consulter les archives.")
        return redirect('users:dashboard')
    
    # Filtres
    year_filter = request.GET.get('year')
    semester_filter = request.GET.get('semester')
    
    archives = ArchivedProject.objects.select_related('project', 'archived_by')
    
    if year_filter:
        archives = archives.filter(year=year_filter)
    if semester_filter:
        archives = archives.filter(semester=semester_filter)
    
    archives = archives.order_by('-archived_at')
    
    # Années disponibles
    years = ArchivedProject.objects.values_list('year', flat=True).distinct()
    
    context = {
        'archives': archives,
        'years': years,
        'selected_year': year_filter,
        'selected_semester': semester_filter,
    }
    return render(request, 'archives/archive_list.html', context)


@login_required
def archive_detail_view(request, pk):
    """Détails d'un projet archivé"""
    if request.user.role not in ['admin', 'supervisor']:
        messages.error(request, "Vous n'êtes pas autorisé à consulter les archives.")
        return redirect('users:dashboard')
    
    archive = get_object_or_404(ArchivedProject, pk=pk)
    
    context = {
        'archive': archive,
    }
    return render(request, 'archives/archive_detail.html', context)


@login_required
def archive_project_view(request, project_id):
    """Archiver un projet (admin uniquement)"""
    if request.user.role != 'admin':
        messages.error(request, "Seuls les administrateurs peuvent archiver des projets.")
        return redirect('users:dashboard')
    
    project = get_object_or_404(Project, pk=project_id)
    
    # Vérifier si le projet est déjà archivé
    if hasattr(project, 'archived_project'):
        messages.warning(request, "Ce projet est déjà archivé.")
        return redirect('archives:detail', pk=project.archived_project.pk)
    
    if request.method == 'POST':
        form = ArchiveProjectForm(request.POST)
        if form.is_valid():
            archive = form.save()
            messages.success(request, f"Le projet '{project.title}' a été archivé avec succès.")
            return redirect('archives:detail', pk=archive.pk)
    else:
        # Valeurs initiales
        current_year = datetime.now().year
        
        form = ArchiveProjectForm(initial={
            'project': project,
            'year': current_year,
            'archived_by': request.user,
        })
    
    context = {
        'form': form,
        'project': project,
    }
    return render(request, 'archives/archive_form.html', context)


@login_required
def reports_view(request):
    """Liste des rapports générés"""
    if request.user.role != 'admin':
        messages.error(request, "Seuls les administrateurs peuvent accéder aux rapports.")
        return redirect('users:dashboard')
    
    reports = Report.objects.all().order_by('-generated_at')
    
    context = {
        'reports': reports,
    }
    return render(request, 'archives/reports.html', context)


@login_required
def generate_report_view(request):
    """Générer un nouveau rapport"""
    if request.user.role != 'admin':
        messages.error(request, "Seuls les administrateurs peuvent générer des rapports.")
        return redirect('users:dashboard')
    
    if request.method == 'POST':
        form = ReportGenerationForm(request.POST)
        form = ReportGenerationForm(request.POST)
        if form.is_valid():
            report_type = form.cleaned_data['report_type']
            year_str = form.cleaned_data.get('academic_year')
            semester = form.cleaned_data.get('semester')
            
            # Convertir l'année en entier si fournie
            year = int(year_str) if year_str else None
            
            # Générer les statistiques selon le type de rapport
            statistics = generate_statistics(report_type, year, semester)
            
            # Dates de début et fin
            from datetime import date
            if year:
                period_start = date(year, 1, 1)
                period_end = date(year, 12, 31)
            else:
                period_start = date(2020, 1, 1)
                period_end = date.today()
            
            # Créer le rapport
            report = Report.objects.create(
                title=get_report_title(report_type, year_str, semester),
                type=report_type,
                period_start=period_start,
                period_end=period_end,
                content=statistics,
                generated_by=request.user
            )
            messages.success(request, "Rapport généré avec succès.")
            return redirect('archives:report_detail', pk=report.pk)
    else:
        form = ReportGenerationForm()
    
    context = {
        'form': form,
    }
    return render(request, 'archives/generate_report.html', context)


@login_required
def report_detail_view(request, pk):
    """Afficher un rapport"""
def generate_statistics(report_type, year=None, semester=None):
    """Générer les statistiques selon le type de rapport"""
    archives = ArchivedProject.objects.all()
    
    if year:
        archives = archives.filter(year=year)
    context = {
        'report': report,
    }
    return render(request, 'archives/report_detail.html', context)


def generate_statistics(report_type, academic_year=None, semester=None):
    """Générer les statistiques selon le type de rapport"""
    archives = ArchivedProject.objects.all()
    
    if academic_year:
        archives = archives.filter(academic_year=academic_year)
    if semester:
        archives = archives.filter(semester=semester)
    
    stats = {
        'total_projects': archives.count(),
        'average_grade': archives.aggregate(Avg('final_grade'))['final_grade__avg'],
        'by_level': {},
        'by_semester': {},
    }
    
    if report_type == 'annual':
        # Statistiques par niveau
        for archive in archives:
            level = archive.project.assignment.student.level
            if level not in stats['by_level']:
                stats['by_level'][level] = {'count': 0, 'total_grade': 0}
            stats['by_level'][level]['count'] += 1
            if archive.final_grade:
                stats['by_level'][level]['total_grade'] += archive.final_grade
    
    elif report_type == 'semester':
        # Statistiques par semestre
        semester_stats = archives.values('semester').annotate(
            count=Count('id'),
            avg_grade=Avg('final_grade')
        )
        stats['by_semester'] = {s['semester']: s for s in semester_stats}
    
    elif report_type == 'supervisor':
        # Statistiques par encadreur
        supervisor_stats = {}
        for archive in archives:
            supervisor = archive.project.assignment.subject.supervisor
            name = supervisor.get_full_name()
            if name not in supervisor_stats:
                supervisor_stats[name] = {'count': 0, 'total_grade': 0}
            supervisor_stats[name]['count'] += 1
            if archive.final_grade:
                supervisor_stats[name]['total_grade'] += archive.final_grade
        stats['by_supervisor'] = supervisor_stats
    
    return stats


def get_report_title(report_type, year, semester):
    """Générer le titre du rapport"""
    titles = {
        'annual': 'Rapport annuel',
        'semester': 'Rapport semestriel',
        'supervisor': 'Rapport par encadreur',
        'statistics': 'Statistiques générales',
    }
    
    title = titles.get(report_type, 'Rapport')
    if year:
        title += f" {year}"
    if semester:
        semester_dict = {'S1': 'Semestre 1', 'S2': 'Semestre 2'}
        title += f" - {semester_dict.get(semester, semester)}"
    
    return title
