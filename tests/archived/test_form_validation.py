"""
Test détaillé de l'inscription avec affichage des erreurs
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from users.forms import UserRegistrationForm

def test_form_validation():
    print("=" * 80)
    print("TEST DÉTAILLÉ DES FORMULAIRES D'INSCRIPTION")
    print("=" * 80)
    
    # Test 1: Étudiant
    print("\n[1] Test Etudiant")
    print("-" * 80)
    student_data = {
        'username': 'test_student_unique',
        'email': 'test.student@enspd.edu',
        'first_name': 'Test',
        'last_name': 'Student',
        'role': 'student',
        'matricule': '2024TEST999',
        'level': 'M2',
        'filiere': 'GIT',
        'password1': 'TestPassword123!',
        'password2': 'TestPassword123!',
    }
    
    form = UserRegistrationForm(data=student_data)
    print(f"Données soumises: {list(student_data.keys())}")
    print(f"Form valide? {form.is_valid()}")
    
    if form.is_valid():
        print("[OK] Formulaire etudiant valide")
        user = form.save()
        print(f"   Créé: {user.username} ({user.role})")
        user.delete()
    else:
        print("[ERREUR] Erreurs:")
        for field, errors in form.errors.items():
            print(f"   {field}: {errors}")
    
    # Test 2: Encadreur
    print("\n[2] Test Encadreur")
    print("-" * 80)
    supervisor_data = {
        'username': 'test_supervisor_unique',
        'email': 'test.supervisor@enspd.edu',
        'first_name': 'Test',
        'last_name': 'Supervisor',
        'role': 'supervisor',
        'filiere': 'GESI',
        'academic_title': 'professeur',
        'specialite': 'Test Specialité',
        'max_students': 5,
        'password1': 'TestPassword123!',
        'password2': 'TestPassword123!',
    }
    
    form = UserRegistrationForm(data=supervisor_data)
    print(f"Données soumises: {list(supervisor_data.keys())}")
    print(f"Form valide? {form.is_valid()}")
    
    if form.is_valid():
        print("[OK] Formulaire encadreur valide")
        user = form.save()
        print(f"   Cree: {user.username} ({user.role})")
        print(f"   Departement: {user.filiere}")
        print(f"   Grade: {user.academic_title}")
        user.delete()
    else:
        print("[ERREUR] Erreurs:")
        for field, errors in form.errors.items():
            print(f"   {field}: {errors}")
    
    # Test 3: Admin
    print("\n[3] Test Admin")
    print("-" * 80)
    admin_data = {
        'username': 'test_admin_unique',
        'email': 'test.admin@enspd.edu',
        'first_name': 'Test',
        'last_name': 'Admin',
        'role': 'admin',
        'filiere': 'GAM',
        'password1': 'TestPassword123!',
        'password2': 'TestPassword123!',
    }
    
    form = UserRegistrationForm(data=admin_data)
    print(f"Données soumises: {list(admin_data.keys())}")
    print(f"Form valide? {form.is_valid()}")
    
    if form.is_valid():
        print("[OK] Formulaire admin valide")
        user = form.save()
        print(f"   Cree: {user.username} ({user.role})")
        print(f"   Departement: {user.filiere}")
        user.delete()
    else:
        print("[ERREUR] Erreurs:")
        for field, errors in form.errors.items():
            print(f"   {field}: {errors}")
    
    # Test 4: Vérifier les champs du formulaire
    print("\n[4] Analyse de la structure du formulaire")
    print("-" * 80)
    form = UserRegistrationForm()
    print(f"Champs disponibles dans le formulaire:")
    for field_name in form.fields:
        field = form.fields[field_name]
        required = "Obligatoire" if field.required else "Optionnel"
        print(f"   - {field_name}: {required}")
    
    print("\n" + "=" * 80)
    print("[OK] Tests termines")
    print("=" * 80)

if __name__ == '__main__':
    test_form_validation()
