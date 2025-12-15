"""
Signaux Django pour automatiser les interactions entre rôles
"""
from django.db.models.signals import post_save, pre_save, pre_delete
from django.dispatch import receiver
from django.utils import timezone

from subjects.models import Application, Assignment
from projects.models import Project, Milestone, Deliverable
from defenses.models import Defense, DefenseChangeRequest, JuryMember
from communications.models import Notification, Message


@receiver(post_save, sender=Application)
def handle_application_notification(sender, instance, created, **kwargs):
    """Notifier l'encadreur quand un étudiant candidate"""
    if created:
        # Notification à l'encadreur
        Notification.objects.create(
            user=instance.subject.supervisor,
            type='application',
            title='Nouvelle candidature',
            message=f"{instance.student.get_full_name()} a candidaté au sujet '{instance.subject.title}'.",
            link=f"/subjects/{instance.subject.pk}/applications/"
        )


@receiver(post_save, sender=Application)
def handle_application_review_notification(sender, instance, created, **kwargs):
    """Notifier l'étudiant du résultat de sa candidature"""
    if not created and instance.status in ['accepted', 'rejected']:
        if instance.status == 'accepted':
            reviewer_name = instance.reviewed_by.get_full_name() if instance.reviewed_by else "l'administration"
            message = f"Votre candidature au sujet '{instance.subject.title}' a été acceptée par {reviewer_name}."
            notif_type = 'application_status'
        else:
            message = f"Votre candidature au sujet '{instance.subject.title}' a été rejetée."
            notif_type = 'application_status'
        
        Notification.objects.create(
            user=instance.student,
            type=notif_type,
            title='Réponse à votre candidature',
            message=message,
            link=f"/subjects/my-applications/"
        )


@receiver(post_save, sender=Assignment)
def handle_assignment_creation(sender, instance, created, **kwargs):
    """Actions automatiques après affectation d'un sujet"""
    if created:
        # 1. Notification à l'étudiant
        Notification.objects.create(
            user=instance.student,
            type='project',
            title='Sujet affecté!',
            message=f"Le sujet '{instance.subject.title}' vous a été affecté. Vous pouvez maintenant créer votre projet.",
            link=f"/subjects/{instance.subject.pk}/"
        )
        
        # 2. Notification à l'encadreur
        Notification.objects.create(
            user=instance.subject.supervisor,
            type='project',
            title='Nouveau projet à encadrer',
            message=f"L'étudiant {instance.student.get_full_name()} vous a été affecté pour le sujet '{instance.subject.title}'.",
            link=f"/subjects/{instance.subject.pk}/"
        )
        
        # 3. Créer automatiquement le projet avec statut "awaiting_kickoff"
        if not hasattr(instance, 'project'):
            Project.objects.create(
                assignment=instance,
                title=instance.subject.title,
                description=instance.subject.description,
                objectives=instance.subject.description,
                status='awaiting_kickoff'  # En attente de réunion de cadrage
            )


@receiver(post_save, sender='subjects.StudentProposal')
def handle_student_proposal(sender, instance, created, **kwargs):
    """Actions automatiques pour les propositions d'étudiants"""
    from subjects.models import StudentProposal, Subject, Assignment
    
    if created:
        # Notifier les encadreurs choisis
        for supervisor in instance.get_preferred_supervisors():
            Notification.objects.create(
                user=supervisor,
                type='proposal',
                title='Nouvelle proposition d\'étudiant',
                message=f"{instance.student.get_full_name()} vous propose d'encadrer son projet: {instance.title}",
                link=f"/subjects/proposals/"
            )
    
    elif instance.status == 'accepted' and instance.accepted_by:
        # Créer un sujet basé sur la proposition
        subject = Subject.objects.create(
            title=instance.title,
            description=instance.description,
            objectives=instance.objectives,
            domain=instance.domain,
            type=instance.type,
            level=instance.student.level,
            supervisor=instance.accepted_by,
            status='assigned',
            keywords=instance.technologies
        )
        
        # Créer l'affectation automatiquement
        assignment = Assignment.objects.create(
            subject=subject,
            student=instance.student,
            status='accepted'
        )
        
        # Notifier l'étudiant
        Notification.objects.create(
            user=instance.student,
            type='proposal',
            title='Proposition acceptée!',
            message=f"Votre proposition '{instance.title}' a été acceptée par {instance.accepted_by.get_full_name()}. Votre projet a été créé.",
            link=f"/projects/"
        )


@receiver(post_save, sender=Milestone)
def handle_milestone_notification(sender, instance, created, **kwargs):
    """Notifier l'encadreur quand un jalon est ajouté/modifié"""
    if created:
        Notification.objects.create(
            user=instance.project.assignment.subject.supervisor,
            type='milestone',
            title='Nouveau jalon ajouté',
            message=f"{instance.project.assignment.student.get_full_name()} a ajouté un jalon: {instance.title}",
            link=f"/projects/{instance.project.pk}/"
        )


@receiver(post_save, sender=Deliverable)
def handle_deliverable_notification(sender, instance, created, **kwargs):
    """Notifier l'encadreur quand un livrable est déposé"""
    if created:
        Notification.objects.create(
            user=instance.project.assignment.subject.supervisor,
            type='deliverable',
            title='Nouveau livrable',
            message=f"{instance.project.assignment.student.get_full_name()} a déposé: {instance.title}",
            link=f"/projects/{instance.project.pk}/"
        )


@receiver(post_save, sender=Defense)
def handle_defense_notification(sender, instance, created, **kwargs):
    """Notifier toutes les parties concernées lors de la planification d'une soutenance"""
    if created:
        # Notification à l'étudiant
        Notification.objects.create(
            user=instance.project.assignment.student,
            type='defense',
            title='Soutenance planifiée',
            message=f"Votre soutenance a été planifiée le {instance.date.strftime('%d/%m/%Y')} à {instance.time.strftime('%H:%M')} en salle {instance.room}.",
            link=f"/defenses/{instance.pk}/"
        )
        
        # Notification à l'encadreur
        Notification.objects.create(
            user=instance.project.assignment.subject.supervisor,
            type='defense',
            title='Soutenance planifiée',
            message=f"Soutenance de {instance.project.assignment.student.get_full_name()} planifiée le {instance.date.strftime('%d/%m/%Y')} à {instance.time.strftime('%H:%M')}.",
            link=f"/defenses/{instance.pk}/"
        )


@receiver(post_save, sender=JuryMember)
def handle_jury_member_notification(sender, instance, created, **kwargs):
    """Notifier les membres du jury quand ils sont ajoutés"""
    if created:
        Notification.objects.create(
            user=instance.user,
            type='defense',
            title='Invitation au jury',
            message=f"Vous avez été désigné comme {instance.get_role_display()} pour la soutenance de {instance.defense.project.assignment.student.get_full_name()} le {instance.defense.date.strftime('%d/%m/%Y')}.",
            link=f"/defenses/{instance.defense.pk}/"
        )


@receiver(post_save, sender=DefenseChangeRequest)
def handle_defense_change_request_notification(sender, instance, created, **kwargs):
    """Notifier l'admin des demandes de modification"""
    if created:
        # Notifier tous les admins
        from users.models import User
        admins = User.objects.filter(role='admin')
        for admin in admins:
            Notification.objects.create(
                user=admin,
                type='defense',
                title='Demande de modification de soutenance',
                message=f"{instance.requested_by.get_full_name()} demande une modification pour la soutenance du {instance.defense.date.strftime('%d/%m/%Y')}.",
                link=f"/defenses/change-requests/{instance.pk}/review/"
            )
    
    # Notifier le demandeur du résultat
    elif instance.status in ['approved', 'rejected']:
        if instance.status == 'approved':
            message = "Votre demande de modification a été approuvée."
        else:
            message = f"Votre demande de modification a été rejetée. Raison: {instance.review_comment}"
        
        Notification.objects.create(
            user=instance.requested_by,
            type='defense',
            title='Réponse à votre demande',
            message=message,
            link=f"/defenses/{instance.defense.pk}/"
        )
        
        # Si approuvé, notifier toutes les parties
        if instance.status == 'approved':
            # Notifier l'étudiant
            Notification.objects.create(
                user=instance.defense.project.assignment.student,
                type='defense',
                title='Modification de soutenance',
                message=f"Votre soutenance a été reprogrammée au {instance.defense.date.strftime('%d/%m/%Y')} à {instance.defense.time.strftime('%H:%M')}.",
                link=f"/defenses/{instance.defense.pk}/"
            )
            
            # Notifier l'encadreur si ce n'est pas lui qui a demandé
            if instance.requested_by != instance.defense.project.assignment.subject.supervisor:
                Notification.objects.create(
                    user=instance.defense.project.assignment.subject.supervisor,
                    type='defense',
                    title='Modification de soutenance',
                    message=f"La soutenance de {instance.defense.project.assignment.student.get_full_name()} a été reprogrammée au {instance.defense.date.strftime('%d/%m/%Y')}.",
                    link=f"/defenses/{instance.defense.pk}/"
                )
            
            # Notifier les membres du jury
            for jury_member in instance.defense.jury_members.all():
                Notification.objects.create(
                    user=jury_member.user,
                    type='defense',
                    title='Modification de soutenance',
                    message=f"La soutenance a été reprogrammée au {instance.defense.date.strftime('%d/%m/%Y')} à {instance.defense.time.strftime('%H:%M')}.",
                    link=f"/defenses/{instance.defense.pk}/"
                )


@receiver(post_save, sender=Deliverable)
def handle_deliverable_review_notification(sender, instance, created, **kwargs):
    """Notifier l'étudiant quand un livrable est validé/rejeté par l'encadreur"""
    if not created and instance.status in ['approved', 'rejected']:
        if instance.status == 'approved':
            message = f"Votre livrable '{instance.title}' a été approuvé par {instance.reviewed_by.get_full_name()}."
            if instance.review_comments:
                message += f"\nCommentaire: {instance.review_comments}"
        else:
            message = f"Votre livrable '{instance.title}' a été rejeté."
            if instance.review_comments:
                message += f"\nRaison: {instance.review_comments}"
        
        Notification.objects.create(
            user=instance.submitted_by,
            type='deliverable',
            title='Évaluation de livrable',
            message=message,
            link=f"/projects/{instance.project.pk}/"
        )


@receiver(post_save, sender=Milestone)
def handle_milestone_status_change_notification(sender, instance, created, **kwargs):
    """Notifier l'encadreur quand un jalon change de statut"""
    if not created and instance.status == 'completed':
        Notification.objects.create(
            user=instance.project.assignment.subject.supervisor,
            type='milestone',
            title='Jalon complété',
            message=f"{instance.project.assignment.student.get_full_name()} a marqué le jalon '{instance.title}' comme complété.",
            link=f"/projects/{instance.project.pk}/"
        )


@receiver(post_save, sender=Project)
def handle_project_status_change_notification(sender, instance, created, **kwargs):
    """Notifier les parties prenantes quand le statut d'un projet change"""
    if not created and instance.status in ['submitted', 'under_review', 'approved', 'rejected', 'completed']:
        # Notifier l'encadreur sauf si c'est lui qui a changé le statut
        if instance.status == 'submitted':
            Notification.objects.create(
                user=instance.assignment.subject.supervisor,
                type='project',
                title='Projet soumis',
                message=f"{instance.assignment.student.get_full_name()} a soumis le projet '{instance.title}' pour révision.",
                link=f"/projects/{instance.pk}/"
            )
        
        # Notifier l'étudiant pour les changements de statut importants
        elif instance.status in ['approved', 'rejected', 'completed']:
            if instance.status == 'approved':
                message = f"Votre projet '{instance.title}' a été approuvé par votre encadreur."
            elif instance.status == 'rejected':
                message = f"Votre projet '{instance.title}' nécessite des révisions."
            else:
                message = f"Votre projet '{instance.title}' est marqué comme terminé."
            
            if instance.supervisor_notes:
                message += f"\nNote de l'encadreur: {instance.supervisor_notes}"
            
            Notification.objects.create(
                user=instance.assignment.student,
                type='project',
                title='Mise à jour du projet',
                message=message,
                link=f"/projects/{instance.pk}/"
            )


@receiver(pre_delete, sender=JuryMember)
def handle_jury_member_removal_notification(sender, instance, **kwargs):
    """Notifier un membre du jury quand il est retiré d'une soutenance"""
    Notification.objects.create(
        user=instance.user,
        type='defense',
        title='Retrait du jury',
        message=f"Vous avez été retiré du jury de la soutenance de {instance.defense.project.assignment.student.get_full_name()} prévue le {instance.defense.date.strftime('%d/%m/%Y')}.",
        link=f"/defenses/"
    )


@receiver(post_save, sender=Message)
def handle_new_message_notification(sender, instance, created, **kwargs):
    """Notifier le destinataire quand il reçoit un nouveau message"""
    if created:
        Notification.objects.create(
            user=instance.recipient,
            type='message',
            title='Nouveau message',
            message=f"{instance.sender.get_full_name()} vous a envoyé un message: \"{instance.subject}\"",
            link=f"/communications/messages/{instance.pk}/"
        )


@receiver(pre_delete, sender=Assignment)
def handle_assignment_cancellation_notification(sender, instance, **kwargs):
    """Notifier l'étudiant et l'encadreur en cas d'annulation d'affectation"""
    # Notifier l'étudiant
    Notification.objects.create(
        user=instance.student,
        type='project',
        title='Affectation annulée',
        message=f"Votre affectation au sujet '{instance.subject.title}' a été annulée.",
        link=f"/subjects/"
    )
    
    # Notifier l'encadreur
    Notification.objects.create(
        user=instance.subject.supervisor,
        type='project',
        title='Affectation annulée',
        message=f"L'affectation de {instance.student.get_full_name()} au sujet '{instance.subject.title}' a été annulée.",
        link=f"/subjects/"
    )


@receiver(pre_delete, sender=Defense)
def handle_defense_cancellation_notification(sender, instance, **kwargs):
    """Notifier toutes les parties en cas d'annulation de soutenance"""
    # Notifier l'étudiant
    Notification.objects.create(
        user=instance.project.assignment.student,
        type='defense',
        title='Soutenance annulée',
        message=f"La soutenance prévue le {instance.date.strftime('%d/%m/%Y')} à {instance.time.strftime('%H:%M')} a été annulée.",
        link=f"/defenses/"
    )
    
    # Notifier l'encadreur
    Notification.objects.create(
        user=instance.project.assignment.subject.supervisor,
        type='defense',
        title='Soutenance annulée',
        message=f"La soutenance de {instance.project.assignment.student.get_full_name()} prévue le {instance.date.strftime('%d/%m/%Y')} a été annulée.",
        link=f"/defenses/"
    )
    
    # Notifier tous les membres du jury
    for jury_member in instance.jury_members.all():
        Notification.objects.create(
            user=jury_member.user,
            type='defense',
            title='Soutenance annulée',
            message=f"La soutenance prévue le {instance.date.strftime('%d/%m/%Y')} à {instance.time.strftime('%H:%M')} a été annulée.",
            link=f"/defenses/"
        )
