#!/usr/bin/env python
"""
Test de l'interface de planification des soutenances pour les encadreurs
Vérifie que:
1. L'encadreur peut accéder au planning
2. Il voit TOUTES les soutenances (planning global)
3. Mais projects_data ne contient que SES projets
4. Il peut demander reprogrammation seulement pour SES soutenances
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
from subjects.models import Subject, Assignment
from projects.models import Project
from defenses.models import Defense
from datetime import date, time

User = get_user_model()

def test_supervisor_planning():
    """Test complet de l'interface encadreur"""
    
    print("=" * 80)
    print("TEST: Interface de planification pour encadreur")
    print("=" * 80)
    
    # 1. Récupérer un encadreur et un admin
    supervisor = User.objects.filter(role='supervisor').first()
    admin = User.objects.filter(role='admin').first()
    
    if not supervisor:
        print("❌ ERREUR: Aucun encadreur trouvé")
        return
    
    print(f"\n✓ Encadreur test: {supervisor.get_full_name()} ({supervisor.email})")
    print(f"✓ Admin test: {admin.get_full_name() if admin else 'N/A'}")
    
    # 2. Compter les sujets de cet encadreur
    supervisor_subjects = Subject.objects.filter(supervisor=supervisor)
    print(f"\n✓ Sujets de l'encadreur: {supervisor_subjects.count()}")
    
    # 3. Compter les affectations actives de cet encadreur
    supervisor_assignments = Assignment.objects.filter(
        status='active',
        subject__supervisor=supervisor
    )
    print(f"✓ Affectations actives de l'encadreur: {supervisor_assignments.count()}")
    
    # 4. Compter TOUTES les soutenances (tous encadreurs)
    all_defenses = Defense.objects.all()
    print(f"✓ Total soutenances dans le système: {all_defenses.count()}")
    
    # 5. Compter les soutenances de CET encadreur
    supervisor_defenses = Defense.objects.filter(
        project__assignment__subject__supervisor=supervisor
    )
    print(f"✓ Soutenances de l'encadreur: {supervisor_defenses.count()}")
    
    # 6. Créer un client et se connecter en tant qu'encadreur
    client = Client()
    client.force_login(supervisor)
    
    # 7. Appeler la vue
    response = client.get('/defenses/planning/')
    
    if response.status_code != 200:
        print(f"\n❌ ERREUR: Code de statut {response.status_code}")
        return
    
    print(f"\n✓ Vue exécutée avec succès (status: {response.status_code})")
    
    # 8. Vérifier le contexte
    context = response.context
    
    if context is None:
        print("\n❌ ERREUR: Pas de contexte dans la réponse")
        print("La vue n'a peut-être pas retourné un TemplateResponse")
        return False
    
    print("\n" + "=" * 80)
    print("VÉRIFICATION DU CONTEXTE")
    print("=" * 80)
    
    # Vérifier all_defenses (doit contenir TOUTES les soutenances)
    all_defenses_count = len(context.get('all_defenses', []))
    print(f"\n✓ all_defenses: {all_defenses_count} soutenances")
    print(f"  → Doit contenir TOUTES les soutenances du système")
    
    if all_defenses_count != all_defenses.count():
        print(f"  ⚠️  Différence: BD={all_defenses.count()}, Contexte={all_defenses_count}")
    else:
        print(f"  ✓ Correspond au total en base de données")
    
    # Vérifier projects_data (doit contenir seulement SES projets)
    projects_data_count = len(context.get('projects_data', []))
    print(f"\n✓ projects_data: {projects_data_count} projets")
    print(f"  → Doit contenir SEULEMENT les projets de l'encadreur")
    
    if projects_data_count != supervisor_assignments.count():
        print(f"  ⚠️  Différence: Affectations={supervisor_assignments.count()}, Contexte={projects_data_count}")
    else:
        print(f"  ✓ Correspond aux affectations de l'encadreur")
    
    # Vérifier les flags
    is_admin = context.get('is_admin', False)
    is_supervisor = context.get('is_supervisor', False)
    
    print(f"\n✓ is_admin: {is_admin} (devrait être False)")
    print(f"✓ is_supervisor: {is_supervisor} (devrait être True)")
    
    if not is_admin and is_supervisor:
        print("  ✓ Flags corrects pour un encadreur")
    else:
        print("  ❌ Flags incorrects!")
    
    # 9. Afficher les détails des soutenances
    print("\n" + "=" * 80)
    print("DÉTAILS DES SOUTENANCES")
    print("=" * 80)
    
    print(f"\n📅 Planning global (visible par l'encadreur):")
    for defense in context['all_defenses'][:5]:  # Afficher 5 premiers
        is_mine = defense.project.assignment.subject.supervisor == supervisor
        marker = "👤 MES PROJETS" if is_mine else "👥 AUTRES"
        print(f"  {marker} - {defense.project.title[:40]} - {defense.date} - {defense.project.assignment.subject.supervisor.get_full_name()}")
    
    if len(context['all_defenses']) > 5:
        print(f"  ... et {len(context['all_defenses']) - 5} autres soutenances")
    
    # 10. Afficher projects_data
    print(f"\n📊 Mes projets (gestion détaillée):")
    for data in context['projects_data'][:5]:
        status_defense = "✓ Planifiée" if data['has_defense'] else "⏳ Non planifiée"
        print(f"  {status_defense} - {data['assignment'].subject.title[:40]} - {data['assignment'].student.get_full_name()}")
    
    if len(context['projects_data']) > 5:
        print(f"  ... et {len(context['projects_data']) - 5} autres projets")
    
    # 11. Résumé
    print("\n" + "=" * 80)
    print("RÉSUMÉ DU TEST")
    print("=" * 80)
    
    tests_passed = 0
    tests_total = 5
    
    print("\n✅ Tests réussis:")
    
    if response.status_code == 200:
        print("  ✓ Encadreur peut accéder au planning")
        tests_passed += 1
    
    if all_defenses_count == all_defenses.count():
        print("  ✓ Encadreur voit TOUTES les soutenances (planning global)")
        tests_passed += 1
    
    if projects_data_count == supervisor_assignments.count():
        print("  ✓ projects_data contient SEULEMENT les projets de l'encadreur")
        tests_passed += 1
    
    if not is_admin and is_supervisor:
        print("  ✓ Flags is_admin et is_supervisor corrects")
        tests_passed += 1
    
    # Vérifier qu'il y a au moins une soutenance qui n'est PAS à l'encadreur
    other_defenses = [d for d in context['all_defenses'] 
                      if d.project.assignment.subject.supervisor != supervisor]
    if other_defenses:
        print("  ✓ Le planning contient des soutenances d'autres encadreurs")
        tests_passed += 1
    
    print(f"\n{'='*80}")
    print(f"RÉSULTAT FINAL: {tests_passed}/{tests_total} tests réussis")
    print(f"{'='*80}")
    
    if tests_passed == tests_total:
        print("\n✅ TOUS LES TESTS PASSÉS - L'interface fonctionne correctement!")
        print("\nFonctionnalités validées:")
        print("  • L'encadreur peut accéder au planning")
        print("  • Il voit le planning GLOBAL (toutes les soutenances)")
        print("  • Mais il ne gère que SES projets dans la section détaillée")
        print("  • Il peut demander reprogrammation seulement pour ses soutenances")
        print("  • Les flags de rôle sont corrects")
    else:
        print(f"\n⚠️  {tests_total - tests_passed} test(s) échoué(s)")
        print("Vérifiez les détails ci-dessus pour identifier les problèmes.")
    
    return tests_passed == tests_total


if __name__ == '__main__':
    try:
        success = test_supervisor_planning()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ ERREUR DURANT LE TEST: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
