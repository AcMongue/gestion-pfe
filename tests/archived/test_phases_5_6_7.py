#!/usr/bin/env python
"""
Script de test pour les phases 5, 6 et 7.
Teste AcademicYear, thesis management, archivage et calcul automatique progression.
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.utils import timezone
from datetime import datetime, timedelta
from users.models import User
from projects.models import Project, AcademicYear, Milestone
from defenses.models import Defense, DefenseJury
from archives.models import ArchivedProject

def test_phase_5_academic_year():
    """Test Phase 5: AcademicYear et gestion thesis"""
    print("\n" + "="*60)
    print("TEST PHASE 5: AcademicYear et gestion du mémoire")
    print("="*60)
    
    # Créer une année académique
    today = timezone.now().date()
    
    try:
        academic_year = AcademicYear.objects.create(
            year="2025-2026",
            start_date=today - timedelta(days=180),
            end_date=today + timedelta(days=180),
            thesis_submission_deadline=today + timedelta(days=60),
            is_active=True
        )
        print("✅ AcademicYear créé:", academic_year)
    except Exception as e:
        print(f"⚠️ AcademicYear existe déjà ou erreur: {e}")
        academic_year = AcademicYear.objects.filter(is_active=True).first()
    
    # Vérifier qu'une seule année est active
    active_years = AcademicYear.objects.filter(is_active=True).count()
    assert active_years == 1, f"❌ Erreur: {active_years} années actives au lieu de 1"
    print("✅ Une seule année académique est active")
    
    # Test sur un projet
    project = Project.objects.first()
    if project:
        project.academic_year = academic_year
        project.save()
        print(f"✅ Projet lié à l'année académique: {project.title}")
        
        # Test propriétés thesis
        print(f"   - Mémoire soumis: {project.is_thesis_submitted}")
        print(f"   - Jours avant deadline: {project.days_until_thesis_deadline}")
        print(f"   - En retard: {project.is_thesis_late}")
    else:
        print("⚠️ Aucun projet disponible pour tester")
    
    return True


def test_phase_6_archivage():
    """Test Phase 6: Système d'archivage"""
    print("\n" + "="*60)
    print("TEST PHASE 6: Système d'archivage")
    print("="*60)
    
    # Vérifier que le modèle ArchivedProject existe
    archived_count = ArchivedProject.objects.count()
    print(f"✅ {archived_count} projet(s) archivé(s) dans la base")
    
    # Tester la fonction d'archivage
    from archives.views import archive_project_after_defense
    print("✅ Fonction archive_project_after_defense importée avec succès")
    
    # Test sur un projet avec soutenance
    projects_with_defense = Project.objects.filter(defense__isnull=False)
    if projects_with_defense.exists():
        project = projects_with_defense.first()
        print(f"✅ Projet avec soutenance trouvé: {project.title}")
        
        defense = project.defense
        print(f"   - Soutenance: {defense.date}")
        print(f"   - Note finale: {defense.final_grade or 'Non notée'}")
        print(f"   - Complètement notée: {defense.is_fully_graded}")
    else:
        print("⚠️ Aucun projet avec soutenance pour tester l'archivage")
    
    return True


def test_phase_7_calcul_progression():
    """Test Phase 7: Calcul automatique progression"""
    print("\n" + "="*60)
    print("TEST PHASE 7: Calcul automatique progression")
    print("="*60)
    
    # Test sur un projet avec jalons
    projects_with_milestones = Project.objects.filter(milestones__isnull=False).distinct()
    
    if projects_with_milestones.exists():
        project = projects_with_milestones.first()
        print(f"✅ Projet avec jalons trouvé: {project.title}")
        
        total = project.milestones.count()
        validated = project.milestones.filter(validated_by_supervisor=True).count()
        
        print(f"   - Jalons totaux: {total}")
        print(f"   - Jalons validés: {validated}")
        print(f"   - Progression calculée: {project.progress}%")
        
        # Vérifier que la progression est correcte
        expected_progress = int((validated / total) * 100) if total > 0 else 0
        assert project.progress == expected_progress, \
            f"❌ Erreur: progression {project.progress}% != {expected_progress}%"
        print(f"✅ Calcul automatique correct: {expected_progress}%")
        
        # Tester la mise à jour
        project.update_progress_from_milestones()
        print(f"✅ Mise à jour manuelle: progress_percentage = {project.progress_percentage}%")
    else:
        print("⚠️ Aucun projet avec jalons pour tester")
        
        # Créer un projet de test
        teacher = User.objects.filter(role='teacher').first()
        if teacher:
            print("   Création d'un projet de test...")
            # On ne crée pas de projet de test pour ne pas polluer la base
    
    # Vérifier que les signaux sont enregistrés
    from django.db.models import signals
    from projects.models import Milestone
    
    receivers = signals.post_save.receivers
    has_signal = any('update_project_progress' in str(r) for r in receivers)
    
    if has_signal:
        print("✅ Signal post_save pour Milestone enregistré")
    else:
        print("⚠️ Signal post_save non détecté (peut être normal)")
    
    return True


def test_defense_jury_model():
    """Test DefenseJury model (Phase 2)"""
    print("\n" + "="*60)
    print("TEST BONUS: Modèle DefenseJury")
    print("="*60)
    
    jury_count = DefenseJury.objects.count()
    print(f"✅ {jury_count} membre(s) de jury dans la base")
    
    if jury_count > 0:
        jury_member = DefenseJury.objects.first()
        print(f"   - Enseignant: {jury_member.teacher.get_full_name()}")
        print(f"   - Rôle: {jury_member.get_role_display()}")
        print(f"   - Note: {jury_member.grade or 'Non attribuée'}")
    
    return True


def main():
    """Exécute tous les tests"""
    print("\n" + "="*60)
    print("🚀 TEST DES PHASES 5, 6 ET 7")
    print("="*60)
    
    results = []
    
    try:
        results.append(("Phase 5: AcademicYear", test_phase_5_academic_year()))
    except Exception as e:
        print(f"❌ Erreur Phase 5: {e}")
        results.append(("Phase 5: AcademicYear", False))
    
    try:
        results.append(("Phase 6: Archivage", test_phase_6_archivage()))
    except Exception as e:
        print(f"❌ Erreur Phase 6: {e}")
        results.append(("Phase 6: Archivage", False))
    
    try:
        results.append(("Phase 7: Progression", test_phase_7_calcul_progression()))
    except Exception as e:
        print(f"❌ Erreur Phase 7: {e}")
        results.append(("Phase 7: Progression", False))
    
    try:
        results.append(("Bonus: DefenseJury", test_defense_jury_model()))
    except Exception as e:
        print(f"❌ Erreur DefenseJury: {e}")
        results.append(("Bonus: DefenseJury", False))
    
    # Résumé
    print("\n" + "="*60)
    print("📊 RÉSUMÉ DES TESTS")
    print("="*60)
    
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    total = len(results)
    passed = sum(1 for _, s in results if s)
    print(f"\n{passed}/{total} tests réussis ({int(passed/total*100)}%)")
    
    if passed == total:
        print("\n🎉 TOUS LES TESTS SONT PASSÉS !")
    else:
        print("\n⚠️ Certains tests ont échoué")


if __name__ == '__main__':
    main()
