#!/usr/bin/env python
"""Script pour déboguer le problème de visibilité des sujets."""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from subjects.models import Subject
from users.models import User

print("=" * 60)
print("DIAGNOSTIC: Visibilité des sujets")
print("=" * 60)

# Liste tous les sujets
subjects = Subject.objects.all()
print(f"\n📚 Nombre total de sujets: {subjects.count()}")
for subject in subjects:
    print(f"\n  Sujet #{subject.id}: {subject.title}")
    print(f"    - Statut: {subject.status}")
    print(f"    - Niveau: {subject.level}")
    print(f"    - Encadreur: {subject.supervisor.get_full_name()}")

# Liste tous les étudiants
students = User.objects.filter(role='student')
print(f"\n👨‍🎓 Nombre d'étudiants: {students.count()}")
for student in students:
    print(f"\n  Étudiant: {student.username} ({student.get_full_name()})")
    print(f"    - Niveau: {student.level if hasattr(student, 'level') else 'NON DÉFINI'}")
    
    # Sujets visibles pour cet étudiant
    if hasattr(student, 'level') and student.level:
        visible_subjects = Subject.objects.filter(status='published', level=student.level)
        print(f"    - Sujets visibles: {visible_subjects.count()}")
        for subj in visible_subjects:
            print(f"      • {subj.title}")
    else:
        print(f"    - ⚠️ PROBLÈME: Niveau non défini!")

print("\n" + "=" * 60)
print("SOLUTION:")
print("=" * 60)
print("Si un étudiant n'a pas de niveau défini, connectez-vous")
print("avec son compte et mettez à jour le profil.")
print("=" * 60)
