"""
Script de test pour la configuration email
Exécutez: python manage.py shell < test_email.py
"""

from django.core.mail import send_mail
from django.conf import settings

print("\n" + "="*80)
print("TEST DE CONFIGURATION EMAIL")
print("="*80)

print(f"\nBackend Email: {settings.EMAIL_BACKEND}")
print(f"Host: {getattr(settings, 'EMAIL_HOST', 'Non configuré')}")
print(f"Port: {getattr(settings, 'EMAIL_PORT', 'Non configuré')}")
print(f"Use TLS: {getattr(settings, 'EMAIL_USE_TLS', 'Non configuré')}")
print(f"From Email: {settings.DEFAULT_FROM_EMAIL}")

# Test si Gmail est configuré
if hasattr(settings, 'EMAIL_HOST_USER'):
    print(f"Email User: {settings.EMAIL_HOST_USER}")
    print(f"Password configuré: {'Oui' if settings.EMAIL_HOST_PASSWORD else 'Non'}")
else:
    print("Email User: Non configuré")

print("\n" + "-"*80)
print("Test d'envoi d'email...")
print("-"*80)

try:
    # Remplacez par votre email pour tester
    test_email = input("\nEntrez votre adresse email pour le test: ").strip()
    
    if test_email:
        send_mail(
            'Test - Configuration Email GradEase',
            'Ceci est un email de test. Si vous recevez ce message, la configuration email fonctionne correctement !',
            settings.DEFAULT_FROM_EMAIL,
            [test_email],
            fail_silently=False,
        )
        print(f"\n✅ Email de test envoyé à {test_email}")
        print("\nVérifiez votre boîte de réception (et le dossier spam).")
    else:
        print("\n❌ Aucune adresse email fournie.")
        
except Exception as e:
    print(f"\n❌ Erreur: {e}")
    print(f"\nType d'erreur: {type(e).__name__}")
    import traceback
    print("\nDétails de l'erreur:")
    print(traceback.format_exc())

print("\n" + "="*80)
print("FIN DU TEST")
print("="*80 + "\n")
