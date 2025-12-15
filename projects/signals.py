# projects/signals.py
# Signaux pour automatiser les actions sur les projets

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Milestone, Project


@receiver(post_save, sender=Milestone)
def update_project_progress_on_milestone_change(sender, instance, created, **kwargs):
    """
    Met à jour automatiquement la progression du projet quand un jalon est modifié.
    Se déclenche après la sauvegarde d'un jalon.
    """
    project = instance.project
    
    # Recalculer et mettre à jour le pourcentage
    project.update_progress_from_milestones()


@receiver(pre_save, sender=Milestone)
def notify_on_milestone_validation(sender, instance, **kwargs):
    """
    Envoie une notification quand un jalon est validé ou rejeté.
    """
    if instance.pk:
        # C'est une modification, pas une création
        try:
            old_instance = Milestone.objects.get(pk=instance.pk)
            
            # Vérifier si le statut de validation a changé
            if old_instance.validated_by_supervisor != instance.validated_by_supervisor:
                # Import ici pour éviter les imports circulaires
                from communications.email_utils import notify_milestone_validated, notify_milestone_rejected
                
                if instance.validated_by_supervisor:
                    # Jalon validé
                    notify_milestone_validated(instance)
                else:
                    # Jalon rejeté ou non validé
                    if old_instance.validated_by_supervisor:
                        notify_milestone_rejected(instance)
        
        except Milestone.DoesNotExist:
            pass
