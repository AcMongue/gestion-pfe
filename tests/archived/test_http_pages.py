#!/usr/bin/env python
"""Test HTTP direct des pages encadreur."""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model

User = get_user_model()

print("=" * 80)
print("TEST HTTP DES PAGES ENCADREUR")
print("=" * 80)

# Créer un client
client = Client()

# Récupérer un encadreur
supervisor = User.objects.filter(role='supervisor').first()

if not supervisor:
    print("❌ Aucun encadreur trouvé. Créons-en un.")
    supervisor = User.objects.create_user(
        username='test_supervisor',
        email='supervisor@test.com',
        password='test123',
        role='supervisor',
        first_name='Test',
        last_name='Supervisor',
        grade='Professeur'
    )
    print(f"✅ Encadreur créé: {supervisor.username}")

# Se connecter
logged_in = client.login(username=supervisor.username, password='test123')
print(f"\n1️⃣ Connexion: {'✅ OK' if logged_in else '❌ ÉCHEC'}")

if not logged_in:
    # Essayer avec un password connu
    supervisor.set_password('test123')
    supervisor.save()
    logged_in = client.login(username=supervisor.username, password='test123')
    print(f"   Retry: {'✅ OK' if logged_in else '❌ ÉCHEC'}")

if logged_in:
    # Test page "Mes Étudiants"
    print("\n2️⃣ Test: /projects/supervisor/students/")
    try:
        response = client.get('/projects/supervisor/students/')
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            print(f"   ✅ Page chargée")
            print(f"   Template: {response.template_name if hasattr(response, 'template_name') else 'N/A'}")
            
            # Vérifier le contexte
            if hasattr(response, 'context'):
                ctx = response.context
                print(f"   Context variables:")
                print(f"      - students_count: {ctx.get('students_count', 'N/A')}")
                print(f"      - projects: {len(ctx.get('projects', []))}")
        elif response.status_code == 302:
            print(f"   ⚠️  Redirection vers: {response.url}")
        else:
            print(f"   ❌ Erreur {response.status_code}")
            if hasattr(response, 'content'):
                content = response.content.decode('utf-8')[:500]
                print(f"   Content: {content}")
    except Exception as e:
        print(f"   ❌ Exception: {e}")
        import traceback
        traceback.print_exc()
    
    # Test page "Propositions reçues"
    print("\n3️⃣ Test: /subjects/proposals/")
    try:
        response = client.get('/subjects/proposals/')
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            print(f"   ✅ Page chargée")
            
            # Vérifier le contexte
            if hasattr(response, 'context'):
                ctx = response.context
                print(f"   Context variables:")
                print(f"      - proposals: {len(ctx.get('proposals', []))}")
                print(f"      - status_filter: {ctx.get('status_filter', 'N/A')}")
                print(f"      - total_count: {ctx.get('total_count', 'N/A')}")
        elif response.status_code == 302:
            print(f"   ⚠️  Redirection vers: {response.url}")
        else:
            print(f"   ❌ Erreur {response.status_code}")
    except Exception as e:
        print(f"   ❌ Exception: {e}")
        import traceback
        traceback.print_exc()

print("\n" + "=" * 80)
print("TEST TERMINÉ")
print("=" * 80)
