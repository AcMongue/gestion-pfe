#!/usr/bin/env python
"""Script pour définir automatiquement le niveau L3 à tous les étudiants."""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from users.models import User

# Mettre à jour tous les étudiants sans niveau pour leur donner L3 par défaut
updated = User.objects.filter(role='student', level__isnull=True).update(level='L3')

print(f"✅ {updated} étudiant(s) mis à jour avec le niveau L3")

# Afficher le résumé
students = User.objects.filter(role='student')
print(f"\n📊 Résumé des étudiants:")
for student in students:
    print(f"  - {student.username}: {student.get_level_display() if student.level else 'Aucun niveau'}")
