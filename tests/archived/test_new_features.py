"""
Test rapide des nouvelles fonctionnalités créées.
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model

User = get_user_model()

def print_section(title):
    print("\n" + "="*80)
    print(f" {title}")
    print("="*80 + "\n")


def test_supervisor_views():
    """Test les nouvelles vues encadreur."""
    print_section("TEST: Nouvelles vues Encadreur")
    
    supervisor = User.objects.filter(role='supervisor').first()
    
    if not supervisor:
        print("❌ Aucun encadreur trouvé")
        return
    
    client = Client()
    client.force_login(supervisor)
    
    print(f"👤 Connecté en tant que: {supervisor.get_full_name()}")
    
    # Test 1: Vue "Mes Étudiants"
    print("\n1️⃣ Test: Vue 'Mes Étudiants'")
    print("   URL: /projects/supervisor/students/")
    response = client.get('/projects/supervisor/students/')
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        print("   ✅ Vue accessible")
        context = response.context
        print(f"   📊 Statistiques:")
        print(f"      - Étudiants: {context.get('students_count', 0)}")
        print(f"      - Projets actifs: {context.get('active_projects_count', 0)}")
        print(f"      - Items en attente: {context.get('pending_items_count', 0)}")
        print(f"      - Progression moyenne: {context.get('average_progress', 0):.1f}%")
    else:
        print(f"   ❌ Erreur: {response.status_code}")
    
    # Test 2: Vue de suivi d'un étudiant
    from projects.models import Project
    project = Project.objects.filter(assignment__subject__supervisor=supervisor).first()
    
    if project:
        student_id = project.assignment.student.id
        print(f"\n2️⃣ Test: Suivi d'un étudiant (ID: {student_id})")
        print(f"   URL: /projects/supervisor/student/{student_id}/")
        response = client.get(f'/projects/supervisor/student/{student_id}/')
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            print("   ✅ Page de suivi accessible")
            context = response.context
            print(f"   📊 Informations:")
            print(f"      - Étudiant: {context.get('student').get_full_name()}")
            print(f"      - Projet: {context.get('project').title}")
            print(f"      - Jalons: {context.get('total_milestones_count', 0)}")
            print(f"      - Jalons validés: {context.get('validated_milestones_count', 0)}")
            print(f"      - Livrables: {context.get('total_deliverables_count', 0)}")
        else:
            print(f"   ❌ Erreur: {response.status_code}")
    else:
        print("\n2️⃣ Test: Suivi d'un étudiant")
        print("   ⚠️  Aucun projet pour tester")


def test_student_project_creation():
    """Test la création de projet pour un étudiant."""
    print_section("TEST: Création de Projet Étudiant")
    
    from subjects.models import Assignment
    
    # Trouver un étudiant avec affectation sans projet
    student = None
    assignment = None
    
    for ass in Assignment.objects.filter(status='accepted'):
        try:
            project = ass.project
        except:
            student = ass.student
            assignment = ass
            break
    
    if not student:
        print("⚠️  Tous les étudiants ont déjà un projet")
        print("   Recherche d'un étudiant avec projet...")
        assignment = Assignment.objects.filter(status='accepted').first()
        if assignment:
            student = assignment.student
            print(f"   Étudiant trouvé: {student.get_full_name()}")
    else:
        print(f"✅ Étudiant sans projet trouvé: {student.get_full_name()}")
        print(f"   Affectation: {assignment.subject.title}")
    
    if not student:
        print("❌ Aucun étudiant pour tester")
        return
    
    client = Client()
    client.force_login(student)
    
    # Test du dashboard
    print("\n1️⃣ Test: Dashboard étudiant")
    print("   URL: /dashboard/")
    response = client.get('/dashboard/')
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        content = response.content.decode('utf-8')
        if 'Créer mon projet' in content:
            print("   ✅ Bouton 'Créer mon projet' présent")
        elif 'Voir mon projet' in content:
            print("   ✅ Bouton 'Voir mon projet' présent (projet existe)")
        else:
            print("   ⚠️  Aucun bouton de projet visible")
    
    # Test de la page de création
    if assignment:
        print(f"\n2️⃣ Test: Page de création de projet")
        print(f"   URL: /projects/create/?assignment={assignment.id}")
        response = client.get(f'/projects/create/?assignment={assignment.id}')
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            print("   ✅ Page accessible")
            
            # Vérifier le pré-remplissage
            content = response.content.decode('utf-8')
            if assignment.subject.title in content:
                print(f"   ✅ Titre pré-rempli: {assignment.subject.title[:50]}...")
            else:
                print("   ⚠️  Titre non pré-rempli")
        else:
            print(f"   ❌ Erreur: {response.status_code}")


def test_urls_exist():
    """Vérifie que les URLs sont bien configurées."""
    print_section("TEST: Configuration des URLs")
    
    from django.urls import reverse, NoReverseMatch
    
    urls_to_test = [
        ('projects:supervisor_students', "Vue 'Mes Étudiants'"),
        ('projects:create', "Création de projet"),
    ]
    
    for url_name, description in urls_to_test:
        try:
            url = reverse(url_name)
            print(f"✅ {description}: {url}")
        except NoReverseMatch:
            print(f"❌ {description}: URL non trouvée")
    
    # Test avec paramètres
    try:
        url = reverse('projects:supervisor_student_detail', kwargs={'student_id': 1})
        print(f"✅ Suivi étudiant: {url}")
    except NoReverseMatch:
        print(f"❌ Suivi étudiant: URL non trouvée")
    
    try:
        url = reverse('projects:evaluate', kwargs={'pk': 1})
        print(f"✅ Évaluation projet: {url}")
    except NoReverseMatch:
        print(f"❌ Évaluation projet: URL non trouvée")


def main():
    print("\n" + "🧪"*40)
    print(" "*25 + "TESTS DES NOUVELLES FONCTIONNALITÉS")
    print("🧪"*40 + "\n")
    
    test_urls_exist()
    test_supervisor_views()
    test_student_project_creation()
    
    print("\n" + "="*80)
    print(" "*30 + "FIN DES TESTS")
    print("="*80 + "\n")
    
    print("💡 Pour tester manuellement:")
    print("   1. Lancez le serveur: python manage.py runserver")
    print("   2. Connectez-vous en tant qu'encadreur")
    print("   3. Allez sur: http://localhost:8000/projects/supervisor/students/")
    print("   4. Cliquez sur un étudiant pour voir le suivi détaillé")
    print()
    print("   Pour l'étudiant:")
    print("   1. Connectez-vous en tant qu'étudiant")
    print("   2. Allez sur: http://localhost:8000/dashboard/")
    print("   3. Cliquez sur 'Créer mon projet' (si disponible)")
    print()


if __name__ == '__main__':
    main()
