"""
Test du système de notifications automatiques
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from users.models import User
from subjects.models import Subject, Application, Assignment
from projects.models import Project
from communications.models import Notification

print("=" * 80)
print("TEST DU SYSTÈME DE NOTIFICATIONS AUTOMATIQUES")
print("=" * 80)

# Test 1: Candidature
print("\n[TEST 1] Simulation d'une candidature")
print("-" * 80)

etudiant = User.objects.filter(role='student').first()
encadreur = User.objects.filter(role='supervisor').first()
sujet = Subject.objects.filter(supervisor=encadreur).first()

if etudiant and encadreur and sujet:
    # Compter les notifications avant
    notifs_avant = Notification.objects.filter(user=encadreur).count()
    
    # Créer une candidature
    app = Application.objects.create(
        subject=sujet,
        student=etudiant,
        motivation_letter="Test de notification automatique",
        status='pending'
    )
    
    # Vérifier les notifications après
    notifs_apres = Notification.objects.filter(user=encadreur).count()
    
    print(f"Étudiant: {etudiant.get_full_name()}")
    print(f"Encadreur: {encadreur.get_full_name()}")
    print(f"Sujet: {sujet.title}")
    print(f"Notifications avant: {notifs_avant}")
    print(f"Notifications après: {notifs_apres}")
    
    if notifs_apres > notifs_avant:
        print("✅ Notification créée automatiquement!")
        derniere_notif = Notification.objects.filter(user=encadreur).latest('created_at')
        print(f"   Titre: {derniere_notif.title}")
        print(f"   Message: {derniere_notif.message}")
    else:
        print("❌ Aucune notification créée")
    
    # Nettoyer
    app.delete()
else:
    print("❌ Données de test manquantes")

# Test 2: Acceptation de candidature
print("\n[TEST 2] Simulation d'acceptation de candidature")
print("-" * 80)

if etudiant and encadreur and sujet:
    # Créer une candidature
    app = Application.objects.create(
        subject=sujet,
        student=etudiant,
        motivation_letter="Test",
        status='pending'
    )
    
    # Compter notifications avant
    notifs_avant = Notification.objects.filter(user=etudiant).count()
    
    # Accepter la candidature
    app.status = 'accepted'
    app.reviewed_by = encadreur
    app.save()
    
    # Vérifier notifications après
    notifs_apres = Notification.objects.filter(user=etudiant).count()
    
    print(f"Notifications étudiant avant: {notifs_avant}")
    print(f"Notifications étudiant après: {notifs_apres}")
    
    if notifs_apres > notifs_avant:
        print("✅ Notification d'acceptation envoyée!")
        derniere_notif = Notification.objects.filter(user=etudiant).latest('created_at')
        print(f"   Titre: {derniere_notif.title}")
        print(f"   Message: {derniere_notif.message}")
    else:
        print("❌ Aucune notification créée")
    
    # Nettoyer
    app.delete()

# Test 3: Affectation
print("\n[TEST 3] Simulation d'affectation")
print("-" * 80)

if etudiant and sujet:
    # Nettoyer les affectations existantes pour cet étudiant
    Assignment.objects.filter(student=etudiant).delete()
    
    # Compter les éléments avant
    notifs_etudiant_avant = Notification.objects.filter(user=etudiant).count()
    notifs_encadreur_avant = Notification.objects.filter(user=encadreur).count()
    projets_avant = Project.objects.filter(assignment__student=etudiant).count()
    
    # Créer une affectation
    assignment = Assignment.objects.create(
        student=etudiant,
        subject=sujet,
        assigned_by=User.objects.filter(role='admin').first(),
        status='active'
    )
    
    # Vérifier après
    notifs_etudiant_apres = Notification.objects.filter(user=etudiant).count()
    notifs_encadreur_apres = Notification.objects.filter(user=encadreur).count()
    projets_apres = Project.objects.filter(assignment__student=etudiant).count()
    
    print(f"Notifications étudiant: {notifs_etudiant_avant} → {notifs_etudiant_apres}")
    print(f"Notifications encadreur: {notifs_encadreur_avant} → {notifs_encadreur_apres}")
    print(f"Projets: {projets_avant} → {projets_apres}")
    
    if notifs_etudiant_apres > notifs_etudiant_avant:
        print("✅ Notification à l'étudiant créée!")
    if notifs_encadreur_apres > notifs_encadreur_avant:
        print("✅ Notification à l'encadreur créée!")
    if projets_apres > projets_avant:
        print("✅ Projet créé automatiquement!")
        projet = Project.objects.filter(assignment=assignment).first()
        print(f"   Titre: {projet.title}")
    
    # Nettoyer
    if projets_apres > projets_avant:
        Project.objects.filter(assignment=assignment).delete()
    assignment.delete()

print("\n" + "=" * 80)
print("RÉSUMÉ DES NOTIFICATIONS ACTUELLES")
print("=" * 80)

total_notifs = Notification.objects.count()
print(f"\n📧 Total notifications: {total_notifs}")

types = Notification.objects.values('type').distinct()
print(f"\n📊 Par type:")
for t in types:
    count = Notification.objects.filter(type=t['type']).count()
    print(f"  - {t['type']}: {count}")

print("\n" + "=" * 80)
