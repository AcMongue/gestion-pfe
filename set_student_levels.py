#!/usr/bin/env python
"""Script pour définir le niveau des étudiants existants."""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from users.models import User

print("=" * 60)
print("MISE À JOUR DES NIVEAUX DES ÉTUDIANTS")
print("=" * 60)

# Récupérer tous les étudiants sans niveau
students_without_level = User.objects.filter(role='student', level__isnull=True)

print(f"\n📊 {students_without_level.count()} étudiant(s) sans niveau défini\n")

for student in students_without_level:
    print(f"Étudiant: {student.username} ({student.get_full_name()})")
    print("Niveaux disponibles:")
    print("  1. L3 - Licence 3")
    print("  2. M2 - Master 2")
    print("  3. DOC - Doctorat")
    
    choice = input("Choisissez le niveau (1-3) ou Enter pour sauter: ").strip()
    
    if choice == '1':
        student.level = 'L3'
        student.save()
        print(f"✅ Niveau L3 attribué à {student.username}\n")
    elif choice == '2':
        student.level = 'M2'
        student.save()
        print(f"✅ Niveau M2 attribué à {student.username}\n")
    elif choice == '3':
        student.level = 'DOC'
        student.save()
        print(f"✅ Niveau DOC attribué à {student.username}\n")
    else:
        print(f"⏭️  Sauté\n")

print("\n" + "=" * 60)
print("TERMINÉ!")
print("=" * 60)

# Afficher le résumé
students_with_level = User.objects.filter(role='student', level__isnull=False)
print(f"\n✅ {students_with_level.count()} étudiant(s) avec niveau défini")
students_without_level = User.objects.filter(role='student', level__isnull=True)
print(f"⚠️  {students_without_level.count()} étudiant(s) sans niveau")
