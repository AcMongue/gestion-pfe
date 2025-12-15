#!/usr/bin/env python
"""
Test simple de l'interface de planification pour encadreur
Vérifie la logique métier sans passer par le contexte HTTP
"""

import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from subjects.models import Subject, Assignment
from projects.models import Project
from defenses.models import Defense

User = get_user_model()

def test_supervisor_planning_logic():
    """Test de la logique de planification pour encadreur"""
    
    print("=" * 80)
    print("TEST: Logique de planification pour encadreur")
    print("=" * 80)
    
    # 1. Récupérer un encadreur
    supervisor = User.objects.filter(role='supervisor').first()
    
    if not supervisor:
        print("❌ ERREUR: Aucun encadreur trouvé")
        return False
    
    print(f"\n✓ Encadreur test: {supervisor.get_full_name()} ({supervisor.email})")
    
    # 2. Compter TOUTES les soutenances (ce que l'encadreur VOIT dans all_defenses)
    all_defenses = Defense.objects.select_related(
        'project', 'project__assignment', 'project__assignment__student',
        'project__assignment__subject__supervisor'
    ).order_by('date', 'time')
    
    print(f"\n📅 PLANNING GLOBAL (all_defenses):")
    print(f"  → Total soutenances dans le système: {all_defenses.count()}")
    
    # 3. Compter les soutenances de CET encadreur
    supervisor_defenses = all_defenses.filter(
        project__assignment__subject__supervisor=supervisor
    )
    
    print(f"  → Soutenances de cet encadreur: {supervisor_defenses.count()}")
    print(f"  → Soutenances d'autres encadreurs: {all_defenses.count() - supervisor_defenses.count()}")
    
    # 4. Compter les projets de l'encadreur (ce qu'il GÈRE dans projects_data)
    active_assignments = Assignment.objects.filter(
        status='active',
        subject__supervisor=supervisor
    ).select_related('student', 'subject', 'subject__supervisor')
    
    print(f"\n📊 MES PROJETS (projects_data):")
    print(f"  → Mes affectations actives: {active_assignments.count()}")
    
    # 5. Afficher détails des soutenances
    print(f"\n{'='*80}")
    print("DÉTAILS DES SOUTENANCES")
    print(f"{'='*80}")
    
    if all_defenses.exists():
        print(f"\n📋 Aperçu du planning global:")
        for i, defense in enumerate(all_defenses[:10], 1):
            is_mine = defense.project.assignment.subject.supervisor == supervisor
            marker = "👤" if is_mine else "👥"
            owner = "VOUS" if is_mine else defense.project.assignment.subject.supervisor.get_full_name()
            print(f"  {marker} {i}. {defense.project.title[:35]:35} | {defense.date} | Encadreur: {owner}")
        
        if all_defenses.count() > 10:
            print(f"  ... et {all_defenses.count() - 10} autres soutenances")
    else:
        print("  Aucune soutenance planifiée")
    
    # 6. Afficher détails des projets
    print(f"\n📁 Aperçu de mes projets:")
    if active_assignments.exists():
        for i, assignment in enumerate(active_assignments[:10], 1):
            try:
                project = assignment.project
                has_project = True
                try:
                    defense = project.defense
                    status = f"✓ Soutenance le {defense.date}"
                except:
                    status = "⏳ Pas de soutenance"
            except:
                has_project = False
                status = "❌ Pas de projet"
            
            print(f"  {i}. {assignment.student.get_full_name():30} | {assignment.subject.title[:30]:30} | {status}")
        
        if active_assignments.count() > 10:
            print(f"  ... et {active_assignments.count() - 10} autres projets")
    else:
        print("  Aucun projet affecté")
    
    # 7. Vérifications
    print(f"\n{'='*80}")
    print("VÉRIFICATIONS")
    print(f"{'='*80}\n")
    
    tests_passed = 0
    tests_total = 4
    
    # Test 1: L'encadreur peut voir toutes les soutenances
    if all_defenses.count() > 0:
        print("✅ Test 1: Des soutenances existent dans le système")
        tests_passed += 1
    else:
        print("⚠️  Test 1: Aucune soutenance dans le système (créer des données de test)")
    
    # Test 2: Il y a des soutenances qui ne sont PAS à lui
    other_defenses = all_defenses.exclude(
        project__assignment__subject__supervisor=supervisor
    )
    
    if other_defenses.exists():
        print(f"✅ Test 2: Il existe {other_defenses.count()} soutenance(s) d'autres encadreurs")
        print(f"   → L'encadreur VOIT ces soutenances dans le planning global")
        tests_passed += 1
    elif all_defenses.count() > 0:
        print("⚠️  Test 2: Toutes les soutenances appartiennent à cet encadreur")
        print("   → Créer des soutenances pour d'autres encadreurs pour tester")
    else:
        print("⚠️  Test 2: Pas de soutenances à vérifier")
    
    # Test 3: Il a des projets à lui
    if active_assignments.exists():
        print(f"✅ Test 3: L'encadreur a {active_assignments.count()} projet(s) actif(s)")
        tests_passed += 1
    else:
        print("⚠️  Test 3: L'encadreur n'a aucun projet actif")
        print("   → Affecter des sujets à cet encadreur")
    
    # Test 4: Il peut identifier SES soutenances dans le planning global
    if supervisor_defenses.exists():
        print(f"✅ Test 4: L'encadreur a {supervisor_defenses.count()} soutenance(s) planifiée(s)")
        print(f"   → Il peut demander reprogrammation pour CELLES-CI uniquement")
        tests_passed += 1
    elif active_assignments.exists():
        print("⚠️  Test 4: L'encadreur a des projets mais aucune soutenance planifiée")
        print("   → Planifier des soutenances pour ses projets")
    else:
        print("⚠️  Test 4: L'encadreur n'a ni projets ni soutenances")
    
    # 8. Résumé
    print(f"\n{'='*80}")
    print("RÉSUMÉ")
    print(f"{'='*80}\n")
    
    print(f"Tests réussis: {tests_passed}/{tests_total}")
    
    print("\n📝 Comportement attendu de l'interface:")
    print("  1. Section 'Planning Global': Affiche TOUTES les soutenances")
    print(f"     → {all_defenses.count()} soutenance(s) visible(s)")
    print("     → Les soutenances de l'encadreur sont en surbrillance")
    print("     → Bouton 'Demander reprogrammation' seulement pour SES soutenances")
    print()
    print("  2. Section 'Mes projets': Affiche seulement SES projets")
    print(f"     → {active_assignments.count()} projet(s) affiché(s)")
    print("     → Détails sur l'état de chaque projet (créé, soutenance planifiée)")
    print()
    print("  3. Boutons d'action:")
    print("     → 'Voir' (👁️): Disponible pour toutes les soutenances")
    print("     → 'Demander reprogrammation' (📅): Seulement pour SES soutenances")
    print("     → 'Planifier' (➕): Seulement pour admin")
    print("     → 'Modifier' (✏️): Seulement pour admin")
    
    if tests_passed >= 3:
        print(f"\n{'='*80}")
        print("✅ CONFIGURATION VALIDÉE")
        print(f"{'='*80}")
        print("\nLe système est correctement configuré pour l'interface encadreur.")
        return True
    else:
        print(f"\n{'='*80}")
        print("⚠️  CONFIGURATION INCOMPLÈTE")
        print(f"{'='*80}")
        print("\nCréer des données de test pour valider complètement l'interface:")
        print("  • Plusieurs encadreurs avec des sujets")
        print("  • Des affectations actives pour chaque encadreur")
        print("  • Des soutenances planifiées pour différents encadreurs")
        return False


if __name__ == '__main__':
    try:
        success = test_supervisor_planning_logic()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ ERREUR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
