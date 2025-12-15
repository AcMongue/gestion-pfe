# Generated migration to rename supervisor role to teacher and remove jury role

from django.db import migrations


def update_roles_forward(apps, schema_editor):
    """
    Renommer 'supervisor' en 'teacher' et supprimer 'jury'.
    Les membres du jury seront des teachers avec academic_title.
    """
    User = apps.get_model('users', 'User')
    
    # Renommer supervisor → teacher
    User.objects.filter(role='supervisor').update(role='teacher')
    
    # Convertir jury → teacher (ils auront un academic_title)
    jury_users = User.objects.filter(role='jury')
    for user in jury_users:
        user.role = 'teacher'
        # S'assurer qu'ils ont un academic_title
        if not user.academic_title:
            user.academic_title = 'maitre_assistant'  # Par défaut
        user.save()


def update_roles_backward(apps, schema_editor):
    """
    Restaurer les anciens rôles en cas de rollback.
    """
    User = apps.get_model('users', 'User')
    
    # Restaurer teacher → supervisor
    User.objects.filter(role='teacher').update(role='supervisor')


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_add_entry_level_m2_only'),
    ]

    operations = [
        migrations.RunPython(update_roles_forward, update_roles_backward),
    ]
