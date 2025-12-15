"""
Test et explication de l'aspect 'Mes Projets' pour les étudiants.

Ce script teste et explique la différence entre les différentes vues de projets.
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from projects.models import Project
from subjects.models import Subject, Assignment
from django.test import RequestFactory
from django.contrib.messages.storage.fallback import FallbackStorage

User = get_user_model()

def print_section(title):
    """Affiche un titre de section."""
    print("\n" + "="*80)
    print(f" {title}")
    print("="*80 + "\n")


def explain_my_projects():
    """Explique ce qu'est 'Mes Projets'."""
    print_section("EXPLICATION: Qu'est-ce que 'Mes Projets' ?")
    
    explanation = """
    🎓 POUR LES ÉTUDIANTS:
    
    Il existe DEUX URLs pour voir les projets:
    
    1. /projects/ (Liste générale)
       - Affiche TOUS les projets selon votre rôle
       - Étudiant: Voit uniquement SES projets
       - Encadreur: Voit uniquement les projets qu'il encadre
       - Admin: Voit TOUS les projets de tous les étudiants
       - Template utilisé: project_list.html
    
    2. /projects/my-projects/ (Mes Projets)
       - Affiche vos projets dans un format CARTE
       - Plus visuel avec des cartes colorées
       - Montre la progression avec une barre de progression
       - Plus adapté pour un aperçu rapide
       - Template utilisé: my_projects.html
    
    📊 DIFFÉRENCE PRINCIPALE:
    - project_list.html: Vue TABLEAU détaillée avec filtres (admin)
    - my_projects.html: Vue CARTES simplifiée pour tous les utilisateurs
    
    🔍 POUR UN ÉTUDIANT:
    - /projects/ montre vos projets dans un tableau
    - /projects/my-projects/ montre vos projets en cartes visuelles
    - Les deux montrent exactement LES MÊMES projets
    - C'est juste une PRÉSENTATION différente
    
    📝 RECOMMANDATION:
    - Utiliser /projects/my-projects/ pour un aperçu rapide
    - Utiliser /projects/ pour voir plus de détails et filtrer (si admin)
    """
    
    print(explanation)


def test_student_projects():
    """Test les projets d'un étudiant."""
    print_section("TEST: Projets d'un étudiant")
    
    # Trouver un étudiant avec des projets
    student = User.objects.filter(role='student').first()
    
    if not student:
        print("❌ Aucun étudiant trouvé dans la base de données.")
        return
    
    print(f"👤 Étudiant testé: {student.get_full_name()} ({student.email})")
    print(f"   ID: {student.id}")
    
    # Récupérer ses affectations
    assignments = Assignment.objects.filter(student=student)
    print(f"\n📋 Affectations de l'étudiant: {assignments.count()}")
    
    for i, assignment in enumerate(assignments, 1):
        print(f"\n{i}. Sujet: {assignment.subject.title}")
        print(f"   Encadreur: {assignment.subject.supervisor.get_full_name()}")
        print(f"   Date d'affectation: {assignment.assigned_at.strftime('%d/%m/%Y')}")
        print(f"   Statut: {assignment.get_status_display()}")
    
    # Récupérer ses projets
    projects = Project.objects.filter(assignment__student=student)
    print(f"\n📁 Projets de l'étudiant: {projects.count()}")
    
    if projects.count() == 0:
        print("   ℹ️  Aucun projet créé pour cet étudiant.")
        print("   💡 Un projet est créé automatiquement quand une affectation est acceptée.")
    else:
        for i, project in enumerate(projects, 1):
            print(f"\n{i}. Projet: {project.assignment.subject.title}")
            print(f"   ID: {project.id}")
            print(f"   Statut: {project.get_status_display()}")
            print(f"   Progression: {project.progress}%")
            print(f"   Date de début: {project.start_date.strftime('%d/%m/%Y') if project.start_date else 'Non définie'}")
            print(f"   Date de fin prévue: {project.end_date.strftime('%d/%m/%Y') if project.end_date else 'Non définie'}")
            
            # Jalons
            milestones = project.milestones.all()
            print(f"   📌 Jalons: {milestones.count()}")
            for milestone in milestones:
                status = "✅" if milestone.is_completed else "⏳"
                validated = "✓ Validé" if milestone.validated else "⏳ En attente"
                print(f"      {status} {milestone.title} - {validated}")
            
            # Livrables
            deliverables = project.deliverables.all()
            print(f"   📦 Livrables: {deliverables.count()}")
            for deliverable in deliverables:
                print(f"      - {deliverable.title} ({deliverable.get_status_display()})")


def test_urls_access():
    """Test l'accès aux différentes URLs."""
    print_section("TEST: Accès aux URLs")
    
    from django.test import Client
    
    student = User.objects.filter(role='student').first()
    if not student:
        print("❌ Aucun étudiant pour tester.")
        return
    
    client = Client()
    client.force_login(student)
    
    print(f"👤 Connecté en tant que: {student.get_full_name()}")
    
    # Test /projects/
    print("\n1. Test de /projects/")
    response = client.get('/projects/')
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        print(f"   ✅ Accès réussi")
        print(f"   Template: {response.templates[0].name if response.templates else 'N/A'}")
        context_projects = response.context.get('projects', [])
        print(f"   Projets dans le contexte: {len(context_projects) if hasattr(context_projects, '__len__') else 'N/A'}")
    else:
        print(f"   ❌ Erreur d'accès")
    
    # Test /projects/my-projects/
    print("\n2. Test de /projects/my-projects/")
    response = client.get('/projects/my-projects/')
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        print(f"   ✅ Accès réussi")
        print(f"   Template: {response.templates[0].name if response.templates else 'N/A'}")
        context_projects = response.context.get('projects', [])
        print(f"   Projets dans le contexte: {len(context_projects) if hasattr(context_projects, '__len__') else 'N/A'}")
    else:
        print(f"   ❌ Erreur d'accès")


def test_project_detail_access():
    """Test l'accès aux détails d'un projet."""
    print_section("TEST: Accès aux détails d'un projet")
    
    from django.test import Client
    
    student = User.objects.filter(role='student').first()
    if not student:
        print("❌ Aucun étudiant pour tester.")
        return
    
    project = Project.objects.filter(assignment__student=student).first()
    if not project:
        print("❌ Aucun projet pour cet étudiant.")
        return
    
    client = Client()
    client.force_login(student)
    
    print(f"👤 Connecté en tant que: {student.get_full_name()}")
    print(f"📁 Projet: {project.assignment.subject.title}")
    
    url = f'/projects/{project.id}/'
    print(f"\nTest de {url}")
    
    response = client.get(url)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        print("✅ Accès réussi")
        print(f"Template: {response.templates[0].name if response.templates else 'N/A'}")
        
        # Vérifier les actions disponibles
        content = response.content.decode('utf-8')
        
        print("\n📝 Actions disponibles pour l'étudiant:")
        if 'Ajouter un jalon' in content:
            print("   ✅ Ajouter un jalon")
        if 'Ajouter un livrable' in content:
            print("   ✅ Ajouter un livrable")
        if 'Ajouter un commentaire' in content:
            print("   ✅ Ajouter un commentaire")
        if 'Modifier le projet' in content:
            print("   ✅ Modifier le projet")
    else:
        print("❌ Erreur d'accès")


def test_student_actions():
    """Test les actions qu'un étudiant peut faire."""
    print_section("TEST: Actions disponibles pour l'étudiant")
    
    student = User.objects.filter(role='student').first()
    if not student:
        print("❌ Aucun étudiant pour tester.")
        return
    
    project = Project.objects.filter(assignment__student=student).first()
    if not project:
        print("❌ Aucun projet pour cet étudiant.")
        return
    
    print(f"👤 Étudiant: {student.get_full_name()}")
    print(f"📁 Projet: {project.assignment.subject.title}")
    
    from django.test import Client
    client = Client()
    client.force_login(student)
    
    print("\n1️⃣ Test: Accès à la page d'ajout de jalon")
    response = client.get(f'/projects/{project.id}/milestones/create/')
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        print("   ✅ Peut ajouter des jalons")
    elif response.status_code == 302:
        print("   ⚠️  Redirigé (peut-être pas autorisé)")
    else:
        print("   ❌ Erreur")
    
    print("\n2️⃣ Test: Accès à la page d'ajout de livrable")
    response = client.get(f'/projects/{project.id}/deliverables/create/')
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        print("   ✅ Peut ajouter des livrables")
    elif response.status_code == 302:
        print("   ⚠️  Redirigé (peut-être pas autorisé)")
    else:
        print("   ❌ Erreur")
    
    print("\n3️⃣ Test: Accès à la page de modification du projet")
    response = client.get(f'/projects/{project.id}/update/')
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        print("   ✅ Peut modifier le projet")
    elif response.status_code == 302:
        print("   ⚠️  Redirigé (peut-être pas autorisé)")
    else:
        print("   ❌ Erreur")


def provide_recommendations():
    """Fournit des recommandations."""
    print_section("RECOMMANDATIONS")
    
    recommendations = """
    💡 POUR AMÉLIORER L'EXPÉRIENCE ÉTUDIANT:
    
    1. 🎯 Clarifier la navigation:
       - Renommer "Mes Projets" en "Vue Cartes" dans le menu
       - Renommer "Liste des Projets" en "Vue Détaillée"
       - Ou garder une seule vue (recommandé)
    
    2. 📱 Vue recommandée pour les étudiants:
       - Utiliser my_projects.html comme page principale
       - C'est plus visuel et convivial
       - Affiche clairement la progression
    
    3. 🔧 Actions à vérifier:
       - L'étudiant peut-il ajouter des jalons ? (À tester)
       - L'étudiant peut-il soumettre des livrables ? (À tester)
       - L'étudiant peut-il commenter ? (À tester)
    
    4. 📊 Informations à afficher:
       - Nombre de jalons complétés / total
       - Prochaine échéance
       - Statut de validation du dernier livrable
       - Messages récents de l'encadreur
    
    5. 🎨 Améliorations UX possibles:
       - Ajouter des notifications pour nouveaux commentaires
       - Afficher les tâches en attente
       - Mettre en avant les actions urgentes
       - Ajouter un tutoriel au premier accès
    """
    
    print(recommendations)


def main():
    """Fonction principale."""
    print("\n" + "🎓"*40)
    print(" "*20 + "TEST 'MES PROJETS' ÉTUDIANT")
    print("🎓"*40 + "\n")
    
    # Explication
    explain_my_projects()
    
    # Tests
    test_student_projects()
    test_urls_access()
    test_project_detail_access()
    test_student_actions()
    
    # Recommandations
    provide_recommendations()
    
    print("\n" + "="*80)
    print(" "*30 + "FIN DES TESTS")
    print("="*80 + "\n")


if __name__ == '__main__':
    main()
