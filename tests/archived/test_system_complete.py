"""
Test complet et exhaustif du système de gestion PFE
Vérifie: URLs, templates, vues, workflows, permissions
"""
import os
import django
from pathlib import Path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.urls import get_resolver, reverse, NoReverseMatch
from django.template.loader import get_template
from django.template import TemplateDoesNotExist
from django.contrib.auth.models import AnonymousUser
from users.models import User

BASE_DIR = Path(__file__).resolve().parent

def separator(title, char="="):
    print(f"\n{char * 80}")
    print(title.center(80))
    print(f"{char * 80}")

def subsection(title):
    print(f"\n{'─' * 80}")
    print(f"📋 {title}")
    print('─' * 80)

separator("TEST COMPLET DU SYSTÈME DE GESTION PFE", "=")

# ============================================================================
# 1. TEST DES URLs
# ============================================================================
separator("1. VÉRIFICATION DES URLs", "=")

# URLs à tester par app
urls_to_test = {
    'users': [
        'users:register',
        'users:login',
        'users:logout',
        'users:profile',
        'users:dashboard',
        'users:user_list',
    ],
    'subjects': [
        'subjects:subject_list',
        'subjects:subject_create',
        'subjects:my_subjects',
        'subjects:my_applications',
        'subjects:assignments_manage',
    ],
    'projects': [
        'projects:project_list',
        'projects:my_projects',
    ],
    'defenses': [
        'defenses:defense_list',
        'defenses:defense_planning',
    ],
    'communications': [
        'communications:message_list',
        'communications:notification_list',
    ],
    'archives': [
        'archives:archive_list',
    ],
}

print("\n🔍 Test de résolution des URLs...")
urls_ok = []
urls_missing = []

for app, url_names in urls_to_test.items():
    subsection(f"App: {app}")
    for url_name in url_names:
        try:
            url = reverse(url_name)
            urls_ok.append(url_name)
            print(f"   ✅ {url_name:40} → {url}")
        except NoReverseMatch:
            urls_missing.append(url_name)
            print(f"   ❌ {url_name:40} → URL NOT FOUND")

print(f"\n📊 Résumé URLs: {len(urls_ok)} OK, {len(urls_missing)} MANQUANTES")

# ============================================================================
# 2. TEST DES TEMPLATES
# ============================================================================
separator("2. VÉRIFICATION DES TEMPLATES", "=")

# Templates à vérifier
templates_to_check = {
    'base': [
        'base.html',
        'home.html',
    ],
    'users': [
        'users/register.html',
        'users/login.html',
        'users/profile.html',
        'users/profile_edit.html',
        'users/dashboard_admin.html',
        'users/dashboard_student.html',
        'users/dashboard_supervisor.html',
        'users/user_list.html',
        'users/user_detail.html',
    ],
    'subjects': [
        'subjects/subject_list.html',
        'subjects/subject_detail.html',
        'subjects/subject_form.html',
        'subjects/subject_create.html',
        'subjects/subject_edit.html',
        'subjects/my_subjects.html',
        'subjects/my_applications.html',
        'subjects/application_form.html',
        'subjects/application_detail.html',
        'subjects/assignments_manage.html',
        'subjects/assignment_create.html',
        'subjects/assignment_cancel.html',
    ],
    'projects': [
        'projects/project_list.html',
        'projects/project_detail.html',
        'projects/project_form.html',
        'projects/project_create.html',
        'projects/project_edit.html',
        'projects/my_projects.html',
        'projects/milestone_form.html',
        'projects/deliverable_form.html',
    ],
    'defenses': [
        'defenses/defense_list.html',
        'defenses/defense_detail.html',
        'defenses/defense_form.html',
        'defenses/defense_planning.html',
        'defenses/defense_update.html',
        'defenses/defense_change_request.html',
        'defenses/defense_change_review.html',
    ],
    'communications': [
        'communications/message_list.html',
        'communications/message_detail.html',
        'communications/message_form.html',
        'communications/notification_list.html',
    ],
    'archives': [
        'archives/archive_list.html',
        'archives/archive_detail.html',
    ],
}

print("\n🔍 Test de présence des templates...")
templates_ok = []
templates_missing = []
templates_error = []

for category, template_list in templates_to_check.items():
    subsection(f"Catégorie: {category}")
    for template_name in template_list:
        try:
            get_template(template_name)
            templates_ok.append(template_name)
            print(f"   ✅ {template_name}")
        except TemplateDoesNotExist:
            templates_missing.append(template_name)
            print(f"   ❌ {template_name} → TEMPLATE NOT FOUND")
        except Exception as e:
            templates_error.append((template_name, str(e)))
            print(f"   ⚠️ {template_name} → SYNTAX ERROR: {str(e)[:50]}...")

print(f"\n📊 Résumé Templates: {len(templates_ok)} OK, {len(templates_missing)} MANQUANTS, {len(templates_error)} ERREURS")

# ============================================================================
# 3. TEST DES VUES (VIEWS)
# ============================================================================
separator("3. VÉRIFICATION DES VUES", "=")

subsection("Vérification imports des vues")

views_to_check = {
    'users.views': [
        'register_view', 'login_view', 'logout_view', 
        'profile_view', 'profile_edit_view', 'dashboard_view',
        'user_list_view', 'user_detail_view'
    ],
    'subjects.views': [
        'subject_list_view', 'subject_detail_view', 'subject_create_view',
        'subject_edit_view', 'subject_delete_view', 'my_subjects_view',
        'application_create_view', 'application_review_view', 'my_applications_view',
        'assignments_manage_view', 'assignment_create_view', 'assignment_cancel_view'
    ],
    'projects.views': [
        'project_list_view', 'project_detail_view', 'project_create_view',
        'project_edit_view', 'my_projects_view',
        'milestone_create_view', 'deliverable_create_view'
    ],
    'defenses.views': [
        'defense_list_view', 'defense_detail_view', 'defense_create_view',
        'defense_planning_view', 'defense_update_view',
        'defense_change_request_create_view', 'defense_change_request_review_view'
    ],
    'communications.views': [
        'message_list_view', 'message_detail_view', 'message_create_view',
        'notification_list_view', 'mark_notification_read_view'
    ],
    'archives.views': [
        'archive_list_view', 'archive_detail_view'
    ],
}

views_ok = []
views_missing = []

for module_name, view_list in views_to_check.items():
    subsection(f"Module: {module_name}")
    try:
        module = __import__(module_name, fromlist=view_list)
        for view_name in view_list:
            if hasattr(module, view_name):
                views_ok.append(f"{module_name}.{view_name}")
                print(f"   ✅ {view_name}")
            else:
                views_missing.append(f"{module_name}.{view_name}")
                print(f"   ❌ {view_name} → VIEW NOT FOUND")
    except ImportError as e:
        print(f"   ⚠️ Erreur d'import du module: {e}")

print(f"\n📊 Résumé Vues: {len(views_ok)} OK, {len(views_missing)} MANQUANTES")

# ============================================================================
# 4. TEST DES MODÈLES
# ============================================================================
separator("4. VÉRIFICATION DES MODÈLES", "=")

subsection("Vérification des modèles et relations")

from users.models import User, Profile
from subjects.models import Subject, Application, Assignment
from projects.models import Project, Milestone, Deliverable, Comment
from defenses.models import Defense, JuryMember, DefenseChangeRequest
from communications.models import Message, Notification
from archives.models import Archive

models_info = {
    'User': User.objects.count(),
    'Profile': Profile.objects.count(),
    'Subject': Subject.objects.count(),
    'Application': Application.objects.count(),
    'Assignment': Assignment.objects.count(),
    'Project': Project.objects.count(),
    'Milestone': Milestone.objects.count(),
    'Deliverable': Deliverable.objects.count(),
    'Defense': Defense.objects.count(),
    'JuryMember': JuryMember.objects.count(),
    'DefenseChangeRequest': DefenseChangeRequest.objects.count(),
    'Message': Message.objects.count(),
    'Notification': Notification.objects.count(),
    'Archive': Archive.objects.count(),
}

print("\n📊 Données en base:")
for model_name, count in models_info.items():
    print(f"   {model_name:25} → {count:4} enregistrement(s)")

# ============================================================================
# 5. TEST DES WORKFLOWS COMPLETS
# ============================================================================
separator("5. VÉRIFICATION DES WORKFLOWS", "=")

subsection("Workflow 1: Candidature d'étudiant")
workflow1_steps = [
    ("URL liste des sujets", 'subjects:subject_list' in [u for u in urls_ok]),
    ("Template liste sujets", 'subjects/subject_list.html' in templates_ok),
    ("URL détail sujet", 'subjects:subject_detail_view' in views_ok or 'subjects.views.subject_detail_view' in views_ok),
    ("Template candidature", 'subjects/application_form.html' in templates_ok),
    ("Vue mes candidatures", 'subjects:my_applications' in [u for u in urls_ok]),
]

print("\nÉtapes du workflow:")
for step, status in workflow1_steps:
    icon = "✅" if status else "❌"
    print(f"   {icon} {step}")

subsection("Workflow 2: Affectation de sujet")
workflow2_steps = [
    ("URL gestion affectations", 'subjects:assignments_manage' in [u for u in urls_ok]),
    ("Template gestion affectations", 'subjects/assignments_manage.html' in templates_ok),
    ("Vue création affectation", 'subjects:assignment_create_view' in views_ok or 'subjects.views.assignment_create_view' in views_ok),
    ("Template création affectation", 'subjects/assignment_create.html' in templates_ok),
]

print("\nÉtapes du workflow:")
for step, status in workflow2_steps:
    icon = "✅" if status else "❌"
    print(f"   {icon} {step}")

subsection("Workflow 3: Gestion de projet")
workflow3_steps = [
    ("URL liste projets", 'projects:project_list' in [u for u in urls_ok]),
    ("Template liste projets", 'projects/project_list.html' in templates_ok),
    ("URL mes projets", 'projects:my_projects' in [u for u in urls_ok]),
    ("Template détail projet", 'projects/project_detail.html' in templates_ok),
    ("Vue création jalon", 'projects:milestone_create_view' in views_ok or 'projects.views.milestone_create_view' in views_ok),
    ("Vue création livrable", 'projects:deliverable_create_view' in views_ok or 'projects.views.deliverable_create_view' in views_ok),
]

print("\nÉtapes du workflow:")
for step, status in workflow3_steps:
    icon = "✅" if status else "❌"
    print(f"   {icon} {step}")

subsection("Workflow 4: Planification soutenance")
workflow4_steps = [
    ("URL planification", 'defenses:defense_planning' in [u for u in urls_ok]),
    ("Template planification", 'defenses/defense_planning.html' in templates_ok),
    ("Vue création soutenance", 'defenses:defense_create_view' in views_ok or 'defenses.views.defense_create_view' in views_ok),
    ("Vue demande modification", 'defenses:defense_change_request_create_view' in views_ok or 'defenses.views.defense_change_request_create_view' in views_ok),
    ("Template demande modification", 'defenses/defense_change_request.html' in templates_ok),
]

print("\nÉtapes du workflow:")
for step, status in workflow4_steps:
    icon = "✅" if status else "❌"
    print(f"   {icon} {step}")

subsection("Workflow 5: Communication")
workflow5_steps = [
    ("URL liste messages", 'communications:message_list' in [u for u in urls_ok]),
    ("Template liste messages", 'communications/message_list.html' in templates_ok),
    ("Vue création message", 'communications:message_create_view' in views_ok or 'communications.views.message_create_view' in views_ok),
    ("URL notifications", 'communications:notification_list' in [u for u in urls_ok]),
    ("Template notifications", 'communications/notification_list.html' in templates_ok),
]

print("\nÉtapes du workflow:")
for step, status in workflow5_steps:
    icon = "✅" if status else "❌"
    print(f"   {icon} {step}")

# ============================================================================
# 6. VÉRIFICATION DES FICHIERS STATIQUES
# ============================================================================
separator("6. VÉRIFICATION DES FICHIERS STATIQUES", "=")

static_files_to_check = [
    'static/css/style.css',
    'static/js/main.js',
]

print("\n🔍 Test de présence des fichiers statiques...")
static_ok = []
static_missing = []

for static_file in static_files_to_check:
    file_path = BASE_DIR / static_file
    if file_path.exists():
        static_ok.append(static_file)
        print(f"   ✅ {static_file}")
    else:
        static_missing.append(static_file)
        print(f"   ❌ {static_file} → FILE NOT FOUND")

print(f"\n📊 Résumé Statiques: {len(static_ok)} OK, {len(static_missing)} MANQUANTS")

# ============================================================================
# 7. TEST DES PERMISSIONS ET RÔLES
# ============================================================================
separator("7. VÉRIFICATION DES PERMISSIONS", "=")

subsection("Vérification des rôles utilisateurs")

roles = ['admin', 'student', 'supervisor']
users_by_role = {role: User.objects.filter(role=role).count() for role in roles}

print("\n👥 Utilisateurs par rôle:")
for role, count in users_by_role.items():
    print(f"   {role:15} → {count:3} utilisateur(s)")

# Test des méthodes de permission
admin = User.objects.filter(role='admin').first()
student = User.objects.filter(role='student').first()
supervisor = User.objects.filter(role='supervisor').first()

subsection("Test des méthodes de permission")

if admin:
    print("\n👤 Admin:")
    print(f"   is_admin_staff(): {admin.is_admin_staff()}")
    print(f"   is_student(): {admin.is_student()}")
    print(f"   is_supervisor(): {admin.is_supervisor()}")

if student:
    print("\n👤 Student:")
    print(f"   is_admin_staff(): {student.is_admin_staff()}")
    print(f"   is_student(): {student.is_student()}")
    print(f"   is_supervisor(): {student.is_supervisor()}")

if supervisor:
    print("\n👤 Supervisor:")
    print(f"   is_admin_staff(): {supervisor.is_admin_staff()}")
    print(f"   is_student(): {supervisor.is_student()}")
    print(f"   is_supervisor(): {supervisor.is_supervisor()}")

# ============================================================================
# 8. ANALYSE DES PROBLÈMES IDENTIFIÉS
# ============================================================================
separator("8. ANALYSE DES PROBLÈMES IDENTIFIÉS", "=")

problemes = []

# Problème 1: URLs manquantes
if urls_missing:
    problemes.append({
        'titre': 'URLs manquantes',
        'gravité': 'HAUTE',
        'details': urls_missing,
        'impact': 'Certaines pages ne sont pas accessibles via l\'interface web'
    })

# Problème 2: Templates manquants
if templates_missing:
    problemes.append({
        'titre': 'Templates manquants',
        'gravité': 'HAUTE',
        'details': templates_missing[:10],  # Limiter l'affichage
        'impact': 'Erreurs 500 lors de l\'accès à certaines pages'
    })

# Problème 3: Vues manquantes
if views_missing:
    problemes.append({
        'titre': 'Vues manquantes',
        'gravité': 'MOYENNE',
        'details': views_missing,
        'impact': 'Fonctionnalités non implémentées'
    })

# Problème 4: Fichiers statiques manquants
if static_missing:
    problemes.append({
        'titre': 'Fichiers statiques manquants',
        'gravité': 'BASSE',
        'details': static_missing,
        'impact': 'Interface utilisateur dégradée'
    })

# Problème 5: Workflows incomplets
workflows_incomplets = []
if not all([status for _, status in workflow1_steps]):
    workflows_incomplets.append("Workflow Candidature")
if not all([status for _, status in workflow2_steps]):
    workflows_incomplets.append("Workflow Affectation")
if not all([status for _, status in workflow3_steps]):
    workflows_incomplets.append("Workflow Gestion Projet")
if not all([status for _, status in workflow4_steps]):
    workflows_incomplets.append("Workflow Soutenance")
if not all([status for _, status in workflow5_steps]):
    workflows_incomplets.append("Workflow Communication")

if workflows_incomplets:
    problemes.append({
        'titre': 'Workflows incomplets',
        'gravité': 'HAUTE',
        'details': workflows_incomplets,
        'impact': 'Parcours utilisateur incomplet, fonctionnalités inaccessibles'
    })

print("\n🔴 PROBLÈMES IDENTIFIÉS:")
print(f"\nNombre total de problèmes: {len(problemes)}")

for i, pb in enumerate(problemes, 1):
    print(f"\n{'─' * 80}")
    print(f"Problème {i}: {pb['titre']} (Gravité: {pb['gravité']})")
    print(f"Impact: {pb['impact']}")
    print(f"Détails: {len(pb['details']) if isinstance(pb['details'], list) else 1} élément(s)")
    if isinstance(pb['details'], list) and len(pb['details']) <= 10:
        for detail in pb['details']:
            print(f"   - {detail}")
    elif isinstance(pb['details'], list):
        for detail in pb['details'][:5]:
            print(f"   - {detail}")
        print(f"   ... et {len(pb['details']) - 5} autres")

# ============================================================================
# 9. RECOMMANDATIONS
# ============================================================================
separator("9. RECOMMANDATIONS DE CORRECTION", "=")

print("""
📝 PLAN D'ACTION PRIORITAIRE:

1. 🔴 CRITIQUE - Templates manquants
   → Créer tous les templates manquants pour éviter les erreurs 500
   → Priorité: templates de base (list, detail, form) pour chaque app
   
2. 🔴 CRITIQUE - URLs manquantes
   → Ajouter les URLs manquantes dans les fichiers urls.py
   → Vérifier la cohérence avec les templates et vues
   
3. 🟡 IMPORTANT - Workflows incomplets
   → Compléter les workflows de bout en bout
   → S'assurer que chaque action utilisateur a un chemin complet
   
4. 🟡 IMPORTANT - Vues manquantes
   → Implémenter les vues nécessaires pour les templates existants
   → Ajouter les vues pour les actions CRUD manquantes
   
5. 🟢 MINEUR - Améliorer l'interface
   → Vérifier que tous les liens dans les templates fonctionnent
   → Ajouter des boutons d'action manquants
   → Améliorer la navigation entre les pages
   
6. 🟢 MINEUR - Tests et validation
   → Tester manuellement chaque workflow
   → Vérifier les permissions pour chaque rôle
   → Valider l'affichage responsive
""")

# ============================================================================
# 10. RÉSUMÉ FINAL
# ============================================================================
separator("10. RÉSUMÉ FINAL", "=")

total_elements = (
    len(urls_ok) + len(urls_missing) +
    len(templates_ok) + len(templates_missing) +
    len(views_ok) + len(views_missing)
)
elements_ok = len(urls_ok) + len(templates_ok) + len(views_ok)
pourcentage = (elements_ok / total_elements * 100) if total_elements > 0 else 0

print(f"""
📊 STATISTIQUES GLOBALES:

   URLs:        {len(urls_ok):3} OK / {len(urls_ok) + len(urls_missing):3} total
   Templates:   {len(templates_ok):3} OK / {len(templates_ok) + len(templates_missing):3} total
   Vues:        {len(views_ok):3} OK / {len(views_ok) + len(views_missing):3} total
   
   Modèles:     {len(models_info)} modèles avec {sum(models_info.values())} enregistrements
   Problèmes:   {len(problemes)} problèmes majeurs identifiés
   
   ✨ Complétude globale: {pourcentage:.1f}%
""")

if pourcentage >= 80:
    print("   ✅ Système globalement fonctionnel, corrections mineures nécessaires")
elif pourcentage >= 60:
    print("   ⚠️ Système partiellement fonctionnel, corrections importantes nécessaires")
else:
    print("   🔴 Système incomplet, corrections majeures nécessaires")

separator("FIN DU TEST SYSTÈME", "=")
print()
