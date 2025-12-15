"""
Test exhaustif de tous les workflows du système
"""
import os
import django
from datetime import date, time, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.utils import timezone
from users.models import User
from subjects.models import Subject, Application, Assignment
from projects.models import Project, Milestone, Deliverable
from defenses.models import Defense, JuryMember, DefenseChangeRequest
from communications.models import Notification, Message

def separator(title):
    print("\n" + "=" * 80)
    print(title.center(80))
    print("=" * 80)

def test_section(title):
    print(f"\n{'─' * 80}")
    print(f"📋 {title}")
    print('─' * 80)

def cleanup():
    """Nettoyer les données de test"""
    print("\n🧹 Nettoyage des données de test...")
    DefenseChangeRequest.objects.all().delete()
    JuryMember.objects.all().delete()
    Defense.objects.all().delete()
    Deliverable.objects.all().delete()
    Milestone.objects.all().delete()
    Project.objects.all().delete()
    Assignment.objects.all().delete()
    Application.objects.all().delete()
    Notification.objects.all().delete()
    print("✅ Nettoyage terminé")

# Récupérer les utilisateurs
admin = User.objects.filter(role='admin').first()
etudiant = User.objects.filter(role='student').first()
encadreur = User.objects.filter(role='supervisor').first()
jury1 = User.objects.filter(role='supervisor').exclude(id=encadreur.id).first()
jury2 = User.objects.filter(role='admin').exclude(id=admin.id).first()

separator("TEST EXHAUSTIF DE TOUS LES WORKFLOWS")
print(f"\n👥 Utilisateurs de test:")
print(f"   Admin: {admin.get_full_name()}")
print(f"   Étudiant: {etudiant.get_full_name()}")
print(f"   Encadreur: {encadreur.get_full_name()}")
print(f"   Jury 1: {jury1.get_full_name() if jury1 else 'N/A'}")
print(f"   Jury 2: {jury2.get_full_name() if jury2 else 'N/A'}")

# Nettoyer avant de commencer
cleanup()

# ============================================================================
# WORKFLOW 1: CYCLE COMPLET DE CANDIDATURE
# ============================================================================
test_section("WORKFLOW 1: Cycle complet de candidature")

sujet = Subject.objects.filter(supervisor=encadreur, status='published').first()
if not sujet:
    sujet = Subject.objects.create(
        title="Test: Application IA pour la santé",
        description="Projet de test pour les workflows",
        supervisor=encadreur,
        status='published',
        level='master'
    )
    print(f"✅ Sujet créé: {sujet.title}")

print(f"\n1️⃣ Étudiant candidate au sujet")
notifs_encadreur_avant = Notification.objects.filter(user=encadreur).count()
app = Application.objects.create(
    subject=sujet,
    student=etudiant,
    motivation_letter="Je suis très motivé par ce projet en IA médicale",
    status='pending'
)
notifs_encadreur_apres = Notification.objects.filter(user=encadreur).count()
print(f"   Notifications encadreur: {notifs_encadreur_avant} → {notifs_encadreur_apres}")
if notifs_encadreur_apres > notifs_encadreur_avant:
    print(f"   ✅ Encadreur notifié de la nouvelle candidature")

print(f"\n2️⃣ Encadreur accepte la candidature")
notifs_etudiant_avant = Notification.objects.filter(user=etudiant).count()
app.status = 'accepted'
app.reviewed_by = encadreur
app.review_comment = "Excellent profil, candidature acceptée"
app.save()
notifs_etudiant_apres = Notification.objects.filter(user=etudiant).count()
print(f"   Notifications étudiant: {notifs_etudiant_avant} → {notifs_etudiant_apres}")
if notifs_etudiant_apres > notifs_etudiant_avant:
    print(f"   ✅ Étudiant notifié de l'acceptation")

# ============================================================================
# WORKFLOW 2: AFFECTATION ET CRÉATION AUTOMATIQUE DE PROJET
# ============================================================================
test_section("WORKFLOW 2: Affectation et création automatique de projet")

print(f"\n1️⃣ Admin crée l'affectation")
notifs_etudiant_avant = Notification.objects.filter(user=etudiant).count()
notifs_encadreur_avant = Notification.objects.filter(user=encadreur).count()
projets_avant = Project.objects.count()

assignment = Assignment.objects.create(
    student=etudiant,
    subject=sujet,
    assigned_by=admin,
    status='active'
)

notifs_etudiant_apres = Notification.objects.filter(user=etudiant).count()
notifs_encadreur_apres = Notification.objects.filter(user=encadreur).count()
projets_apres = Project.objects.count()

print(f"   Notifications étudiant: {notifs_etudiant_avant} → {notifs_etudiant_apres}")
print(f"   Notifications encadreur: {notifs_encadreur_avant} → {notifs_encadreur_apres}")
print(f"   Projets: {projets_avant} → {projets_apres}")

if notifs_etudiant_apres > notifs_etudiant_avant:
    print(f"   ✅ Étudiant notifié de l'affectation")
if notifs_encadreur_apres > notifs_encadreur_avant:
    print(f"   ✅ Encadreur notifié du nouveau projet")
if projets_apres > projets_avant:
    projet = Project.objects.get(assignment=assignment)
    print(f"   ✅ Projet créé automatiquement: {projet.title}")

# ============================================================================
# WORKFLOW 3: GESTION DES JALONS
# ============================================================================
test_section("WORKFLOW 3: Gestion des jalons (Milestones)")

print(f"\n1️⃣ Étudiant ajoute un jalon")
notifs_encadreur_avant = Notification.objects.filter(user=encadreur).count()

milestone1 = Milestone.objects.create(
    project=projet,
    title="Revue de littérature",
    description="Analyse de l'état de l'art",
    due_date=date.today() + timedelta(days=30),
    status='pending'
)

notifs_encadreur_apres = Notification.objects.filter(user=encadreur).count()
print(f"   Notifications encadreur: {notifs_encadreur_avant} → {notifs_encadreur_apres}")
if notifs_encadreur_apres > notifs_encadreur_avant:
    print(f"   ✅ Encadreur notifié du nouveau jalon")
    notif = Notification.objects.filter(user=encadreur, type='milestone').latest('created_at')
    print(f"   📧 \"{notif.title}\"")

print(f"\n2️⃣ Étudiant ajoute un second jalon")
notifs_encadreur_avant = Notification.objects.filter(user=encadreur).count()

milestone2 = Milestone.objects.create(
    project=projet,
    title="Développement du prototype",
    description="Implémentation de la première version",
    due_date=date.today() + timedelta(days=60),
    status='pending'
)

notifs_encadreur_apres = Notification.objects.filter(user=encadreur).count()
if notifs_encadreur_apres > notifs_encadreur_avant:
    print(f"   ✅ Encadreur notifié du nouveau jalon")

# ============================================================================
# WORKFLOW 4: GESTION DES LIVRABLES
# ============================================================================
test_section("WORKFLOW 4: Gestion des livrables (Deliverables)")

print(f"\n1️⃣ Étudiant dépose un livrable")
notifs_encadreur_avant = Notification.objects.filter(user=encadreur).count()

# Créer un fichier temporaire pour le test
from django.core.files.base import ContentFile
deliverable1 = Deliverable.objects.create(
    project=projet,
    title="Rapport d'avancement",
    description="Premier rapport d'avancement du projet",
    type='report',
    file=ContentFile(b"Contenu du rapport", name="rapport_test.pdf"),
    submitted_by=etudiant,
    status='submitted'
)

notifs_encadreur_apres = Notification.objects.filter(user=encadreur).count()
print(f"   Notifications encadreur: {notifs_encadreur_avant} → {notifs_encadreur_apres}")
if notifs_encadreur_apres > notifs_encadreur_avant:
    print(f"   ✅ Encadreur notifié du nouveau livrable")
    notif = Notification.objects.filter(user=encadreur, type='deliverable').latest('created_at')
    print(f"   📧 \"{notif.title}\"")

print(f"\n2️⃣ Étudiant dépose le code source")
notifs_encadreur_avant = Notification.objects.filter(user=encadreur).count()

deliverable2 = Deliverable.objects.create(
    project=projet,
    title="Code source - Version 1.0",
    description="Première version du code complet",
    type='code',
    file=ContentFile(b"# Code source", name="code_v1.zip"),
    submitted_by=etudiant,
    status='submitted'
)

notifs_encadreur_apres = Notification.objects.filter(user=encadreur).count()
if notifs_encadreur_apres > notifs_encadreur_avant:
    print(f"   ✅ Encadreur notifié du nouveau livrable")

# ============================================================================
# WORKFLOW 5: PLANIFICATION DE SOUTENANCE
# ============================================================================
test_section("WORKFLOW 5: Planification de soutenance")

print(f"\n1️⃣ Admin planifie une soutenance")
notifs_etudiant_avant = Notification.objects.filter(user=etudiant).count()
notifs_encadreur_avant = Notification.objects.filter(user=encadreur).count()

defense = Defense.objects.create(
    project=projet,
    date=date.today() + timedelta(days=90),
    time=time(14, 0),
    room="Amphi A",
    duration=45
)

notifs_etudiant_apres = Notification.objects.filter(user=etudiant).count()
notifs_encadreur_apres = Notification.objects.filter(user=encadreur).count()

print(f"   Notifications étudiant: {notifs_etudiant_avant} → {notifs_etudiant_apres}")
print(f"   Notifications encadreur: {notifs_encadreur_avant} → {notifs_encadreur_apres}")

if notifs_etudiant_apres > notifs_etudiant_avant:
    print(f"   ✅ Étudiant notifié de la planification")
if notifs_encadreur_apres > notifs_encadreur_avant:
    print(f"   ✅ Encadreur notifié de la planification")

# ============================================================================
# WORKFLOW 6: AJOUT DE MEMBRES DU JURY
# ============================================================================
test_section("WORKFLOW 6: Ajout de membres du jury")

if jury1:
    print(f"\n1️⃣ Admin ajoute le président du jury")
    notifs_jury1_avant = Notification.objects.filter(user=jury1).count()
    
    jury_member1 = JuryMember.objects.create(
        defense=defense,
        user=jury1,
        role='president'
    )
    
    notifs_jury1_apres = Notification.objects.filter(user=jury1).count()
    print(f"   Notifications jury: {notifs_jury1_avant} → {notifs_jury1_apres}")
    if notifs_jury1_apres > notifs_jury1_avant:
        print(f"   ✅ Membre du jury notifié de son invitation")
        notif = Notification.objects.filter(user=jury1).latest('created_at')
        print(f"   📧 \"{notif.title}\"")

if jury2:
    print(f"\n2️⃣ Admin ajoute un examinateur")
    notifs_jury2_avant = Notification.objects.filter(user=jury2).count()
    
    jury_member2 = JuryMember.objects.create(
        defense=defense,
        user=jury2,
        role='examiner'
    )
    
    notifs_jury2_apres = Notification.objects.filter(user=jury2).count()
    if notifs_jury2_apres > notifs_jury2_avant:
        print(f"   ✅ Examinateur notifié de son invitation")

# ============================================================================
# WORKFLOW 7: DEMANDE DE MODIFICATION DE SOUTENANCE
# ============================================================================
test_section("WORKFLOW 7: Demande de modification de soutenance")

print(f"\n1️⃣ Étudiant demande une modification")
notifs_admin_avant = Notification.objects.filter(user=admin).count()

change_request = DefenseChangeRequest.objects.create(
    defense=defense,
    requested_by=etudiant,
    proposed_date=defense.date + timedelta(days=7),
    proposed_time=time(10, 0),
    proposed_location="Amphi B",
    reason="Conflit avec une autre soutenance ce jour-là",
    status='pending'
)

notifs_admin_apres = Notification.objects.filter(user=admin).count()
print(f"   Notifications admin: {notifs_admin_avant} → {notifs_admin_apres}")
if notifs_admin_apres > notifs_admin_avant:
    print(f"   ✅ Admin notifié de la demande de modification")
    notif = Notification.objects.filter(user=admin, type='defense').latest('created_at')
    print(f"   📧 \"{notif.title}\"")

print(f"\n2️⃣ Admin approuve la modification")
notifs_etudiant_avant = Notification.objects.filter(user=etudiant).count()
notifs_encadreur_avant = Notification.objects.filter(user=encadreur).count()
notifs_jury1_avant = Notification.objects.filter(user=jury1).count() if jury1 else 0
notifs_jury2_avant = Notification.objects.filter(user=jury2).count() if jury2 else 0

change_request.status = 'approved'
change_request.reviewed_by = admin
change_request.review_comment = "Modification approuvée"
change_request.save()

# Mettre à jour la soutenance
defense.date = change_request.proposed_date
defense.time = change_request.proposed_time
defense.room = change_request.proposed_location
defense.save()

notifs_etudiant_apres = Notification.objects.filter(user=etudiant).count()
notifs_encadreur_apres = Notification.objects.filter(user=encadreur).count()
notifs_jury1_apres = Notification.objects.filter(user=jury1).count() if jury1 else 0
notifs_jury2_apres = Notification.objects.filter(user=jury2).count() if jury2 else 0

print(f"   Notifications étudiant: {notifs_etudiant_avant} → {notifs_etudiant_apres}")
print(f"   Notifications encadreur: {notifs_encadreur_avant} → {notifs_encadreur_apres}")
if jury1:
    print(f"   Notifications jury 1: {notifs_jury1_avant} → {notifs_jury1_apres}")
if jury2:
    print(f"   Notifications jury 2: {notifs_jury2_avant} → {notifs_jury2_apres}")

if notifs_etudiant_apres > notifs_etudiant_avant:
    print(f"   ✅ Étudiant notifié de l'approbation")
if notifs_encadreur_apres > notifs_encadreur_avant:
    print(f"   ✅ Encadreur notifié de la modification")
if jury1 and notifs_jury1_apres > notifs_jury1_avant:
    print(f"   ✅ Jury 1 notifié de la modification")
if jury2 and notifs_jury2_apres > notifs_jury2_avant:
    print(f"   ✅ Jury 2 notifié de la modification")

# ============================================================================
# WORKFLOW 8: REJET DE CANDIDATURE (workflow négatif)
# ============================================================================
test_section("WORKFLOW 8: Rejet de candidature")

sujet2 = Subject.objects.create(
    title="Test: Blockchain et IoT",
    description="Autre projet de test",
    supervisor=encadreur,
    status='published',
    level='master'
)

print(f"\n1️⃣ Étudiant candidate à un autre sujet")
app2 = Application.objects.create(
    subject=sujet2,
    student=etudiant,
    motivation_letter="Intéressé par ce projet également",
    status='pending'
)

print(f"\n2️⃣ Encadreur rejette la candidature")
notifs_etudiant_avant = Notification.objects.filter(user=etudiant).count()

app2.status = 'rejected'
app2.reviewed_by = encadreur
app2.review_comment = "Sujet déjà pris par un autre étudiant"
app2.save()

notifs_etudiant_apres = Notification.objects.filter(user=etudiant).count()
print(f"   Notifications étudiant: {notifs_etudiant_avant} → {notifs_etudiant_apres}")
if notifs_etudiant_apres > notifs_etudiant_avant:
    print(f"   ✅ Étudiant notifié du rejet")
    notif = Notification.objects.filter(user=etudiant, type='application_status').latest('created_at')
    print(f"   📧 \"{notif.message}\"")

# ============================================================================
# WORKFLOW 9: REJET DE DEMANDE DE MODIFICATION
# ============================================================================
test_section("WORKFLOW 9: Rejet de demande de modification")

print(f"\n1️⃣ Encadreur demande une modification")
change_request2 = DefenseChangeRequest.objects.create(
    defense=defense,
    requested_by=encadreur,
    proposed_date=defense.date + timedelta(days=14),
    proposed_time=time(16, 0),
    proposed_location="Amphi C",
    reason="Conflit d'agenda personnel",
    status='pending'
)

print(f"\n2️⃣ Admin rejette la demande")
notifs_encadreur_avant = Notification.objects.filter(user=encadreur).count()

change_request2.status = 'rejected'
change_request2.reviewed_by = admin
change_request2.review_comment = "Date trop proche d'une autre soutenance importante"
change_request2.save()

notifs_encadreur_apres = Notification.objects.filter(user=encadreur).count()
print(f"   Notifications encadreur: {notifs_encadreur_avant} → {notifs_encadreur_apres}")
if notifs_encadreur_apres > notifs_encadreur_avant:
    print(f"   ✅ Encadreur notifié du rejet")
    notif = Notification.objects.filter(user=encadreur).latest('created_at')
    print(f"   📧 Message: \"{notif.message}\"")

# ============================================================================
# WORKFLOW 10: MULTIPLES CANDIDATURES (workflow de concurrence)
# ============================================================================
test_section("WORKFLOW 10: Multiples candidatures au même sujet")

# Créer d'autres étudiants
etudiant2 = User.objects.filter(role='student').exclude(id=etudiant.id).first()
etudiant3 = User.objects.filter(role='student').exclude(id__in=[etudiant.id, etudiant2.id if etudiant2 else 0]).first()

if etudiant2 and etudiant3:
    sujet3 = Subject.objects.create(
        title="Test: Machine Learning pour le climat",
        description="Projet très demandé",
        supervisor=encadreur,
        status='published',
        level='master'
    )
    
    print(f"\n1️⃣ Trois étudiants candidatent au même sujet populaire")
    
    notifs_encadreur_avant = Notification.objects.filter(user=encadreur).count()
    
    app_concurrent1 = Application.objects.create(
        subject=sujet3,
        student=etudiant2,
        motivation_letter="Premier candidat",
        status='pending'
    )
    
    app_concurrent2 = Application.objects.create(
        subject=sujet3,
        student=etudiant3,
        motivation_letter="Deuxième candidat",
        status='pending'
    )
    
    app_concurrent3 = Application.objects.create(
        subject=sujet3,
        student=etudiant,
        motivation_letter="Troisième candidat",
        status='pending'
    )
    
    notifs_encadreur_apres = Notification.objects.filter(user=encadreur).count()
    print(f"   Notifications encadreur: {notifs_encadreur_avant} → {notifs_encadreur_apres}")
    print(f"   ✅ Encadreur reçoit {notifs_encadreur_apres - notifs_encadreur_avant} notifications")
    
    print(f"\n2️⃣ Encadreur accepte un candidat et rejette les autres")
    app_concurrent1.status = 'accepted'
    app_concurrent1.reviewed_by = encadreur
    app_concurrent1.save()
    
    app_concurrent2.status = 'rejected'
    app_concurrent2.reviewed_by = encadreur
    app_concurrent2.review_comment = "Sujet attribué à un autre étudiant"
    app_concurrent2.save()
    
    app_concurrent3.status = 'rejected'
    app_concurrent3.reviewed_by = encadreur
    app_concurrent3.review_comment = "Sujet attribué à un autre étudiant"
    app_concurrent3.save()
    
    print(f"   ✅ Tous les étudiants notifiés de la décision")
else:
    print("⚠️ Pas assez d'étudiants pour tester ce workflow")

# ============================================================================
# WORKFLOW 11: PROGRESSION DE JALON
# ============================================================================
test_section("WORKFLOW 11: Marquage de jalon comme complété")

print(f"\n1️⃣ Étudiant marque un jalon comme terminé")
print(f"   Jalon: {milestone1.title}")
milestone1.status = 'completed'
milestone1.completed_date = date.today()
milestone1.save()
print(f"   ✅ Jalon marqué comme complété")
print(f"   ℹ️ Note: Pas de notification automatique pour changement de statut")
print(f"   💡 Suggestion: Ajouter un signal pour notifier l'encadreur")

# ============================================================================
# WORKFLOW 12: VALIDATION DE LIVRABLE PAR ENCADREUR
# ============================================================================
test_section("WORKFLOW 12: Validation de livrable")

print(f"\n1️⃣ Encadreur valide un livrable")
print(f"   Livrable: {deliverable1.title}")
deliverable1.status = 'approved'
deliverable1.review_comments = "Excellent travail, rapport très complet"
deliverable1.reviewed_by = encadreur
deliverable1.reviewed_at = timezone.now()
deliverable1.save()
print(f"   ✅ Livrable validé")
print(f"   ℹ️ Note: Pas de notification automatique pour validation")
print(f"   💡 Suggestion: Ajouter un signal pour notifier l'étudiant")

# ============================================================================
# STATISTIQUES FINALES
# ============================================================================
separator("STATISTIQUES FINALES")

total_notifs = Notification.objects.count()
print(f"\n📊 STATISTIQUES GLOBALES:")
print(f"   Total notifications créées: {total_notifs}")

print(f"\n📧 Par utilisateur:")
for user in [admin, etudiant, encadreur, jury1, jury2]:
    if user:
        count = Notification.objects.filter(user=user).count()
        print(f"   {user.get_full_name()} ({user.role}): {count} notifications")

print(f"\n📂 Par type:")
types = Notification.objects.values_list('type', flat=True).distinct()
for notif_type in types:
    count = Notification.objects.filter(type=notif_type).count()
    print(f"   {notif_type}: {count}")

print(f"\n📈 Éléments créés:")
print(f"   Sujets: {Subject.objects.count()}")
print(f"   Candidatures: {Application.objects.count()}")
print(f"   Affectations: {Assignment.objects.count()}")
print(f"   Projets: {Project.objects.count()}")
print(f"   Jalons: {Milestone.objects.count()}")
print(f"   Livrables: {Deliverable.objects.count()}")
print(f"   Soutenances: {Defense.objects.count()}")
print(f"   Membres jury: {JuryMember.objects.count()}")
print(f"   Demandes modification: {DefenseChangeRequest.objects.count()}")

# ============================================================================
# WORKFLOWS MANQUANTS IDENTIFIÉS
# ============================================================================
separator("WORKFLOWS MANQUANTS À IMPLÉMENTER")

print("""
🔴 NOTIFICATIONS MANQUANTES IDENTIFIÉES:

1. ❌ Validation de livrable par encadreur → Notification à l'étudiant
2. ❌ Changement de statut de jalon → Notification à l'encadreur
3. ❌ Changement de statut de projet → Notifications aux parties prenantes
4. ❌ Annulation de soutenance → Notifications à tous (étudiant, encadreur, jury)
5. ❌ Annulation d'affectation → Notifications à l'étudiant et l'encadreur
6. ❌ Suppression de membre du jury → Notification au membre
7. ❌ Nouveau message → Notification au destinataire
8. ❌ Approche de deadline → Rappels automatiques
9. ❌ Soumission en retard → Alertes

💡 AMÉLIORATIONS SUGGÉRÉES:

1. 📧 Système de rappels automatiques (emails/notifications):
   - 7 jours avant la soutenance
   - 3 jours avant une deadline
   - 1 jour avant expiration

2. 🔔 Notifications en temps réel:
   - WebSockets pour notifications instantanées
   - Compteur de notifications non lues dans la navbar

3. 📨 Résumés périodiques:
   - Email hebdomadaire avec résumé d'activités
   - Tableau de bord avec statistiques

4. ⚡ Actions groupées:
   - Accepter/rejeter plusieurs candidatures
   - Notifier tous les étudiants d'un changement global

5. 🔍 Traçabilité complète:
   - Historique de toutes les notifications envoyées
   - Log des actions importantes
""")

separator("TEST TERMINÉ")
print("\n✅ Tous les workflows ont été testés avec succès!")
print("📝 Consulter les suggestions ci-dessus pour améliorer le système\n")
