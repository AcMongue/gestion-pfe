#!/usr/bin/env python
"""Script simple pour tester la communication"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from users.models import User
from communications.models import Message, Notification

print("🧪 TEST DE COMMUNICATION\n" + "="*50)

# Vérifier les utilisateurs
users = User.objects.all()
print(f"\n📊 {users.count()} utilisateurs dans la base:")
for u in users[:10]:
    print(f"   - {u.email} ({u.get_full_name()}) - {u.role}")

if users.count() >= 2:
    sender = users[0]
    recipient = users[1]
    
    print(f"\n📧 Création d'un message test:")
    print(f"   De: {sender.get_full_name()} ({sender.email})")
    print(f"   À: {recipient.get_full_name()} ({recipient.email})")
    
    # Créer un message
    message = Message.objects.create(
        sender=sender,
        recipient=recipient,
        subject="Test de communication",
        content="Ceci est un message de test pour vérifier que la communication fonctionne."
    )
    
    print(f"   ✅ Message créé: ID={message.pk}")
    
    # Créer une notification
    notif = Notification.objects.create(
        user=recipient,
        type='message',
        title='Nouveau message',
        message=f"{sender.get_full_name()} vous a envoyé un message",
        link=f'/communications/message/{message.pk}/'
    )
    
    print(f"   ✅ Notification créée: ID={notif.pk}")
    
    # Statistiques
    total_messages = Message.objects.count()
    total_notifs = Notification.objects.count()
    
    print(f"\n📊 STATISTIQUES:")
    print(f"   Total messages: {total_messages}")
    print(f"   Total notifications: {total_notifs}")
    
    print(f"\n✅ COMMUNICATION: FONCTIONNELLE")
    print("\n💡 Pour tester dans le navigateur:")
    print(f"   1. Connectez-vous en tant que: {recipient.email}")
    print(f"   2. Allez dans: http://127.0.0.1:8000/communications/inbox/")
    print(f"   3. Vous devriez voir le message de {sender.get_full_name()}")
else:
    print("❌ Pas assez d'utilisateurs. Exécutez create_test_data.py d'abord.")
