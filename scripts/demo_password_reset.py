"""
Script de démonstration du système de réinitialisation de mot de passe
Exécutez: python manage.py shell < scripts/demo_password_reset.py
"""

import os
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from users.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

print("\n" + "="*80)
print("DÉMONSTRATION - SYSTÈME DE RÉINITIALISATION DE MOT DE PASSE")
print("="*80)

# Vérifier s'il y a des utilisateurs
users = User.objects.all()
if not users.exists():
    print("\n❌ Aucun utilisateur dans la base de données.")
    print("   Créez d'abord un compte via l'interface d'inscription.")
    print("\n" + "="*80 + "\n")
    exit()

print(f"\n📊 Utilisateurs disponibles dans la base de données:")
print("-"*80)
for idx, user in enumerate(users, 1):
    print(f"{idx}. {user.username} - {user.email} ({user.get_role_display()})")

print("\n" + "-"*80)
choice = input("\nChoisissez un utilisateur (numéro) ou 'q' pour quitter: ").strip()

if choice.lower() == 'q':
    print("\n👋 Au revoir!\n")
    exit()

try:
    user_idx = int(choice) - 1
    if user_idx < 0 or user_idx >= len(users):
        print("\n❌ Choix invalide.")
        exit()
    
    user = list(users)[user_idx]
    
    print(f"\n✅ Utilisateur sélectionné: {user.username} ({user.email})")
    print("\n" + "="*80)
    print("GÉNÉRATION DU LIEN DE RÉINITIALISATION")
    print("="*80)
    
    # Générer le token
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    
    print(f"\n🔑 Token généré: {token[:20]}...")
    print(f"🆔 UID: {uid}")
    
    # Créer le contexte pour l'email
    context = {
        "email": user.email,
        'domain': 'localhost:8000',
        'site_name': 'GradEase',
        "uid": uid,
        "user": user,
        'token': token,
        'protocol': 'http',
    }
    
    # Générer le lien
    reset_link = f"http://localhost:8000/users/password-reset-confirm/{uid}/{token}/"
    print(f"\n🔗 Lien de réinitialisation:\n   {reset_link}")
    
    print("\n" + "="*80)
    print("ENVOI DE L'EMAIL")
    print("="*80)
    
    # Créer l'email
    subject = "Réinitialisation de mot de passe - GradEase"
    text_content = render_to_string("users/password_reset_email.txt", context)
    html_content = render_to_string("users/password_reset_email.html", context)
    
    try:
        email = EmailMultiAlternatives(
            subject,
            text_content,
            settings.DEFAULT_FROM_EMAIL,
            [user.email]
        )
        email.attach_alternative(html_content, "text/html")
        email.send(fail_silently=False)
        
        print(f"\n✅ Email envoyé à: {user.email}")
        print(f"   Backend utilisé: {settings.EMAIL_BACKEND}")
        
        if 'console' in settings.EMAIL_BACKEND:
            print("\n📧 MODE CONSOLE ACTIVÉ")
            print("   L'email s'affiche ci-dessus dans la console.")
            print("   En production avec Gmail, il sera envoyé réellement.")
        
        print("\n" + "="*80)
        print("INSTRUCTIONS POUR TESTER")
        print("="*80)
        print("\n1. Copiez le lien de réinitialisation ci-dessus")
        print("2. Ouvrez-le dans votre navigateur")
        print("3. Définissez un nouveau mot de passe")
        print("4. Connectez-vous avec le nouveau mot de passe")
        
        print("\n💡 CONSEIL: Le lien expire après 1 heure.")
        
    except Exception as e:
        print(f"\n❌ Erreur lors de l'envoi: {e}")
        import traceback
        print(traceback.format_exc())

except ValueError:
    print("\n❌ Veuillez entrer un numéro valide.")
except Exception as e:
    print(f"\n❌ Erreur: {e}")
    import traceback
    print(traceback.format_exc())

print("\n" + "="*80 + "\n")
