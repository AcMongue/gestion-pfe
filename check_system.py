#!/usr/bin/env python
"""Script de vérification complète du système."""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Count
from subjects.models import Subject, Application, Assignment

User = get_user_model()

print("=" * 70)
print("🔍 VÉRIFICATION COMPLÈTE DU SYSTÈME DE GESTION PFE")
print("=" * 70)

# 1. Vérifier les utilisateurs
print("\n👥 UTILISATEURS")
print("-" * 70)
total_users = User.objects.count()
students = User.objects.filter(role='student').count()
supervisors = User.objects.filter(role='supervisor').count()
admins = User.objects.filter(role='admin').count()
jury = User.objects.filter(role='jury').count()

print(f"Total utilisateurs: {total_users}")
print(f"  - Étudiants: {students}")
print(f"  - Encadreurs: {supervisors}")
print(f"  - Administrateurs: {admins}")
print(f"  - Membres du jury: {jury}")

# Vérifier les étudiants sans niveau
students_without_level = User.objects.filter(role='student', level__isnull=True).count()
if students_without_level > 0:
    print(f"  ⚠️  {students_without_level} étudiant(s) sans niveau défini")
else:
    print(f"  ✅ Tous les étudiants ont un niveau défini")

# 2. Vérifier les sujets
print("\n📚 SUJETS")
print("-" * 70)
total_subjects = Subject.objects.count()
published = Subject.objects.filter(status='published').count()
draft = Subject.objects.filter(status='draft').count()
assigned = Subject.objects.filter(status='assigned').count()
archived = Subject.objects.filter(status='archived').count()

print(f"Total sujets: {total_subjects}")
print(f"  - Publiés: {published}")
print(f"  - Brouillons: {draft}")
print(f"  - Attribués: {assigned}")
print(f"  - Archivés: {archived}")

# Par niveau
l3_subjects = Subject.objects.filter(status='published', level='L3').count()
m2_subjects = Subject.objects.filter(status='published', level='M2').count()
doc_subjects = Subject.objects.filter(status='published', level='DOC').count()
print(f"\nSujets publiés par niveau:")
print(f"  - L3: {l3_subjects}")
print(f"  - M2: {m2_subjects}")
print(f"  - Doctorat: {doc_subjects}")

# 3. Vérifier les candidatures
print("\n📋 CANDIDATURES")
print("-" * 70)
total_applications = Application.objects.count()
pending = Application.objects.filter(status='pending').count()
accepted = Application.objects.filter(status='accepted').count()
rejected = Application.objects.filter(status='rejected').count()
withdrawn = Application.objects.filter(status='withdrawn').count()

print(f"Total candidatures: {total_applications}")
print(f"  - En attente: {pending}")
print(f"  - Acceptées: {accepted}")
print(f"  - Rejetées: {rejected}")
print(f"  - Retirées: {withdrawn}")

# 4. Vérifier les affectations
print("\n📌 AFFECTATIONS")
print("-" * 70)
total_assignments = Assignment.objects.count()
active = Assignment.objects.filter(status='active').count()
completed = Assignment.objects.filter(status='completed').count()
cancelled = Assignment.objects.filter(status='cancelled').count()

print(f"Total affectations: {total_assignments}")
print(f"  - Actives: {active}")
print(f"  - Terminées: {completed}")
print(f"  - Annulées: {cancelled}")

# 5. Statistiques avancées
print("\n📊 STATISTIQUES")
print("-" * 70)

# Sujets les plus populaires
popular_subjects = Subject.objects.filter(status='published').annotate(
    app_count=Count('applications')
).order_by('-app_count')[:5]

if popular_subjects:
    print("Top 5 sujets les plus demandés:")
    for i, subject in enumerate(popular_subjects, 1):
        print(f"  {i}. {subject.title} - {subject.app_count} candidature(s)")
else:
    print("Aucun sujet avec candidatures")

# 6. Vérifier l'intégrité
print("\n✅ VÉRIFICATIONS D'INTÉGRITÉ")
print("-" * 70)

issues = []

# Vérifier les candidatures orphelines
orphan_apps = Application.objects.filter(subject__isnull=True).count()
if orphan_apps > 0:
    issues.append(f"❌ {orphan_apps} candidature(s) sans sujet")
else:
    print("✅ Pas de candidatures orphelines")

# Vérifier les affectations sans sujet
orphan_assignments = Assignment.objects.filter(subject__isnull=True).count()
if orphan_assignments > 0:
    issues.append(f"❌ {orphan_assignments} affectation(s) sans sujet")
else:
    print("✅ Pas d'affectations orphelines")

# Vérifier les doublons de candidatures
duplicates = Application.objects.values('student', 'subject').annotate(
    count=Count('id')
).filter(count__gt=1).count()
if duplicates > 0:
    issues.append(f"❌ {duplicates} candidature(s) en double")
else:
    print("✅ Pas de candidatures en double")

# Vérifier les étudiants avec plusieurs affectations actives
students_multi_assignments = User.objects.filter(
    role='student',
    assignment__status='active'
).annotate(
    count=Count('assignment')
).filter(count__gt=1).count()
if students_multi_assignments > 0:
    issues.append(f"⚠️  {students_multi_assignments} étudiant(s) avec plusieurs affectations actives")
else:
    print("✅ Pas d'étudiants avec plusieurs affectations actives")

if issues:
    print("\n⚠️  PROBLÈMES DÉTECTÉS:")
    for issue in issues:
        print(f"  {issue}")
else:
    print("\n🎉 Aucun problème d'intégrité détecté!")

# 7. État des fonctionnalités
print("\n🎯 ÉTAT DES FONCTIONNALITÉS")
print("-" * 70)
print("✅ Fonctionnalité 1: Gestion des utilisateurs et authentification - COMPLÈTE")
print("✅ Fonctionnalité 2: Catalogue et affectation des sujets - COMPLÈTE")
print("🚧 Fonctionnalité 3: Suivi collaboratif des projets - EN DÉVELOPPEMENT")
print("🚧 Fonctionnalité 4: Communication contextualisée - EN DÉVELOPPEMENT")
print("🚧 Fonctionnalité 5: Planification automatisée des soutenances - EN DÉVELOPPEMENT")
print("🚧 Fonctionnalité 6: Archivage et reporting - EN DÉVELOPPEMENT")

print("\n" + "=" * 70)
print("✅ VÉRIFICATION TERMINÉE")
print("=" * 70)
print("\n💡 Serveur accessible sur: http://127.0.0.1:8000/")
print("💡 Admin accessible sur: http://127.0.0.1:8000/admin/")
print("💡 Compte admin: admin / admin123")
print("\n")
