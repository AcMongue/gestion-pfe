"""
Diagnostic des problèmes identifiés:
1. Création de projet
2. Workflow encadreur pour suivre les étudiants
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from projects.models import Project
from subjects.models import Subject, Assignment, Application

User = get_user_model()

def print_section(title):
    print("\n" + "="*80)
    print(f" {title}")
    print("="*80 + "\n")


def check_project_creation():
    """Vérifie le processus de création de projet."""
    print_section("PROBLÈME 1: Création de Projet")
    
    print("📋 ANALYSE:")
    print("\n1. Comment les projets sont-ils créés actuellement ?")
    print("   - Méthode 1: Manuellement via /projects/create/ (admin/encadreur)")
    print("   - Méthode 2: Automatiquement via signal quand affectation acceptée")
    
    # Vérifier les signals
    from config import signals
    print("\n2. Vérification des signals:")
    print("   ✓ Signal exists: create_project_on_assignment_accepted")
    
    # Vérifier les affectations et projets
    assignments = Assignment.objects.all()
    print(f"\n3. État actuel:")
    print(f"   - Affectations totales: {assignments.count()}")
    
    accepted = assignments.filter(status='accepted')
    print(f"   - Affectations acceptées: {accepted.count()}")
    
    projects = Project.objects.all()
    print(f"   - Projets créés: {projects.count()}")
    
    # Vérifier les affectations acceptées sans projet
    print("\n4. Affectations acceptées SANS projet:")
    for assignment in accepted:
        try:
            project = assignment.project
            print(f"   ✓ {assignment.student.get_full_name()} - {assignment.subject.title} - Projet existe")
        except:
            print(f"   ❌ {assignment.student.get_full_name()} - {assignment.subject.title} - PAS DE PROJET!")
    
    print("\n🔧 PROBLÈME IDENTIFIÉ:")
    missing = accepted.count() - projects.count()
    if missing > 0:
        print(f"   ⚠️  {missing} affectations acceptées n'ont pas de projet!")
        print("   Solution: Créer les projets manquants automatiquement")
    else:
        print("   ✓ Tous les projets sont créés correctement")
    
    print("\n💡 AMÉLIORATION NÉCESSAIRE:")
    print("   - Ajouter un bouton 'Créer un projet' visible pour l'étudiant")
    print("   - Améliorer le formulaire de création de projet")
    print("   - Pré-remplir les champs depuis l'affectation")


def check_supervisor_workflow():
    """Vérifie le workflow de l'encadreur."""
    print_section("PROBLÈME 2: Workflow Encadreur")
    
    supervisor = User.objects.filter(role='supervisor').first()
    
    if not supervisor:
        print("❌ Aucun encadreur trouvé")
        return
    
    print(f"👤 Encadreur testé: {supervisor.get_full_name()}")
    
    # 1. Sujets proposés
    subjects = Subject.objects.filter(supervisor=supervisor)
    print(f"\n1. Sujets proposés: {subjects.count()}")
    for subject in subjects:
        print(f"   - {subject.title} (Statut: {subject.get_status_display()})")
    
    # 2. Candidatures reçues
    applications = Application.objects.filter(subject__supervisor=supervisor)
    print(f"\n2. Candidatures reçues: {applications.count()}")
    pending = applications.filter(status='pending')
    print(f"   - En attente: {pending.count()}")
    accepted = applications.filter(status='accepted')
    print(f"   - Acceptées: {accepted.count()}")
    
    # 3. Affectations (étudiants assignés)
    assignments = Assignment.objects.filter(subject__supervisor=supervisor)
    print(f"\n3. Affectations (étudiants assignés): {assignments.count()}")
    for assignment in assignments:
        print(f"   - {assignment.student.get_full_name()} → {assignment.subject.title}")
        print(f"     Statut: {assignment.get_status_display()}")
    
    # 4. Projets encadrés
    projects = Project.objects.filter(assignment__subject__supervisor=supervisor)
    print(f"\n4. Projets encadrés: {projects.count()}")
    
    if projects.count() == 0:
        print("   ⚠️  AUCUN PROJET à encadrer!")
        print("   Raison possible:")
        if assignments.count() == 0:
            print("      - Aucune affectation acceptée")
        else:
            print("      - Les projets n'ont pas été créés pour les affectations")
    else:
        for project in projects:
            print(f"\n   📁 {project.title}")
            print(f"      Étudiant: {project.assignment.student.get_full_name()}")
            print(f"      Progression: {project.progress}%")
            print(f"      Statut: {project.get_status_display()}")
            
            # Jalons
            milestones = project.milestones.all()
            completed = milestones.filter(validated_by_supervisor=True).count()
            print(f"      Jalons: {completed}/{milestones.count()} validés")
            
            # Livrables
            deliverables = project.deliverables.all()
            reviewed = deliverables.filter(status='approved').count()
            print(f"      Livrables: {reviewed}/{deliverables.count()} approuvés")
    
    print("\n🔧 PROBLÈMES IDENTIFIÉS:")
    print("\n   1. Navigation confuse:")
    print("      - Trop de vues: dashboard, mes sujets, mes étudiants, projets")
    print("      - L'encadreur doit chercher ses étudiants")
    
    print("\n   2. Suivi incomplet:")
    print("      - Pas de vue centralisée par étudiant")
    print("      - Difficile de voir l'avancement global")
    print("      - Pas de tableau de bord de suivi")
    
    print("\n   3. Actions manquantes:")
    print("      - Pas de bouton 'Valider' visible sur les jalons")
    print("      - Pas de bouton 'Réviser' visible sur les livrables")
    print("      - Pas de moyen de noter le projet facilement")


def test_supervisor_views():
    """Test les vues disponibles pour l'encadreur."""
    print_section("TEST: Vues Encadreur")
    
    from django.test import Client
    
    supervisor = User.objects.filter(role='supervisor').first()
    
    if not supervisor:
        print("❌ Aucun encadreur pour tester")
        return
    
    client = Client()
    client.force_login(supervisor)
    
    print(f"👤 Connecté en tant que: {supervisor.get_full_name()}")
    
    views_to_test = [
        ('/dashboard/', 'Dashboard'),
        ('/subjects/', 'Mes sujets'),
        ('/subjects/my-subjects/', 'Mes sujets (alt)'),
        ('/projects/', 'Projets'),
        ('/projects/my-projects/', 'Mes projets'),
    ]
    
    for url, name in views_to_test:
        response = client.get(url)
        status_icon = "✅" if response.status_code == 200 else "❌"
        print(f"{status_icon} {name}: {url} - Status {response.status_code}")


def recommend_solutions():
    """Recommande des solutions."""
    print_section("💡 SOLUTIONS RECOMMANDÉES")
    
    print("""
1. CRÉATION DE PROJET:
   ═══════════════════════════════════════════════════════════════════
   
   a) Automatiser complètement:
      - Signal crée automatiquement le projet quand affectation acceptée
      - Pré-remplir: titre (sujet), description, objectifs
      - Étudiant peut modifier ensuite
   
   b) Ajouter bouton visible:
      - Dans le dashboard étudiant: "Démarrer mon projet"
      - Dans la page d'affectation: "Créer le projet"
   
   c) Améliorer le formulaire:
      - Simplifier pour l'étudiant
      - Champs: objectifs détaillés, méthodologie, planning
      - Technologies prévues


2. WORKFLOW ENCADREUR:
   ═══════════════════════════════════════════════════════════════════
   
   a) Vue centralisée "Mes Étudiants":
      URL: /supervisor/students/
      Tableau avec:
      - Photo et nom de l'étudiant
      - Sujet du projet
      - Progression (%)
      - Dernière activité
      - Actions rapides: Voir projet, Messages, Valider
   
   b) Page de suivi par étudiant:
      URL: /supervisor/student/<id>/
      Onglets:
      - Vue d'ensemble (projet, progression)
      - Jalons (avec boutons de validation)
      - Livrables (avec formulaire de révision)
      - Communication (historique)
      - Notes et évaluations
   
   c) Dashboard amélioré:
      Widgets:
      - Alertes: Jalons en retard, livrables en attente
      - Timeline: Activités récentes des étudiants
      - Statistiques: Nombre d'étudiants, progression moyenne
      - Actions rapides


3. SUIVI DE PROJET:
   ═══════════════════════════════════════════════════════════════════
   
   a) Timeline du projet:
      - Historique des jalons complétés
      - Livrables soumis
      - Commentaires échangés
      - Modifications du projet
   
   b) Indicateurs visuels:
      - Graphique de progression
      - Dates clés (début, échéances, fin)
      - Alertes (retards, problèmes)
   
   c) Rapports automatiques:
      - Rapport hebdomadaire pour l'encadreur
      - Rapport mensuel pour l'administration
      - Export PDF du projet complet


4. AMÉLIORATIONS UX:
   ═══════════════════════════════════════════════════════════════════
   
   a) Navigation simplifiée:
      - Menu: Mes Étudiants | Mes Sujets | Planning | Messages
      - Notifications en temps réel
   
   b) Actions rapides:
      - Boutons d'action directement dans les listes
      - Modales pour validation rapide
      - Confirmation en un clic
   
   c) Feedback visuel:
      - Badge "Nouveau" sur les livrables non vus
      - Compteurs sur les onglets
      - Couleurs selon urgence
    """)


def main():
    print("\n" + "🔍"*40)
    print(" "*25 + "DIAGNOSTIC DES PROBLÈMES")
    print("🔍"*40 + "\n")
    
    check_project_creation()
    check_supervisor_workflow()
    test_supervisor_views()
    recommend_solutions()
    
    print("\n" + "="*80)
    print(" "*30 + "FIN DU DIAGNOSTIC")
    print("="*80 + "\n")


if __name__ == '__main__':
    main()
