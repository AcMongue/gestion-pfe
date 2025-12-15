#!/usr/bin/env python
"""Script pour créer des projets de test"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.utils import timezone
from users.models import User
from subjects.models import Subject, Assignment
from projects.models import Project

def create_test_projects():
    """Crée des projets de test"""
    print("Création de projets de test...")
    
    # Récupérer les affectations existantes
    assignments = Assignment.objects.filter(status='active')
    
    if not assignments.exists():
        print("Aucune affectation active trouvée. Création d'affectations...")
        
        # Récupérer des sujets et étudiants
        subjects = Subject.objects.filter(status='published')[:3]
        students = User.objects.filter(role='student')[:3]
        
        if subjects.count() < 3:
            print("Pas assez de sujets. Créez d'abord des sujets.")
            return
            
        if students.count() < 3:
            print("Pas assez d'étudiants. Créez d'abord des étudiants.")
            return
        
        # Créer des affectations
        for subject, student in zip(subjects, students):
            assignment, created = Assignment.objects.get_or_create(
                subject=subject,
                student=student,
                defaults={'status': 'active'}
            )
            if created:
                print(f"Affectation créée: {student.get_full_name()} -> {subject.title}")
                # Mettre à jour le statut du sujet
                subject.status = 'assigned'
                subject.save()
        
        assignments = Assignment.objects.filter(status='active')
    
    # Créer des projets pour chaque affectation
    projects_created = 0
    for assignment in assignments:
        # Vérifier si un projet existe déjà
        if hasattr(assignment, 'project'):
            print(f"Projet déjà existant pour {assignment.student.get_full_name()}")
            continue
            
        project = Project.objects.create(
            assignment=assignment,
            title=assignment.subject.title,
            description=assignment.subject.description,
            objectives=assignment.subject.objectives,
            methodology="Méthodologie de développement agile avec sprints de 2 semaines",
            technologies="Python, Django, PostgreSQL, React",
            status='in_progress',
            progress_percentage=35,
            start_date=timezone.now().date()
        )
        projects_created += 1
        print(f"✓ Projet créé: {project.title} (ID: {project.pk})")
    
    if projects_created == 0:
        print("Tous les projets existent déjà.")
    else:
        print(f"\n{projects_created} projet(s) créé(s) avec succès!")
        
    # Afficher les projets disponibles pour soutenance
    print("\n=== Projets disponibles pour planification de soutenance ===")
    projects = Project.objects.all()
    for project in projects:
        has_defense = hasattr(project, 'defense')
        status = "✓ Soutenance planifiée" if has_defense else "⚠ Aucune soutenance"
        print(f"ID: {project.pk} | {project.title} | {status}")

if __name__ == '__main__':
    create_test_projects()
