"""
Script de debug pour identifier les problemes d'inscription web
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.test import Client

def test_registration_via_http():
    print("=" * 80)
    print("TEST INSCRIPTION VIA HTTP (simulation navigateur)")
    print("=" * 80)
    
    client = Client()
    
    # Test 1: Etudiant
    print("\n[1] Test inscription Etudiant via POST")
    print("-" * 80)
    
    response = client.get('/users/register/')
    print(f"GET /users/register/ -> {response.status_code}")
    
    student_data = {
        'username': 'webtest_student',
        'email': 'webtest.student@enspd.edu',
        'first_name': 'Web',
        'last_name': 'Student',
        'role': 'student',
        'matricule': '2024WEBTEST001',
        'level': 'M2',
        'filiere': 'GIT',
        'password1': 'TestWebPassword123!',
        'password2': 'TestWebPassword123!',
    }
    
    response = client.post('/users/register/', student_data)
    print(f"POST /users/register/ -> {response.status_code}")
    
    if response.status_code == 302:
        print("[OK] Redirection reussie - inscription OK")
        print(f"   Redirection vers: {response.url}")
    else:
        print("[ERREUR] Pas de redirection - formulaire a des erreurs")
        if hasattr(response, 'context') and response.context and 'form' in response.context:
            form = response.context['form']
            if form.errors:
                print("   Erreurs du formulaire:")
                for field, errors in form.errors.items():
                    print(f"     - {field}: {errors}")
            else:
                print("   Aucune erreur specifique trouvee dans le contexte")
    
    # Test 2: Encadreur
    print("\n[2] Test inscription Encadreur via POST")
    print("-" * 80)
    
    supervisor_data = {
        'username': 'webtest_supervisor',
        'email': 'webtest.supervisor@enspd.edu',
        'first_name': 'Web',
        'last_name': 'Supervisor',
        'role': 'supervisor',
        'filiere': 'GESI',
        'academic_title': 'maitre_conference',
        'specialite': 'Test Specialite Web',
        'max_students': '5',
        'password1': 'TestWebPassword123!',
        'password2': 'TestWebPassword123!',
    }
    
    response = client.post('/users/register/', supervisor_data)
    print(f"POST /users/register/ -> {response.status_code}")
    
    if response.status_code == 302:
        print("[OK] Redirection reussie - inscription OK")
        print(f"   Redirection vers: {response.url}")
    else:
        print("[ERREUR] Pas de redirection - formulaire a des erreurs")
        if hasattr(response, 'context') and response.context and 'form' in response.context:
            form = response.context['form']
            if form.errors:
                print("   Erreurs du formulaire:")
                for field, errors in form.errors.items():
                    print(f"     - {field}: {errors}")
    
    # Test 3: Admin
    print("\n[3] Test inscription Admin via POST")
    print("-" * 80)
    
    admin_data = {
        'username': 'webtest_admin',
        'email': 'webtest.admin@enspd.edu',
        'first_name': 'Web',
        'last_name': 'Admin',
        'role': 'admin',
        'filiere': 'GAM',
        'password1': 'TestWebPassword123!',
        'password2': 'TestWebPassword123!',
    }
    
    response = client.post('/users/register/', admin_data)
    print(f"POST /users/register/ -> {response.status_code}")
    
    if response.status_code == 302:
        print("[OK] Redirection reussie - inscription OK")
        print(f"   Redirection vers: {response.url}")
    else:
        print("[ERREUR] Pas de redirection - formulaire a des erreurs")
        if hasattr(response, 'context') and response.context and 'form' in response.context:
            form = response.context['form']
            if form.errors:
                print("   Erreurs du formulaire:")
                for field, errors in form.errors.items():
                    print(f"     - {field}: {errors}")
    
    print("\n" + "=" * 80)
    print("[INFO] Verifications des utilisateurs crees")
    print("=" * 80)
    
    from users.models import User
    
    web_users = User.objects.filter(username__startswith='webtest')
    print(f"Utilisateurs webtest trouves: {web_users.count()}")
    for user in web_users:
        print(f"  - {user.username} ({user.role}) - Email: {user.email}")
    
    # Nettoyage
    if web_users.exists():
        print("\n[CLEANUP] Suppression des utilisateurs de test...")
        web_users.delete()
        print("[OK] Nettoyage termine")
    
    print("\n" + "=" * 80)
    print("[OK] Tests HTTP termines")
    print("=" * 80)

if __name__ == '__main__':
    test_registration_via_http()
