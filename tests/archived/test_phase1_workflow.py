#!/usr/bin/env python
"""
Script de test rapide pour vérifier le workflow des propositions étudiantes - Phase 1
"""
import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from subjects.models import StudentProposal, Subject, Assignment
from projects.models import Project, Meeting

User = get_user_model()

print("=" * 80)
print("TEST RAPIDE - WORKFLOW PHASE 1")
print("=" * 80)

# 1. Vérifier les modèles
print("\n1️⃣ Vérification des modèles...")
try:
    # StudentProposal
    proposal_fields = [f.name for f in StudentProposal._meta.get_fields()]
    assert 'title' in proposal_fields
    assert 'preferred_supervisor_1' in proposal_fields
    assert 'status' in proposal_fields
    print("   ✅ StudentProposal: OK")
    
    # Meeting
    meeting_fields = [f.name for f in Meeting._meta.get_fields()]
    assert 'type' in meeting_fields
    assert 'minutes' in meeting_fields
    assert 'decisions_made' in meeting_fields
    print("   ✅ Meeting: OK")
    
    # Project status
    status_choices = dict(Project.STATUS_CHOICES)
    assert 'awaiting_kickoff' in status_choices
    print("   ✅ Project.STATUS_CHOICES: OK (awaiting_kickoff présent)")
    
except Exception as e:
    print(f"   ❌ Erreur: {e}")
    sys.exit(1)

# 2. Vérifier les utilisateurs de test
print("\n2️⃣ Vérification des utilisateurs de test...")
try:
    student = User.objects.filter(role='student').first()
    supervisor = User.objects.filter(role='supervisor').first()
    
    if not student:
        print("   ⚠️  Aucun étudiant trouvé - créons-en un")
        student = User.objects.create_user(
            username='etudiant_test',
            email='etudiant@test.com',
            password='test123',
            role='student',
            first_name='Test',
            last_name='Étudiant',
            level='Master 2',
            filiere='Informatique'
        )
        print(f"   ✅ Étudiant créé: {student.get_full_name()}")
    else:
        print(f"   ✅ Étudiant trouvé: {student.get_full_name()}")
    
    if not supervisor:
        print("   ⚠️  Aucun encadreur trouvé - créons-en un")
        supervisor = User.objects.create_user(
            username='encadreur_test',
            email='encadreur@test.com',
            password='test123',
            role='supervisor',
            first_name='Test',
            last_name='Encadreur',
            grade='Professeur',
            specialite='Intelligence Artificielle'
        )
        print(f"   ✅ Encadreur créé: {supervisor.get_full_name()}")
    else:
        print(f"   ✅ Encadreur trouvé: {supervisor.get_full_name()}")
        
except Exception as e:
    print(f"   ❌ Erreur: {e}")
    sys.exit(1)

# 3. Tester la création d'une proposition
print("\n3️⃣ Test de création de proposition...")
try:
    # Vérifier si l'étudiant a déjà une affectation
    existing_assignment = Assignment.objects.filter(student=student).first()
    if existing_assignment:
        print(f"   ⚠️  L'étudiant a déjà une affectation: {existing_assignment.subject.title}")
        print("   ℹ️  Un étudiant avec affectation ne devrait pas pouvoir proposer")
    else:
        # Créer une proposition
        proposal = StudentProposal.objects.create(
            student=student,
            title="Système de gestion des projets PFE avec IA",
            description="Un système intelligent pour gérer les projets de fin d'études en utilisant l'IA pour la planification automatique.",
            objectives="- Automatiser la planification\n- Optimiser les affectations\n- Suivre les progressions",
            methodology="Développement agile avec sprints de 2 semaines",
            technologies="Django, React, TensorFlow",
            domain='software_engineering',
            type='development',
            preferred_supervisor_1=supervisor,
            supervisor_justification="Expert en IA et gestion de projets",
            status='pending'
        )
        print(f"   ✅ Proposition créée: {proposal.title}")
        print(f"   ✅ Statut: {proposal.get_status_display()}")
        print(f"   ✅ Encadreur préféré: {proposal.preferred_supervisor_1.get_full_name()}")
        
        # Test de la méthode can_be_accepted_by
        can_accept = proposal.can_be_accepted_by(supervisor)
        print(f"   ✅ L'encadreur peut accepter: {can_accept}")
        
except Exception as e:
    print(f"   ❌ Erreur: {e}")
    import traceback
    traceback.print_exc()

# 4. Statistiques
print("\n4️⃣ Statistiques globales...")
try:
    total_proposals = StudentProposal.objects.count()
    pending_proposals = StudentProposal.objects.filter(status='pending').count()
    accepted_proposals = StudentProposal.objects.filter(status='accepted').count()
    
    total_meetings = Meeting.objects.count()
    kickoff_meetings = Meeting.objects.filter(type='kickoff').count()
    
    awaiting_kickoff_projects = Project.objects.filter(status='awaiting_kickoff').count()
    in_progress_projects = Project.objects.filter(status='in_progress').count()
    
    print(f"   📊 Propositions étudiantes:")
    print(f"      - Total: {total_proposals}")
    print(f"      - En attente: {pending_proposals}")
    print(f"      - Acceptées: {accepted_proposals}")
    
    print(f"   📊 Réunions:")
    print(f"      - Total: {total_meetings}")
    print(f"      - Réunions de cadrage: {kickoff_meetings}")
    
    print(f"   📊 Projets:")
    print(f"      - En attente de cadrage: {awaiting_kickoff_projects}")
    print(f"      - En cours: {in_progress_projects}")
    
except Exception as e:
    print(f"   ❌ Erreur: {e}")

# 5. Vérifier les vues
print("\n5️⃣ Vérification des URLs...")
try:
    from django.urls import reverse
    
    urls_to_test = [
        ('subjects:proposal_create', {}),
        ('subjects:my_proposals', {}),
        ('subjects:supervisor_proposals', {}),
    ]
    
    for url_name, kwargs in urls_to_test:
        try:
            url = reverse(url_name, kwargs=kwargs)
            print(f"   ✅ {url_name}: {url}")
        except Exception as e:
            print(f"   ❌ {url_name}: {e}")
            
except Exception as e:
    print(f"   ❌ Erreur: {e}")

print("\n" + "=" * 80)
print("✅ TESTS TERMINÉS")
print("=" * 80)
print("\n💡 Prochaines étapes:")
print("   1. Démarrer le serveur: python manage.py runserver")
print("   2. Se connecter en tant qu'étudiant")
print("   3. Tester: Proposer un sujet → Choisir encadreurs → Soumettre")
print("   4. Se connecter en tant qu'encadreur")
print("   5. Tester: Voir propositions → Accepter/Refuser → Organiser cadrage")
print("\n")
