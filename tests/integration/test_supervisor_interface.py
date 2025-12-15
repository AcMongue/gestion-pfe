"""
Test de l'interface encadreur - Vérification des données du dashboard
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from subjects.models import Subject, Application, Assignment
from projects.models import Project
from communications.models import Message

User = get_user_model()

def test_supervisor_dashboard():
    """Test des données affichées dans le dashboard encadreur"""
    print("\n" + "="*80)
    print("TEST INTERFACE ENCADREUR")
    print("="*80 + "\n")
    
    # Trouver ou créer un encadreur
    supervisor = User.objects.filter(role='supervisor').first()
    
    if not supervisor:
        print("Aucun encadreur trouvé dans le système!")
        return
    
    print(f"Encadreur testé: {supervisor.get_full_name()} ({supervisor.username})")
    print("-" * 80)
    
    # 1. Sujets proposés
    my_subjects = Subject.objects.filter(supervisor=supervisor)
    print(f"\n1. Sujets proposés: {my_subjects.count()}")
    for subject in my_subjects:
        print(f"   - {subject.title} [{subject.get_status_display()}]")
    
    # 2. Candidatures en attente
    pending_applications = Application.objects.filter(
        subject__supervisor=supervisor,
        status='pending'
    )
    print(f"\n2. Candidatures en attente: {pending_applications.count()}")
    for app in pending_applications:
        print(f"   - {app.student.get_full_name()} -> {app.subject.title}")
    
    # 3. Projets encadrés
    supervised_projects = Project.objects.filter(assignment__subject__supervisor=supervisor)
    print(f"\n3. Projets encadrés: {supervised_projects.count()}")
    for project in supervised_projects:
        print(f"   - {project.title}")
        print(f"     Étudiant: {project.assignment.student.get_full_name()}")
        print(f"     Progression: {project.progress}%")
        print(f"     Statut: {project.get_status_display()}")
    
    # 4. Messages non lus
    unread_messages = Message.objects.filter(recipient=supervisor, is_read=False).count()
    print(f"\n4. Messages non lus: {unread_messages}")
    
    # Résumé
    print("\n" + "="*80)
    print("RÉSUMÉ DU DASHBOARD ENCADREUR")
    print("="*80)
    print(f"Sujets proposés:        {my_subjects.count()}")
    print(f"Candidatures en attente: {pending_applications.count()}")
    print(f"Projets encadrés:       {supervised_projects.count()}")
    print(f"Messages non lus:       {unread_messages}")
    
    if my_subjects.count() > 0 or supervised_projects.count() > 0:
        print("\n✓ Le dashboard encadreur devrait afficher des données!")
    else:
        print("\n⚠ Le dashboard sera vide car l'encadreur n'a pas encore de sujets/projets")
    
    print("\n" + "="*80)


if __name__ == '__main__':
    test_supervisor_dashboard()
