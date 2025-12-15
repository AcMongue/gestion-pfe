"""
Analyse complète des workflows et interactions entre rôles
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from users.models import User
from subjects.models import Subject, Application, Assignment
from projects.models import Project, Milestone, Deliverable
from defenses.models import Defense, JuryMember, DefenseChangeRequest
from communications.models import Message, Notification

print("=" * 80)
print("ANALYSE DES WORKFLOWS ET INTERACTIONS ENTRE RÔLES")
print("=" * 80)

# Définir les workflows attendus
workflows = {
    "1. PROPOSITION DE SUJET": {
        "Encadreur": "Crée un sujet (statut: draft)",
        "Actions attendues": [
            "→ Notification automatique à l'admin",
            "→ Admin valide/rejette",
            "→ Si validé: statut → published, notification à l'encadreur",
            "→ Si rejeté: notification à l'encadreur avec raison"
        ],
        "État actuel": "Manque système de validation admin"
    },
    
    "2. CANDIDATURE": {
        "Étudiant": "Candidate à un sujet",
        "Actions attendues": [
            "→ Notification automatique à l'encadreur",
            "→ Encadreur évalue (accepte/rejette/shortlist)",
            "→ Notification à l'étudiant du résultat",
            "→ Si accepté: visible dans interface admin pour affectation"
        ],
        "État actuel": "✓ Évaluation OK, ✗ Notifications manquantes"
    },
    
    "3. AFFECTATION": {
        "Admin": "Affecte un sujet à un étudiant",
        "Actions attendues": [
            "→ Création automatique du projet",
            "→ Notification à l'étudiant",
            "→ Notification à l'encadreur",
            "→ Sujet passe en statut 'assigned'",
            "→ Autres candidatures automatiquement rejetées avec notification"
        ],
        "État actuel": "✓ Affectation OK, ✗ Notifications manquantes, ✗ Création auto projet"
    },
    
    "4. SUIVI DU PROJET": {
        "Étudiant": "Ajoute jalons/livrables",
        "Actions attendues": [
            "→ Notification à l'encadreur",
            "→ Encadreur peut commenter/valider",
            "→ Notification à l'étudiant si commentaire"
        ],
        "État actuel": "✗ Système de notification absent"
    },
    
    "5. PLANIFICATION SOUTENANCE": {
        "Admin": "Planifie une soutenance",
        "Actions attendues": [
            "→ Notification à l'étudiant",
            "→ Notification à l'encadreur",
            "→ Notification aux membres du jury (quand ajoutés)",
            "→ Rappel automatique 1 semaine avant",
            "→ Rappel automatique 1 jour avant"
        ],
        "État actuel": "✗ Notifications manquantes, ✗ Rappels absents"
    },
    
    "6. MODIFICATION SOUTENANCE": {
        "Étudiant/Encadreur": "Suggère une modification",
        "Actions attendues": [
            "→ Notification immédiate à l'admin",
            "→ Admin examine et décide",
            "→ Notification au demandeur (approuvé/rejeté)",
            "→ Si approuvé: notifications à tous les concernés (étudiant, encadreur, jury)"
        ],
        "État actuel": "✓ Système créé, ✗ Notifications manquantes"
    },
    
    "7. ÉVALUATION": {
        "Jury": "Note la soutenance",
        "Actions attendues": [
            "→ Calcul automatique note finale",
            "→ Notification à l'étudiant",
            "→ Notification à l'encadreur",
            "→ Mise à jour statut projet → completed",
            "→ Archivage automatique"
        ],
        "État actuel": "✗ Notifications manquantes, ✗ Workflow d'archivage incomplet"
    },
    
    "8. COMMUNICATION": {
        "Tous": "Envoient des messages",
        "Actions attendues": [
            "→ Notification au destinataire",
            "→ Compteur de messages non lus",
            "→ Marquer comme lu automatiquement à l'ouverture"
        ],
        "État actuel": "✓ Messages OK, ✗ Notifications partielles"
    }
}

print("\n📋 ANALYSE DES 8 WORKFLOWS PRINCIPAUX\n")

for workflow_name, details in workflows.items():
    print(f"\n{workflow_name}")
    print("-" * 80)
    for key, value in details.items():
        if isinstance(value, list):
            print(f"  {key}:")
            for item in value:
                print(f"    {item}")
        else:
            print(f"  {key}: {value}")

# Vérifier l'état actuel
print("\n" + "=" * 80)
print("VÉRIFICATION DES DONNÉES ACTUELLES")
print("=" * 80)

# Vérifier notifications
notifications = Notification.objects.all()
print(f"\n📧 Notifications existantes: {notifications.count()}")
for notif in notifications[:5]:
    print(f"  - {notif.recipient.username}: {notif.type} - {notif.message[:50]}")

# Vérifier si les notifications sont créées lors des actions
print(f"\n📊 Statistiques:")
print(f"  - Sujets: {Subject.objects.count()}")
print(f"  - Candidatures: {Application.objects.count()}")
print(f"  - Affectations: {Assignment.objects.count()}")
print(f"  - Projets: {Project.objects.count()}")
print(f"  - Soutenances: {Defense.objects.count()}")
print(f"  - Messages: {Message.objects.count()}")
print(f"  - Notifications: {Notification.objects.count()}")

print("\n" + "=" * 80)
print("ACTIONS MANQUANTES CRITIQUES")
print("=" * 80)

actions_manquantes = [
    "1. Système de validation des sujets par l'admin",
    "2. Notifications automatiques lors des candidatures",
    "3. Notifications automatiques lors des affectations",
    "4. Création automatique du projet après affectation",
    "5. Notifications lors de l'ajout de jalons/livrables",
    "6. Notifications lors de la planification des soutenances",
    "7. Système de rappels automatiques",
    "8. Notifications lors des modifications de soutenance",
    "9. Workflow d'évaluation complet avec notifications",
    "10. Archivage automatique après soutenance",
    "11. Compteur de messages non lus",
    "12. Statut 'lu' pour les messages"
]

for action in actions_manquantes:
    print(f"  ❌ {action}")

print("\n" + "=" * 80)
print("RECOMMANDATIONS")
print("=" * 80)
print("""
Pour un workflow complet et cohérent:

1. SYSTÈME DE NOTIFICATIONS CENTRALISÉ
   - Créer une fonction utilitaire pour envoyer des notifications
   - Déclencher automatiquement lors des actions clés
   - Grouper par type et importance

2. SIGNAUX DJANGO
   - Utiliser post_save, post_delete pour déclencher actions automatiques
   - Exemple: post_save sur Assignment → créer Project + notifications

3. TÂCHES PLANIFIÉES (Celery/Cron)
   - Rappels automatiques avant soutenances
   - Nettoyage des notifications anciennes
   - Archivage automatique

4. PERMISSIONS ET VALIDATIONS
   - Admin valide les sujets avant publication
   - Workflow d'approbation pour modifications sensibles

5. TABLEAU DE BORD RÉACTIF
   - Compteurs temps réel
   - Alertes pour actions en attente
   - Indicateurs de progression
""")

print("=" * 80)
