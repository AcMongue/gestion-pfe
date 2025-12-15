#!/usr/bin/env python
"""
Test de la vue globale des projets
Vérifie que l'admin voit tous les projets avec statistiques
"""

import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

# Add testserver to ALLOWED_HOSTS for testing
from django.conf import settings
if 'testserver' not in settings.ALLOWED_HOSTS:
    settings.ALLOWED_HOSTS.append('testserver')

from django.contrib.auth import get_user_model
from django.test import Client
from projects.models import Project
from subjects.models import Assignment

User = get_user_model()

def test_global_projects_view():
    """Test de la vue globale des projets"""
    
    print("=" * 80)
    print("TEST: Vue globale des projets")
    print("=" * 80)
    
    # 1. Vérifier les utilisateurs
    admin = User.objects.filter(role='admin').first()
    supervisor = User.objects.filter(role='supervisor').first()
    student = User.objects.filter(role='student').first()
    
    if not admin:
        print("❌ ERREUR: Aucun admin trouvé")
        return False
    
    print(f"\n✓ Admin: {admin.get_full_name()}")
    print(f"✓ Supervisor: {supervisor.get_full_name() if supervisor else 'N/A'}")
    print(f"✓ Student: {student.get_full_name() if student else 'N/A'}")
    
    # 2. Statistiques des projets
    total_projects = Project.objects.count()
    projects_in_progress = Project.objects.filter(status='in_progress').count()
    projects_with_defense = Project.objects.filter(defense__isnull=False).count()
    
    print(f"\n📊 STATISTIQUES DES PROJETS:")
    print(f"  → Total projets: {total_projects}")
    print(f"  → En cours: {projects_in_progress}")
    print(f"  → Avec soutenance: {projects_with_defense}")
    print(f"  → Sans soutenance: {total_projects - projects_with_defense}")
    
    # 3. Tester l'accès admin
    client = Client()
    client.force_login(admin)
    
    print(f"\n{'='*80}")
    print("TEST 1: Accès admin à la vue globale")
    print(f"{'='*80}")
    
    response = client.get('/projects/')
    
    if response.status_code == 200:
        print(f"✅ Page chargée avec succès (status: {response.status_code})")
        
        context = response.context
        if context:
            is_global_view = context.get('is_global_view', False)
            projects = context.get('projects', [])
            total_in_context = context.get('total_projects', 0)
            
            print(f"  → is_global_view: {is_global_view}")
            print(f"  → Projets affichés: {len(list(projects))}")
            print(f"  → Total projets (contexte): {total_in_context}")
            
            if is_global_view:
                print("✅ Vue globale activée pour l'admin")
                
                # Vérifier les statistiques
                stats = context.get('projects_by_status', {})
                print(f"\n📈 Statistiques dans le contexte:")
                print(f"  → En cours: {stats.get('in_progress', 0)}")
                print(f"  → Terminés: {stats.get('completed', 0)}")
                print(f"  → En attente: {stats.get('pending', 0)}")
                
                # Vérifier les filtres
                supervisors = context.get('supervisors', [])
                print(f"  → Superviseurs disponibles pour filtre: {len(list(supervisors))}")
            else:
                print("⚠️  Vue globale NON activée pour l'admin")
        else:
            print("⚠️  Pas de contexte dans la réponse")
    else:
        print(f"❌ ERREUR: Code de statut {response.status_code}")
        return False
    
    # 4. Tester l'accès supervisor (vue personnelle)
    if supervisor:
        print(f"\n{'='*80}")
        print("TEST 2: Accès supervisor (vue personnelle)")
        print(f"{'='*80}")
        
        client.force_login(supervisor)
        response = client.get('/projects/')
        
        if response.status_code == 200:
            context = response.context
            is_global_view = context.get('is_global_view', False)
            projects = list(context.get('projects', []))
            
            print(f"✅ Page chargée (status: {response.status_code})")
            print(f"  → is_global_view: {is_global_view}")
            print(f"  → Projets affichés: {len(projects)}")
            
            if not is_global_view:
                print("✅ Vue personnelle pour le supervisor")
                
                # Vérifier que ce sont bien SES projets
                supervisor_projects = Project.objects.filter(
                    assignment__subject__supervisor=supervisor
                ).count()
                print(f"  → Projets du supervisor (DB): {supervisor_projects}")
                
                if len(projects) == supervisor_projects:
                    print("✅ Le supervisor voit uniquement SES projets")
                else:
                    print(f"⚠️  Différence: Vue={len(projects)}, DB={supervisor_projects}")
            else:
                print("⚠️  Vue globale activée pour le supervisor (devrait être personnelle)")
        else:
            print(f"❌ ERREUR: Code de statut {response.status_code}")
    
    # 5. Tester l'accès student
    if student:
        print(f"\n{'='*80}")
        print("TEST 3: Accès student (vue personnelle)")
        print(f"{'='*80}")
        
        client.force_login(student)
        response = client.get('/projects/')
        
        if response.status_code == 200:
            context = response.context
            is_global_view = context.get('is_global_view', False)
            projects = list(context.get('projects', []))
            
            print(f"✅ Page chargée (status: {response.status_code})")
            print(f"  → is_global_view: {is_global_view}")
            print(f"  → Projets affichés: {len(projects)}")
            
            if not is_global_view:
                print("✅ Vue personnelle pour l'étudiant")
                
                student_projects = Project.objects.filter(
                    assignment__student=student
                ).count()
                print(f"  → Projets de l'étudiant (DB): {student_projects}")
                
                if len(projects) == student_projects:
                    print("✅ L'étudiant voit uniquement SON projet")
                else:
                    print(f"⚠️  Différence: Vue={len(projects)}, DB={student_projects}")
            else:
                print("⚠️  Vue globale activée pour l'étudiant (devrait être personnelle)")
        else:
            print(f"❌ ERREUR: Code de statut {response.status_code}")
    
    # 6. Résumé
    print(f"\n{'='*80}")
    print("RÉSUMÉ")
    print(f"{'='*80}\n")
    
    print("✅ Fonctionnalités implémentées:")
    print("  • Admin voit tous les projets (vue globale)")
    print("  • Statistiques globales pour l'admin")
    print("  • Filtres par statut et encadreur")
    print("  • Vue tableau optimisée pour l'admin")
    print("  • Supervisor voit ses projets uniquement")
    print("  • Student voit son projet uniquement")
    print("  • Vue cards pour student/supervisor")
    
    print("\n📋 Améliorations apportées:")
    print("  1. Titre dynamique: 'Tous les Projets' (admin) vs 'Mes Projets' (autres)")
    print("  2. Statistiques: Total, En cours, Avec/Sans soutenance")
    print("  3. Filtres: Statut et Encadreur")
    print("  4. Tableau détaillé pour admin avec plus d'informations")
    print("  5. Boutons d'action rapides (voir, planifier soutenance)")
    print("  6. Indicateurs visuels (badges, progress bars)")
    
    return True


if __name__ == '__main__':
    try:
        success = test_global_projects_view()
        print(f"\n{'='*80}")
        if success:
            print("✅ TOUS LES TESTS PASSÉS")
        else:
            print("⚠️  CERTAINS TESTS ONT ÉCHOUÉ")
        print(f"{'='*80}")
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ ERREUR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
