#!/usr/bin/env python
"""Script de test complet pour vérifier communication et planification"""
import os
import django
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.utils import timezone
from users.models import User
from projects.models import Project
from defenses.models import Defense, JuryMember
from communications.models import Message, Notification

def test_communications():
    """Tester la fonctionnalité de communication"""
    print("\n" + "="*60)
    print("TEST 1: COMMUNICATION")
    print("="*60)
    
    # Récupérer des utilisateurs
    try:
        alice = User.objects.get(email='alice@enspd.cm')
        encadreur = User.objects.get(email='encadreur1@enspd.cm')
        print(f"✓ Utilisateurs trouvés: {alice.get_full_name()}, {encadreur.get_full_name()}")
    except User.DoesNotExist:
        print("✗ Erreur: Utilisateurs non trouvés")
        return False
    
    # Test 1: Créer un message
    try:
        message = Message.objects.create(
            sender=alice,
            recipient=encadreur,
            subject="Question sur le projet",
            content="Bonjour, j'ai une question concernant le jalon à rendre..."
        )
        print(f"✓ Message créé: ID={message.pk}")
    except Exception as e:
        print(f"✗ Erreur création message: {e}")
        return False
    
    # Test 2: Créer une notification
    try:
        notif = Notification.objects.create(
            user=encadreur,
            notification_type='message',
            title='Nouveau message',
            message=f"{alice.get_full_name()} vous a envoyé un message",
            link=f'/communications/message/{message.pk}/'
        )
        print(f"✓ Notification créée: ID={notif.pk}")
    except Exception as e:
        print(f"✗ Erreur création notification: {e}")
        return False
    
    # Test 3: Répondre au message
    try:
        reply = Message.objects.create(
            sender=encadreur,
            recipient=alice,
            subject=f"Re: {message.subject}",
            content="Bonjour Alice, bien sûr, posez votre question...",
            parent=message
        )
        print(f"✓ Réponse créée: ID={reply.pk}")
    except Exception as e:
        print(f"✗ Erreur création réponse: {e}")
        return False
    
    # Statistiques
    total_messages = Message.objects.count()
    total_notifs = Notification.objects.count()
    print(f"\n📊 Statistiques:")
    print(f"   Total messages: {total_messages}")
    print(f"   Total notifications: {total_notifs}")
    
    return True


def test_defense_planning():
    """Tester la planification des soutenances"""
    print("\n" + "="*60)
    print("TEST 2: PLANIFICATION DE SOUTENANCE")
    print("="*60)
    
    # Récupérer un projet sans soutenance
    try:
        project = Project.objects.filter(defense__isnull=True).first()
        if not project:
            print("✗ Aucun projet disponible pour planification")
            return False
        print(f"✓ Projet sélectionné: {project.title} (ID={project.pk})")
    except Exception as e:
        print(f"✗ Erreur récupération projet: {e}")
        return False
    
    # Test 1: Créer une soutenance
    try:
        defense_date = timezone.now().date() + timedelta(days=30)
        defense_time = timezone.now().time().replace(hour=10, minute=0, second=0, microsecond=0)
        
        defense = Defense.objects.create(
            project=project,
            date=defense_date,
            time=defense_time,
            room="A101",
            duration=45,
            status='scheduled'
        )
        print(f"✓ Soutenance créée: ID={defense.pk}")
        print(f"   Date: {defense.date.strftime('%d/%m/%Y')}")
        print(f"   Heure: {defense.time.strftime('%H:%M')}")
        print(f"   Salle: {defense.room}")
        print(f"   Durée: {defense.duration} minutes")
    except Exception as e:
        print(f"✗ Erreur création soutenance: {e}")
        return False
    
    # Test 2: Ajouter des membres du jury
    try:
        jury1 = User.objects.filter(role='jury').first()
        jury2 = User.objects.filter(role='supervisor').first()
        
        if jury1:
            member1 = JuryMember.objects.create(
                defense=defense,
                user=jury1,
                role='president'
            )
            print(f"✓ Président du jury ajouté: {jury1.get_full_name()}")
        
        if jury2:
            member2 = JuryMember.objects.create(
                defense=defense,
                user=jury2,
                role='member'
            )
            print(f"✓ Membre du jury ajouté: {jury2.get_full_name()}")
    except Exception as e:
        print(f"✗ Erreur ajout jury: {e}")
        return False
    
    # Statistiques
    total_defenses = Defense.objects.count()
    total_jury = JuryMember.objects.count()
    print(f"\n📊 Statistiques:")
    print(f"   Total soutenances: {total_defenses}")
    print(f"   Total membres jury: {total_jury}")
    
    return True


def test_urls():
    """Tester l'accessibilité des URLs"""
    print("\n" + "="*60)
    print("TEST 3: ACCESSIBILITÉ DES URLs")
    print("="*60)
    
    from django.test import Client
    client = Client()
    
    urls_to_test = [
        ('/', 'Page d\'accueil'),
        ('/accounts/login/', 'Connexion'),
        ('/subjects/', 'Catalogue sujets'),
        ('/projects/', 'Liste projets'),
        ('/defenses/', 'Liste soutenances'),
        ('/defenses/calendar/', 'Calendrier soutenances'),
        ('/communications/inbox/', 'Boîte de réception'),
        ('/archives/', 'Archives'),
    ]
    
    results = []
    for url, name in urls_to_test:
        try:
            response = client.get(url, follow=True)
            status = "✓" if response.status_code in [200, 302] else "✗"
            results.append((status, name, response.status_code))
            print(f"{status} {name}: HTTP {response.status_code}")
        except Exception as e:
            print(f"✗ {name}: ERREUR - {e}")
            results.append(("✗", name, str(e)))
    
    success = all(r[0] == "✓" for r in results)
    return success


def main():
    """Fonction principale"""
    print("\n" + "🧪 " + "="*58)
    print("   TESTS COMPLETS - COMMUNICATION & PLANIFICATION")
    print("="*60 + "\n")
    
    results = {}
    
    # Test 1: Communication
    results['communication'] = test_communications()
    
    # Test 2: Planification
    results['planification'] = test_defense_planning()
    
    # Test 3: URLs
    results['urls'] = test_urls()
    
    # Résumé
    print("\n" + "="*60)
    print("RÉSUMÉ DES TESTS")
    print("="*60)
    
    for test_name, success in results.items():
        status = "✅ RÉUSSI" if success else "❌ ÉCHOUÉ"
        print(f"{test_name.upper()}: {status}")
    
    all_passed = all(results.values())
    
    print("\n" + "="*60)
    if all_passed:
        print("🎉 TOUS LES TESTS SONT PASSÉS AVEC SUCCÈS!")
        print("✅ Communication: FONCTIONNELLE")
        print("✅ Planification: FONCTIONNELLE")
        print("✅ URLs: ACCESSIBLES")
    else:
        print("⚠️ CERTAINS TESTS ONT ÉCHOUÉ")
        print("Vérifiez les messages d'erreur ci-dessus")
    print("="*60 + "\n")
    
    return all_passed


if __name__ == '__main__':
    success = main()
    exit(0 if success else 1)
