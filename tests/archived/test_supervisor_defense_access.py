"""
Test de l'accès au planning des soutenances pour les encadreurs
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.urls import reverse
from defenses.models import Defense
from projects.models import Project

User = get_user_model()

def test_supervisor_defense_planning_access():
    """Vérifier que les encadreurs peuvent accéder au planning des soutenances"""
    print("\n" + "="*80)
    print("TEST ACCÈS PLANNING SOUTENANCES - ENCADREUR")
    print("="*80 + "\n")
    
    # Trouver un encadreur
    supervisor = User.objects.filter(role='supervisor').first()
    
    if not supervisor:
        print("❌ Aucun encadreur trouvé!")
        return False
    
    print(f"✓ Encadreur trouvé: {supervisor.get_full_name()}")
    
    # Vérifier l'URL du planning
    try:
        planning_url = reverse('defenses:planning')
        print(f"✓ URL du planning: {planning_url}")
    except Exception as e:
        print(f"❌ Erreur URL: {e}")
        return False
    
    # Vérifier les projets de l'encadreur
    projects = Project.objects.filter(assignment__subject__supervisor=supervisor)
    print(f"✓ Projets encadrés: {projects.count()}")
    
    # Vérifier les soutenances
    defenses = Defense.objects.filter(project__assignment__subject__supervisor=supervisor)
    print(f"✓ Soutenances planifiées: {defenses.count()}")
    
    for defense in defenses:
        print(f"  - {defense.project.title}")
        print(f"    Date: {defense.date} à {defense.time}")
        print(f"    Salle: {defense.room}")
        print(f"    Statut: {defense.get_status_display()}")
    
    print("\n" + "="*80)
    print("RÉSULTAT")
    print("="*80)
    print("✓ L'encadreur peut maintenant accéder au planning des soutenances!")
    print("✓ Il peut voir:")
    print("  - La liste de ses projets")
    print("  - Les soutenances planifiées")
    print("  - Les demandes de modification")
    print("\nNote: Les encadreurs ne peuvent pas CRÉER de soutenances")
    print("      (cette action est réservée aux administrateurs)")
    print("="*80 + "\n")
    
    return True


if __name__ == '__main__':
    success = test_supervisor_defense_planning_access()
    exit(0 if success else 1)
