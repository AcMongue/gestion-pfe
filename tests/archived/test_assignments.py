"""
Script pour tester la nouvelle interface d'affectation des sujets
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from users.models import User
from subjects.models import Subject, Application, Assignment

print("=" * 70)
print("TEST DE LA NOUVELLE INTERFACE D'AFFECTATION")
print("=" * 70)

# Vérifier les utilisateurs admin
admins = User.objects.filter(role='admin')
print(f"\n✓ Administrateurs: {admins.count()}")
for admin in admins:
    print(f"  - {admin.get_full_name()} ({admin.email})")

# Vérifier les candidatures acceptées
accepted_apps = Application.objects.filter(status='accepted')
print(f"\n✓ Candidatures acceptées: {accepted_apps.count()}")
for app in accepted_apps:
    has_assignment = Assignment.objects.filter(
        student=app.student,
        status='active'
    ).exists()
    status = "✓ Déjà affectée" if has_assignment else "⏳ En attente d'affectation"
    print(f"  - {app.student.get_full_name()} -> {app.subject.title}")
    print(f"    {status}")

# Vérifier les affectations existantes
assignments = Assignment.objects.all()
print(f"\n✓ Affectations totales: {assignments.count()}")
for assignment in assignments:
    print(f"  - {assignment.student.get_full_name()} -> {assignment.subject.title}")
    print(f"    Statut: {assignment.get_status_display()}")
    print(f"    Affecté le: {assignment.created_at.strftime('%d/%m/%Y')}")
    if assignment.assigned_by:
        print(f"    Par: {assignment.assigned_by.get_full_name()}")

print("\n" + "=" * 70)
print("INSTRUCTIONS POUR TESTER")
print("=" * 70)
print("""
1. Connectez-vous en tant qu'admin:
   - Email: admin@enspd.edu
   - Mot de passe: admin123

2. Allez sur le tableau de bord admin

3. Cliquez sur "Gérer les affectations"

4. Vous devriez voir:
   - Les candidatures acceptées en attente d'affectation
   - Toutes les affectations existantes

5. Pour affecter un sujet:
   - Cliquez sur "Affecter" pour une candidature
   - Confirmez l'affectation
   - Le sujet sera automatiquement affecté à l'étudiant
   - Les autres candidatures pour ce sujet seront rejetées

6. Pour annuler une affectation:
   - Cliquez sur "Annuler" pour une affectation active
   - Le sujet redeviendra disponible

Note: Plus besoin d'utiliser l'interface /admin/ de Django!
""")
print("=" * 70)
