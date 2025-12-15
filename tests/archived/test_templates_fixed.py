"""
Test des templates corrigés pour l'encadreur
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model

User = get_user_model()

def test_supervisor_pages():
    """Teste les pages encadreur après corrections."""
    print("=" * 80)
    print("TEST DES TEMPLATES CORRIGÉS")
    print("=" * 80)
    
    # Créer un client
    client = Client()
    
    # Obtenir ou créer un superviseur
    supervisor = User.objects.filter(role='supervisor').first()
    if not supervisor:
        print("❌ Aucun encadreur trouvé dans la base")
        print("💡 Utilisez: python create_demo_supervisor.py")
        return
    
    print(f"\n✅ Encadreur: {supervisor.username}")
    
    # Login
    client.force_login(supervisor)
    
    # Test des URLs
    urls_to_test = [
        ('/projects/supervisor/students/', 'Mes Étudiants'),
        ('/subjects/proposals/', 'Propositions reçues'),
    ]
    
    print("\n" + "=" * 80)
    print("TESTS DES PAGES")
    print("=" * 80)
    
    for url, name in urls_to_test:
        try:
            response = client.get(url)
            if response.status_code == 200:
                print(f"✅ {name}: OK (200)")
                # Vérifier quelques éléments de contenu
                content = response.content.decode('utf-8')
                if 'TemplateSyntaxError' in content:
                    print(f"   ⚠️  Erreur de template détectée dans le contenu")
                else:
                    print(f"   📄 Template rendu sans erreur")
            else:
                print(f"❌ {name}: Code {response.status_code}")
        except Exception as e:
            print(f"❌ {name}: Erreur - {str(e)}")
    
    print("\n" + "=" * 80)
    print("RÉSUMÉ")
    print("=" * 80)
    print("✅ Tests terminés")
    print("\n💡 Pour tester manuellement:")
    print("   1. Connectez-vous avec: supervisor_demo / demo123")
    print("   2. Visitez:")
    print(f"      - http://127.0.0.1:8000/projects/supervisor/students/")
    print(f"      - http://127.0.0.1:8000/subjects/proposals/")

if __name__ == '__main__':
    test_supervisor_pages()
