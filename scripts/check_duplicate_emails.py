"""
Script pour détecter les emails en doublon dans la base de données
Exécutez: python manage.py shell < scripts/check_duplicate_emails.py
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from users.models import User
from django.db.models import Count

print("\n" + "="*80)
print("VÉRIFICATION DES EMAILS EN DOUBLON")
print("="*80)

# Compter le nombre total d'utilisateurs
total_users = User.objects.count()
print(f"\n📊 Nombre total d'utilisateurs: {total_users}")

# Trouver les emails en doublon
duplicates = User.objects.values('email').annotate(
    count=Count('email')
).filter(count__gt=1).order_by('-count')

if not duplicates:
    print("\n✅ Aucun email en doublon trouvé!")
    print("   Tous les utilisateurs ont des emails uniques.")
else:
    print(f"\n⚠️  {len(duplicates)} email(s) partagé(s) par plusieurs comptes:")
    print("-"*80)
    
    total_affected = 0
    for dup in duplicates:
        email = dup['email']
        count = dup['count']
        total_affected += count
        
        print(f"\n📧 Email: {email or '(vide)'}")
        print(f"   Utilisé par {count} comptes:")
        
        # Afficher les détails de chaque compte
        users = User.objects.filter(email=email)
        for idx, user in enumerate(users, 1):
            print(f"   {idx}. {user.username:20} - {user.get_full_name():30} - {user.get_role_display()}")
    
    print("\n" + "-"*80)
    print(f"📈 Statistiques:")
    print(f"   - Utilisateurs affectés: {total_affected}/{total_users}")
    print(f"   - Emails en doublon: {len(duplicates)}")
    print(f"   - Utilisateurs avec email unique: {total_users - total_affected}")

print("\n" + "="*80)
print("RECOMMANDATIONS")
print("="*80)

if duplicates:
    print("""
⚠️  ACTIONS RECOMMANDÉES:

1. COURT TERME (Déjà implémenté ✅)
   - Le système de réinitialisation gère les doublons
   - Chaque compte reçoit son propre lien de réinitialisation
   - Les emails indiquent clairement quel compte est concerné

2. MOYEN TERME
   - Contacter les utilisateurs concernés
   - Leur demander d'utiliser des emails différents
   - Mettre à jour leurs profils

3. LONG TERME
   - Ajouter une contrainte unique sur le champ email
   - Empêcher la création de nouveaux doublons
   - Modifier le formulaire d'inscription

COMMANDES UTILES:

# Pour voir les détails d'un email spécifique
python manage.py shell
>>> from users.models import User
>>> User.objects.filter(email='email@example.com')

# Pour mettre à jour un email
>>> user = User.objects.get(username='nom_utilisateur')
>>> user.email = 'nouvel.email@example.com'
>>> user.save()
""")
else:
    print("""
✅ EXCELLENTE NOUVELLE!

Aucun email en doublon détecté. Vous pouvez maintenant:

1. Ajouter une contrainte unique sur le champ email (recommandé)
2. Empêcher les futurs doublons au niveau de la base de données
3. Simplifier la logique de réinitialisation si nécessaire

POUR AJOUTER LA CONTRAINTE UNIQUE:

1. Modifiez users/models.py:
   email = models.EmailField(unique=True)

2. Créez et appliquez la migration:
   python manage.py makemigrations
   python manage.py migrate
""")

print("\n" + "="*80 + "\n")
