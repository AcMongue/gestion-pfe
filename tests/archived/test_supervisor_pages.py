#!/usr/bin/env python
"""Test des URLs pour vérifier si les pages fonctionnent."""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.urls import reverse, NoReverseMatch
from django.contrib.auth import get_user_model

User = get_user_model()

print("=" * 80)
print("TEST DES URLs - ENCADREUR")
print("=" * 80)

# Test des URLs
urls_to_test = [
    ('projects:supervisor_students', {}, 'Mes étudiants'),
    ('subjects:supervisor_proposals', {}, 'Propositions reçues'),
    ('subjects:proposal_create', {}, 'Proposer un sujet (étudiant)'),
    ('subjects:my_proposals', {}, 'Mes propositions (étudiant)'),
]

print("\n1️⃣ Vérification des URLs...")
for url_name, kwargs, description in urls_to_test:
    try:
        url = reverse(url_name, kwargs=kwargs)
        print(f"   ✅ {description}: {url}")
    except NoReverseMatch as e:
        print(f"   ❌ {description}: ERREUR - {e}")

# Test avec un encadreur
print("\n2️⃣ Test avec un utilisateur encadreur...")
supervisor = User.objects.filter(role='supervisor').first()

if supervisor:
    print(f"   ✅ Encadreur trouvé: {supervisor.get_full_name()} ({supervisor.username})")
    
    # Vérifier permissions
    print(f"   ✅ is_supervisor(): {supervisor.is_supervisor()}")
    
    # Vérifier les projets
    from projects.models import Project
    from subjects.models import StudentProposal
    from django.db.models import Q
    
    projects = Project.objects.filter(assignment__subject__supervisor=supervisor)
    print(f"   📊 Projets encadrés: {projects.count()}")
    
    proposals = StudentProposal.objects.filter(
        Q(preferred_supervisor_1=supervisor) |
        Q(preferred_supervisor_2=supervisor) |
        Q(preferred_supervisor_3=supervisor)
    )
    print(f"   📊 Propositions reçues: {proposals.count()}")
else:
    print("   ⚠️  Aucun encadreur trouvé")

# Test des templates
print("\n3️⃣ Vérification des templates...")
import os
templates_to_check = [
    'templates/projects/supervisor_students.html',
    'templates/subjects/supervisor_proposals.html',
]

for template_path in templates_to_check:
    full_path = os.path.join(os.getcwd(), template_path)
    if os.path.exists(full_path):
        size = os.path.getsize(full_path)
        print(f"   ✅ {template_path} ({size} bytes)")
    else:
        print(f"   ❌ {template_path} INTROUVABLE")

print("\n" + "=" * 80)
print("TEST TERMINÉ")
print("=" * 80)
