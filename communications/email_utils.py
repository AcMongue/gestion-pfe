# communications/email_utils.py
# Système centralisé de notifications par email

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.utils import timezone
from .models import Notification


def send_notification_email(recipients, subject, template, context, attachments=None):
    """
    Fonction centralisée pour envoyer des emails de notification.
    
    Args:
        recipients: Liste d'emails (strings)
        subject: Objet du mail
        template: Chemin du template HTML (ex: 'emails/new_subject.html')
        context: Contexte pour le template (dict)
        attachments: Liste de tuples (filename, content, mimetype) optionnel
    
    Returns:
        bool: True si envoyé avec succès
    """
    try:
        # Rendre le template HTML
        html_content = render_to_string(template, context)
        
        # Créer l'email
        email = EmailMultiAlternatives(
            subject=subject,
            body=html_content,  # Fallback texte
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=recipients if isinstance(recipients, list) else [recipients]
        )
        email.attach_alternative(html_content, "text/html")
        
        # Ajouter les pièces jointes
        if attachments:
            for filename, content, mimetype in attachments:
                email.attach(filename, content, mimetype)
        
        # Envoyer
        email.send()
        
        # Enregistrer dans la base
        Notification.objects.create(
            recipients=recipients if isinstance(recipients, list) else [recipients],
            subject=subject,
            sent_at=timezone.now()
        )
        
        return True
    
    except Exception as e:
        print(f"Erreur envoi email: {e}")
        return False


def notify_thesis_deadline_reminder(students, deadline):
    """
    Notification J-7 avant la date limite de dépôt du mémoire.
    
    Args:
        students: QuerySet d'étudiants
        deadline: Date limite
    """
    for student in students:
        send_notification_email(
            recipients=[student.email],
            subject="Rappel : Date limite de dépôt du mémoire",
            template='emails/thesis_deadline_reminder.html',
            context={
                'student': student,
                'deadline': deadline
            }
        )


def distribute_thesis_to_jury(project):
    """
    Envoie le mémoire à tous les membres du jury.
    
    Args:
        project: Instance de Project
    """
    if not project.thesis_file:
        return False
    
    defense = project.defense
    jury_members = defense.defense_jury_members.all()
    
    # Préparer la pièce jointe
    with project.thesis_file.open('rb') as f:
        thesis_content = f.read()
    
    for member in jury_members:
        send_notification_email(
            recipients=[member.teacher.email],
            subject=f"Mémoire à évaluer - {project.title}",
            template='emails/thesis_distribution.html',
            context={
                'teacher': member.teacher,
                'project': project,
                'defense': defense,
                'role': member.get_role_display()
            },
            attachments=[
                (f'memoire_{project.id}.pdf', thesis_content, 'application/pdf')
            ]
        )
    
    return True


def notify_defense_reminder(defense, days_before=3):
    """
    Notification J-3 avant la soutenance pour tous les participants.
    
    Args:
        defense: Instance de Defense
        days_before: Nombre de jours avant (par défaut 3)
    """
    project = defense.project
    team = project.team
    
    # Liste des destinataires
    recipients = []
    
    # Étudiant(s)
    recipients.append(team.student1.email)
    if team.student2:
        recipients.append(team.student2.email)
    
    # Membres du jury
    for member in defense.defense_jury_members.all():
        recipients.append(member.teacher.email)
    
    # Envoyer à tous
    send_notification_email(
        recipients=recipients,
        subject=f"Rappel : Soutenance dans {days_before} jours - {project.title}",
        template='emails/defense_reminder.html',
        context={
            'defense': defense,
            'project': project,
            'team': team,
            'days_before': days_before
        }
    )


def notify_defense_result(defense):
    """
    Notification du résultat après notation complète.
    
    Args:
        defense: Instance de Defense
    """
    project = defense.project
    team = project.team
    
    # Calculer la note finale
    final_grade = defense.calculate_final_grade() if hasattr(defense, 'calculate_final_grade') else defense.final_grade
    
    # Étudiants
    students_emails = [team.student1.email]
    if team.student2:
        students_emails.append(team.student2.email)
    
    send_notification_email(
        recipients=students_emails,
        subject=f"Résultat de soutenance - Note finale : {final_grade}/20",
        template='emails/defense_result.html',
        context={
            'defense': defense,
            'project': project,
            'team': team,
            'final_grade': final_grade
        }
    )


# Fonctions pour actions importantes

def notify_new_subject(subject):
    """Notification aux admins lors d'un nouveau sujet."""
    from users.models import User
    admins = User.objects.filter(role='admin')
    
    send_notification_email(
        recipients=[admin.email for admin in admins],
        subject="Nouveau sujet proposé",
        template='emails/new_subject.html',
        context={'subject': subject}
    )


def notify_subject_validated(subject):
    """Notification au superviseur quand son sujet est validé."""
    send_notification_email(
        recipients=[subject.supervisor.email],
        subject="Votre sujet a été validé",
        template='emails/subject_validated.html',
        context={'subject': subject}
    )


def notify_assignment(assignment):
    """Notification lors d'une affectation de sujet."""
    send_notification_email(
        recipients=[
            assignment.student.email,
            assignment.subject.supervisor.email
        ],
        subject=f"Affectation de sujet - {assignment.subject.title}",
        template='emails/new_assignment.html',
        context={'assignment': assignment}
    )


def notify_milestone_validated(milestone):
    """Notification quand un jalon est validé."""
    project = milestone.project
    team = project.team
    
    send_notification_email(
        recipients=[team.student1.email] + ([team.student2.email] if team.student2 else []),
        subject=f"Jalon validé - {milestone.title}",
        template='emails/milestone_validated.html',
        context={'milestone': milestone, 'project': project}
    )


def notify_milestone_rejected(milestone):
    """Notification quand un jalon est rejeté."""
    project = milestone.project
    team = project.team
    
    send_notification_email(
        recipients=[team.student1.email] + ([team.student2.email] if team.student2 else []),
        subject=f"Jalon à revoir - {milestone.title}",
        template='emails/milestone_rejected.html',
        context={'milestone': milestone, 'project': project}
    )
