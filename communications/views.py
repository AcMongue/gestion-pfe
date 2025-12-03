from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Message, Notification
from .forms import MessageForm, ReplyForm

@login_required
def inbox_view(request):
    """Afficher la boîte de réception"""
    received_messages = Message.objects.filter(
        recipient=request.user
    ).order_by('-created_at')
    
    # Marquer les notifications comme lues
    Notification.objects.filter(
        user=request.user,
        type='message',
        is_read=False
    ).update(is_read=True)
    
    context = {
        'messages': received_messages,
        'unread_count': received_messages.filter(is_read=False).count(),
    }
    return render(request, 'communications/inbox.html', context)


@login_required
def sent_messages_view(request):
    """Afficher les messages envoyés"""
    sent_messages = Message.objects.filter(
        sender=request.user
    ).order_by('-created_at')
    
    context = {
        'messages': sent_messages,
    }
    return render(request, 'communications/sent.html', context)


@login_required
def message_detail_view(request, pk):
    """Afficher les détails d'un message"""
    message = get_object_or_404(Message, pk=pk)
    
    # Vérifier que l'utilisateur est autorisé à voir ce message
    if message.recipient != request.user and message.sender != request.user:
        messages.error(request, "Vous n'êtes pas autorisé à voir ce message.")
        return redirect('communications:inbox')
    
    # Marquer comme lu si c'est le destinataire
    if message.recipient == request.user and not message.is_read:
        message.is_read = True
        message.save()
    
    # Gérer la réponse
    if request.method == 'POST':
        form = ReplyForm(request.POST, request.FILES)
        if form.is_valid():
            # Créer un nouveau message en réponse
            reply = Message.objects.create(
                sender=request.user,
                recipient=message.sender if message.recipient == request.user else message.recipient,
                subject=f"Re: {message.subject}",
                content=form.cleaned_data['content'],
                attachment=form.cleaned_data.get('attachment'),
                parent=message
            )
            messages.success(request, "Réponse envoyée avec succès.")
            return redirect('communications:message_detail', pk=message.pk)
    else:
        form = ReplyForm()
    
    # Récupérer les réponses
    replies = Message.objects.filter(parent=message).order_by('created_at')
    
    context = {
        'message': message,
        'replies': replies,
        'reply_form': form,
    }
    return render(request, 'communications/message_detail.html', context)


@login_required
def compose_message_view(request):
    """Composer un nouveau message"""
    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.save()
            
            # Créer une notification pour le destinataire
            Notification.objects.create(
                user=message.recipient,
                type='message',
                title='Nouveau message',
                message=f"{message.sender.get_full_name()} vous a envoyé un message : {message.subject}",
                link=f'/communications/message/{message.pk}/'
            )
            
            messages.success(request, "Message envoyé avec succès.")
            return redirect('communications:sent')
    else:
        # Pré-remplir le destinataire si spécifié dans l'URL
        recipient_id = request.GET.get('to')
        initial = {}
        if recipient_id:
            from users.models import User
            try:
                recipient = User.objects.get(pk=recipient_id)
                initial['recipient'] = recipient
            except User.DoesNotExist:
                pass
        
        form = MessageForm(user=request.user, initial=initial)
    
    context = {
        'form': form,
    }
    return render(request, 'communications/compose.html', context)


@login_required
def delete_message_view(request, pk):
    """Supprimer un message"""
    message = get_object_or_404(Message, pk=pk)
    
    # Seul le destinataire ou l'expéditeur peut supprimer
    if message.recipient != request.user and message.sender != request.user:
        messages.error(request, "Vous n'êtes pas autorisé à supprimer ce message.")
        return redirect('communications:inbox')
    
    message.delete()
    messages.success(request, "Message supprimé.")
    return redirect('communications:inbox')


@login_required
def notifications_view(request):
    """Afficher toutes les notifications"""
    user_notifications = Notification.objects.filter(
        user=request.user
    ).order_by('-created_at')
    
    context = {
        'notifications': user_notifications,
        'unread_count': user_notifications.filter(is_read=False).count(),
    }
    return render(request, 'communications/notifications.html', context)


@login_required
def mark_notification_read_view(request, pk):
    """Marquer une notification comme lue"""
    notification = get_object_or_404(Notification, pk=pk, user=request.user)
    notification.is_read = True
    notification.save()
    
    if notification.link:
        return redirect(notification.link)
    return redirect('communications:notifications')


@login_required
def mark_all_notifications_read_view(request):
    """Marquer toutes les notifications comme lues"""
    Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
    messages.success(request, "Toutes les notifications ont été marquées comme lues.")
    return redirect('communications:notifications')
