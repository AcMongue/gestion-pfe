#!/usr/bin/env python
"""Créer un utilisateur encadreur de test avec mot de passe connu."""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

print("Création d'un encadreur de test...")

# Supprimer s'il existe déjà
User.objects.filter(username='supervisor_demo').delete()

# Créer
supervisor = User.objects.create_user(
    username='supervisor_demo',
    email='supervisor@demo.com',
    password='demo123',
    role='supervisor',
    first_name='Demo',
    last_name='Supervisor',
    grade='Professeur',
    specialite='Intelligence Artificielle'
)

print(f"✅ Encadreur créé avec succès!")
print(f"   Username: supervisor_demo")
print(f"   Password: demo123")
print(f"   URL connexion: http://127.0.0.1:8000/users/login/")
print(f"\nPages à tester:")
print(f"   - Mes étudiants: http://127.0.0.1:8000/projects/supervisor/students/")
print(f"   - Propositions reçues: http://127.0.0.1:8000/subjects/proposals/")
