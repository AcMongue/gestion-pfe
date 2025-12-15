"""
Test du processus d'inscription avec les nouvelles listes déroulantes ENSPD
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.test import TestCase, override_settings
from users.models import User
from users.forms import UserRegistrationForm

@override_settings(ALLOWED_HOSTS=['*'])
def test_registration_process():
    """Test complet du processus d'inscription pour chaque rôle"""
    
    print("=" * 80)
    print("TEST DU PROCESSUS D'INSCRIPTION ENSPD")
    print("=" * 80)
    
    # Test 1: Inscription d'un étudiant via le formulaire
    print("\n1️⃣  TEST: Inscription ÉTUDIANT")
    print("-" * 80)
    
    student_data = {
        'username': 'etudiant_test_git',
        'email': 'etudiant.git@enspd.edu',
        'first_name': 'Jean',
        'last_name': 'Dupont',
        'role': 'student',
        'matricule': '2024GIT001',
        'level': 'M2',
        'filiere': 'GIT',  # Génie Informatique & Télécommunications
        'password1': 'TestPass123!',
        'password2': 'TestPass123!',
    }
    
    form = UserRegistrationForm(data=student_data)
    
    if form.is_valid():
        student = form.save()
        print("✅ Inscription étudiant réussie!")
        print(f"   - Username: {student.username}")
        print(f"   - Rôle: {student.role}")
        print(f"   - Matricule: {student.matricule}")
        print(f"   - Niveau: {student.level}")
        print(f"   - Filière: {student.filiere} ({student.get_filiere_display()})")
    else:
        print("❌ Erreur lors de l'inscription étudiant")
        print(f"   Erreurs: {form.errors}")
    
    # Test 2: Inscription d'un encadreur
    print("\n2️⃣  TEST: Inscription ENCADREUR")
    print("-" * 80)
    
    supervisor_data = {
        'username': 'encadreur_test_gesi',
        'email': 'encadreur.gesi@enspd.edu',
        'first_name': 'Marie',
        'last_name': 'Martin',
        'role': 'supervisor',
        'filiere': 'GESI',  # Génie Électrique et Systèmes Intelligents
        'academic_title': 'professeur',
        'specialite': 'Intelligence Artificielle et Systèmes Embarqués',
        'max_students': 6,
        'password1': 'TestPass123!',
        'password2': 'TestPass123!',
    }
    
    form = UserRegistrationForm(data=supervisor_data)
    
    if form.is_valid():
        supervisor = form.save()
        print("✅ Inscription encadreur réussie!")
        print(f"   - Username: {supervisor.username}")
        print(f"   - Rôle: {supervisor.role}")
        print(f"   - Département: {supervisor.filiere} ({supervisor.get_filiere_display()})")
        print(f"   - Grade: {supervisor.academic_title} ({supervisor.get_academic_title_display()})")
        print(f"   - Spécialité: {supervisor.specialite}")
        print(f"   - Max étudiants: {supervisor.max_students}")
        print(f"   - Peut être président de jury: {supervisor.can_be_jury_president}")
    else:
        print("❌ Erreur lors de l'inscription encadreur")
        print(f"   Erreurs: {form.errors}")
    
    # Test 3: Inscription d'un administrateur
    print("\n3️⃣  TEST: Inscription ADMINISTRATEUR")
    print("-" * 80)
    
    admin_data = {
        'username': 'admin_test_gam',
        'email': 'admin.gam@enspd.edu',
        'first_name': 'Pierre',
        'last_name': 'Durand',
        'role': 'admin',
        'filiere': 'GAM',  # Génie Automobile et Mécatronique
        'password1': 'TestPass123!',
        'password2': 'TestPass123!',
    }
    
    form = UserRegistrationForm(data=admin_data)
    
    if form.is_valid():
        admin = form.save()
        print("✅ Inscription administrateur réussie!")
        print(f"   - Username: {admin.username}")
        print(f"   - Rôle: {admin.role}")
        print(f"   - Département: {admin.filiere} ({admin.get_filiere_display()})")
    else:
        print("❌ Erreur lors de l'inscription administrateur")
        print(f"   Erreurs: {form.errors}")
    
    # Test 4: Vérification des validations
    print("\n4️⃣  TEST: Validation des champs obligatoires")
    print("-" * 80)
    
    # Étudiant sans matricule
    invalid_student = {
        'username': 'etudiant_invalide',
        'email': 'invalide@enspd.edu',
        'first_name': 'Test',
        'last_name': 'Invalide',
        'role': 'student',
        # Pas de matricule, level, filiere
        'password1': 'TestPass123!',
        'password2': 'TestPass123!',
    }
    
    form = UserRegistrationForm(data=invalid_student)
    
    if not form.is_valid():
        print("✅ Validation fonctionne: étudiant sans matricule rejeté")
        print(f"   Erreurs attendues: {list(form.errors.keys())}")
    else:
        print("❌ Validation ne fonctionne pas correctement")
    
    # Test 5: Résumé des utilisateurs créés
    print("\n" + "=" * 80)
    print("RÉSUMÉ DES UTILISATEURS PAR FILIÈRE")
    print("=" * 80)
    
    for filiere_code, filiere_name in User.FILIERE_CHOICES:
        users_count = User.objects.filter(filiere=filiere_code).count()
        if users_count > 0:
            print(f"\n📚 {filiere_name} ({filiere_code}): {users_count} utilisateur(s)")
            users = User.objects.filter(filiere=filiere_code)
            for user in users:
                role_icon = {
                    'student': '🎓',
                    'supervisor': '👨‍🏫',
                    'admin': '👔',
                    'jury': '⚖️'
                }.get(user.role, '👤')
                print(f"   {role_icon} {user.get_full_name()} ({user.username}) - {user.get_role_display()}")
    
    # Test 6: Vérification des grades académiques
    print("\n" + "=" * 80)
    print("ENCADREURS PAR GRADE ACADÉMIQUE")
    print("=" * 80)
    
    supervisors = User.objects.filter(role='supervisor')
    if supervisors.exists():
        for title_code, title_name in User.ACADEMIC_TITLE_CHOICES:
            sups = supervisors.filter(academic_title=title_code)
            if sups.exists():
                print(f"\n🎓 {title_name}:")
                for sup in sups:
                    can_preside = "✅ Peut présider" if sup.can_be_jury_president else "❌ Ne peut pas présider"
                    print(f"   - {sup.get_full_name()} ({sup.get_filiere_display()}) - {can_preside}")
    else:
        print("Aucun encadreur inscrit")
    
    print("\n" + "=" * 80)
    print("✅ TESTS TERMINÉS")
    print("=" * 80)
    
    # Nettoyage (optionnel - commenter pour garder les données)
    print("\n🧹 Nettoyage des données de test...")
    User.objects.filter(username__contains='test').delete()
    print("✅ Données de test supprimées")

if __name__ == '__main__':
    test_registration_process()
