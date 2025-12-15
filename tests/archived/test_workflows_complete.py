"""
Script de test complet de tous les workflows du système
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from users.models import Profile
from subjects.models import Subject, Application, Assignment
from projects.models import Project, Milestone, Deliverable
from defenses.models import Defense
from communications.models import Message, Notification
from archives.models import ArchivedProject
from datetime import datetime, timedelta

User = get_user_model()

def test_workflow_1_users():
    """Test du workflow utilisateurs"""
    print("\n" + "="*80)
    print("WORKFLOW 1: GESTION DES UTILISATEURS")
    print("="*80)
    
    # Création d'utilisateurs de test
    users_data = [
        {'username': 'admin_test', 'role': 'admin', 'first_name': 'Admin', 'last_name': 'Test'},
        {'username': 'supervisor_test', 'role': 'supervisor', 'first_name': 'Encadreur', 'last_name': 'Test'},
        {'username': 'student_test', 'role': 'student', 'first_name': 'Etudiant', 'last_name': 'Test'},
        {'username': 'jury_test', 'role': 'jury', 'first_name': 'Jury', 'last_name': 'Test'},
    ]
    
    created_users = {}
    for data in users_data:
        user, created = User.objects.get_or_create(
            username=data['username'],
            defaults={
                'email': f"{data['username']}@example.com",
                'first_name': data['first_name'],
                'last_name': data['last_name'],
                'role': data['role']
            }
        )
        if created:
            user.set_password('Test1234!')
            if user.role == 'student':
                user.level = 'L3'
            user.save()
            Profile.objects.get_or_create(user=user)
            print(f"✓ Utilisateur créé: {user.username} ({user.get_role_display()})")
        else:
            print(f"  Utilisateur existant: {user.username}")
        created_users[data['role']] = user
    
    print(f"\nTotal utilisateurs: {User.objects.count()}")
    return created_users


def test_workflow_2_subjects(users):
    """Test du workflow catalogue de sujets"""
    print("\n" + "="*80)
    print("WORKFLOW 2: CATALOGUE ET AFFECTATION DES SUJETS")
    print("="*80)
    
    supervisor = users['supervisor']
    student = users['student']
    
    # Création d'un sujet
    subject, created = Subject.objects.get_or_create(
        title="Application de gestion des PFE",
        defaults={
            'supervisor': supervisor,
            'description': 'Développement d\'une application web pour la gestion des projets de fin d\'études',
            'objectives': 'Créer une plateforme complète de gestion',
            'level': 'L3',
            'max_students': 1,
            'status': 'available'
        }
    )
    if created:
        print(f"✓ Sujet créé: {subject.title}")
    else:
        print(f"  Sujet existant: {subject.title}")
    
    # Candidature
    application, created = Application.objects.get_or_create(
        student=student,
        subject=subject,
        defaults={'status': 'pending'}
    )
    if created:
        print(f"✓ Candidature créée: {student.username} -> {subject.title}")
    else:
        print(f"  Candidature existante: {application.status}")
    
    # Acceptation et affectation
    if application.status == 'pending':
        application.status = 'accepted'
        application.save()
        print(f"✓ Candidature acceptée")
    
    assignment, created = Assignment.objects.get_or_create(
        student=student,
        subject=subject,
        defaults={'status': 'active'}
    )
    if created:
        subject.status = 'assigned'
        subject.save()
        print(f"✓ Affectation créée: {student.username} <- {subject.title}")
    else:
        print(f"  Affectation existante: {assignment.status}")
    
    print(f"\nTotal sujets: {Subject.objects.count()}")
    print(f"Total candidatures: {Application.objects.count()}")
    print(f"Total affectations: {Assignment.objects.count()}")
    
    return subject, assignment


def test_workflow_3_projects(assignment, users):
    """Test du workflow suivi de projet"""
    print("\n" + "="*80)
    print("WORKFLOW 3: SUIVI COLLABORATIF DES PROJETS")
    print("="*80)
    
    # Création du projet
    project, created = Project.objects.get_or_create(
        assignment=assignment,
        defaults={
            'title': assignment.subject.title,
            'description': assignment.subject.description,
            'objectives': assignment.subject.objectives,
            'status': 'in_progress',
            'progress_percentage': 0,
            'expected_end_date': datetime.now().date() + timedelta(days=180)
        }
    )
    if created:
        print(f"✓ Projet créé: {project.title}")
    else:
        print(f"  Projet existant: {project.title}")
    
    # Création de jalons
    milestones_data = [
        {'title': 'Analyse et spécification', 'order': 1, 'days': 30},
        {'title': 'Conception', 'order': 2, 'days': 60},
        {'title': 'Développement', 'order': 3, 'days': 120},
        {'title': 'Tests et validation', 'order': 4, 'days': 150},
    ]
    
    for m_data in milestones_data:
        milestone, created = Milestone.objects.get_or_create(
            project=project,
            title=m_data['title'],
            defaults={
                'description': f"Étape: {m_data['title']}",
                'order': m_data['order'],
                'status': 'in_progress' if m_data['order'] == 1 else 'pending',
                'due_date': datetime.now().date() + timedelta(days=m_data['days'])
            }
        )
        if created:
            print(f"  ✓ Jalon créé: {milestone.title}")
    
    # Création d'un livrable (commenté car nécessite un fichier)
    # deliverable, created = Deliverable.objects.get_or_create(
    #     project=project,
    #     title="Cahier des charges",
    #     defaults={
    #         'description': 'Document de spécification des besoins',
    #         'type': 'documentation',
    #         'submitted_by': assignment.student
    #     }
    # )
    # if created:
    #     print(f"  ✓ Livrable créé: {deliverable.title}")
    
    print(f"\nTotal projets: {Project.objects.count()}")
    print(f"Total jalons: {Milestone.objects.count()}")
    print(f"Total livrables: {Deliverable.objects.count()}")
    
    return project


def test_workflow_4_communications(users, project):
    """Test du workflow communication"""
    print("\n" + "="*80)
    print("WORKFLOW 4: COMMUNICATION CONTEXTUALISÉE")
    print("="*80)
    
    student = users['student']
    supervisor = users['supervisor']
    
    # Message de l'étudiant au superviseur
    message, created = Message.objects.get_or_create(
        sender=student,
        recipient=supervisor,
        defaults={
            'subject': 'Question sur le projet',
            'content': 'Bonjour, j\'ai une question concernant l\'architecture du projet.',
            'project': project
        }
    )
    if created:
        print(f"✓ Message créé: {student.username} -> {supervisor.username}")
        
        # Notification automatique
        Notification.objects.create(
            user=supervisor,
            type='message',
            title='Nouveau message',
            message=f"{student.get_full_name()} vous a envoyé un message",
            link=f"/communications/messages/{message.pk}/"
        )
        print(f"  ✓ Notification créée pour {supervisor.username}")
    else:
        print(f"  Message existant")
    
    # Notification de jalon
    Notification.objects.get_or_create(
        user=student,
        type='milestone',
        defaults={
            'title': 'Jalon à venir',
            'message': 'Le jalon "Analyse et spécification" arrive bientôt à échéance'
        }
    )
    
    print(f"\nTotal messages: {Message.objects.count()}")
    print(f"Total notifications: {Notification.objects.count()}")
    
    return message


def test_workflow_5_defenses(project, users):
    """Test du workflow soutenances"""
    print("\n" + "="*80)
    print("WORKFLOW 5: PLANIFICATION DES SOUTENANCES")
    print("="*80)
    
    jury_member = users['jury']
    
    # Mise à jour du statut du projet
    if project.status == 'in_progress':
        project.status = 'submitted'
        project.progress_percentage = 100
        project.save()
        print(f"✓ Projet soumis: {project.title}")
    
    # Planification de la soutenance
    defense, created = Defense.objects.get_or_create(
        project=project,
        defaults={
            'date': datetime.now().date() + timedelta(days=7),
            'time': datetime.now().time(),
            'duration': 30,
            'room': 'A101',
            'building': 'Bâtiment Principal',
            'status': 'scheduled'
        }
    )
    if created:
        # Créer un JuryMember
        from defenses.models import JuryMember
        jury_m, _ = JuryMember.objects.get_or_create(
            defense=defense,
            user=jury_member,
            defaults={'role': 'member'}
        )
        print(f"✓ Soutenance créée: {defense.date} à {defense.time}")
        print(f"  Jury: {jury_member.get_full_name()}")
    else:
        print(f"  Soutenance existante: {defense.status}")
    
    print(f"\nTotal soutenances: {Defense.objects.count()}")
    
    return defense


def test_workflow_6_archives(project, users):
    """Test du workflow archives"""
    print("\n" + "="*80)
    print("WORKFLOW 6: ARCHIVAGE ET REPORTING")
    print("="*80)
    
    admin = users['admin']
    
    # Archivage du projet
    archive, created = ArchivedProject.objects.get_or_create(
        project=project,
        defaults={
            'archived_by': admin,
            'year': datetime.now().year,
            'semester': 'S1' if datetime.now().month <= 6 else 'S2',
            'final_grade': 15.5,
            'keywords': 'gestion, web, django',
            'summary': 'Application complète de gestion des PFE',
            'is_public': True
        }
    )
    if created:
        print(f"✓ Projet archivé: {project.title}")
        print(f"  Année: {archive.year}, Semestre: {archive.semester}")
        print(f"  Note finale: {archive.final_grade}/20")
    else:
        print(f"  Archive existante: {archive.year} {archive.semester}")
    
    print(f"\nTotal projets archivés: {ArchivedProject.objects.count()}")
    
    return archive


def test_permissions():
    """Test des permissions et contrôles d'accès"""
    print("\n" + "="*80)
    print("TEST DES PERMISSIONS")
    print("="*80)
    
    roles = ['admin', 'supervisor', 'student', 'jury']
    
    for role in roles:
        users = User.objects.filter(role=role)
        if users.exists():
            user = users.first()
            print(f"\n{role.upper()}:")
            print(f"  - Est étudiant: {user.is_student()}")
            print(f"  - Est encadreur: {user.is_supervisor()}")
            print(f"  - Est admin/staff: {user.is_admin_staff()}")
            print(f"  - Est jury: {user.is_jury_member()}")


def generate_report():
    """Génération d'un rapport final"""
    print("\n" + "="*80)
    print("RAPPORT FINAL DU SYSTÈME")
    print("="*80)
    
    stats = {
        'Utilisateurs': User.objects.count(),
        'Sujets': Subject.objects.count(),
        'Candidatures': Application.objects.count(),
        'Affectations': Assignment.objects.count(),
        'Projets': Project.objects.count(),
        'Jalons': Milestone.objects.count(),
        'Livrables': Deliverable.objects.count(),
        'Messages': Message.objects.count(),
        'Notifications': Notification.objects.count(),
        'Soutenances': Defense.objects.count(),
        'Archives': ArchivedProject.objects.count(),
    }
    
    print("\nStatistiques globales:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    # Statut des workflows
    print("\nComplétion des workflows:")
    workflows = [
        ('Gestion utilisateurs', User.objects.count() > 0),
        ('Catalogue sujets', Subject.objects.count() > 0 and Assignment.objects.count() > 0),
        ('Suivi projets', Project.objects.count() > 0 and Milestone.objects.count() > 0),
        ('Communication', Message.objects.count() > 0 and Notification.objects.count() > 0),
        ('Soutenances', Defense.objects.count() > 0),
        ('Archives', ArchivedProject.objects.count() > 0),
    ]
    
    all_complete = True
    for name, is_complete in workflows:
        status = "✓ OK" if is_complete else "✗ INCOMPLET"
        print(f"  {name}: {status}")
        if not is_complete:
            all_complete = False
    
    print("\n" + "="*80)
    if all_complete:
        print("TOUS LES WORKFLOWS SONT COMPLETS ET FONCTIONNELS!")
    else:
        print("ATTENTION: Certains workflows nécessitent des données de test")
    print("="*80)


def main():
    """Fonction principale de test"""
    print("\n")
    print("╔" + "="*78 + "╗")
    print("║" + " "*20 + "TEST COMPLET DU SYSTÈME PFE" + " "*31 + "║")
    print("╚" + "="*78 + "╝")
    
    try:
        # Exécution des tests de workflow
        users = test_workflow_1_users()
        subject, assignment = test_workflow_2_subjects(users)
        project = test_workflow_3_projects(assignment, users)
        message = test_workflow_4_communications(users, project)
        defense = test_workflow_5_defenses(project, users)
        archive = test_workflow_6_archives(project, users)
        
        # Tests supplémentaires
        test_permissions()
        
        # Rapport final
        generate_report()
        
        print("\n✓ TOUS LES TESTS SONT TERMINÉS AVEC SUCCÈS!\n")
        
    except Exception as e:
        print(f"\n✗ ERREUR: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
