"""
Commande Django pour créer le premier Administrateur Général.

Usage:
    python manage.py create_admin_general

Cette commande doit être exécutée une seule fois lors du déploiement initial
pour créer le premier compte administrateur qui pourra ensuite créer d'autres
administrateurs via l'interface web.
"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import IntegrityError
import getpass

User = get_user_model()


class Command(BaseCommand):
    help = 'Crée le premier Administrateur Général du système'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('=' * 60))
        self.stdout.write(self.style.SUCCESS('   Création du premier Administrateur Général'))
        self.stdout.write(self.style.SUCCESS('=' * 60))
        self.stdout.write('')

        # Vérifier s'il existe déjà des admins généraux
        existing_admins = User.objects.filter(role='admin_general').count()
        if existing_admins > 0:
            self.stdout.write(self.style.WARNING(
                f'⚠️  Il existe déjà {existing_admins} administrateur(s) général(aux).'
            ))
            response = input('Voulez-vous quand même créer un nouvel admin général ? (oui/non) : ')
            if response.lower() not in ['oui', 'o', 'yes', 'y']:
                self.stdout.write(self.style.ERROR('❌ Opération annulée.'))
                return

        self.stdout.write('')
        
        # Collecte des informations
        try:
            first_name = input('Prénom : ').strip()
            if not first_name:
                self.stdout.write(self.style.ERROR('❌ Le prénom est obligatoire.'))
                return

            last_name = input('Nom : ').strip()
            if not last_name:
                self.stdout.write(self.style.ERROR('❌ Le nom est obligatoire.'))
                return

            username = input('Nom d\'utilisateur : ').strip()
            if not username:
                self.stdout.write(self.style.ERROR('❌ Le nom d\'utilisateur est obligatoire.'))
                return

            # Vérifier si le username existe déjà
            if User.objects.filter(username=username).exists():
                self.stdout.write(self.style.ERROR(
                    f'❌ Le nom d\'utilisateur "{username}" existe déjà.'
                ))
                return

            email = input('Email : ').strip()
            if not email:
                self.stdout.write(self.style.ERROR('❌ L\'email est obligatoire.'))
                return

            # Vérifier si l'email existe déjà
            if User.objects.filter(email=email).exists():
                self.stdout.write(self.style.ERROR(
                    f'❌ L\'email "{email}" est déjà utilisé.'
                ))
                return

            # Mot de passe avec confirmation
            while True:
                password = getpass.getpass('Mot de passe : ')
                if len(password) < 8:
                    self.stdout.write(self.style.ERROR(
                        '❌ Le mot de passe doit contenir au moins 8 caractères.'
                    ))
                    continue

                password_confirm = getpass.getpass('Confirmer le mot de passe : ')
                if password != password_confirm:
                    self.stdout.write(self.style.ERROR(
                        '❌ Les mots de passe ne correspondent pas. Réessayez.'
                    ))
                    continue
                break

            # Créer l'utilisateur
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                role='admin_general'
            )

            self.stdout.write('')
            self.stdout.write(self.style.SUCCESS('=' * 60))
            self.stdout.write(self.style.SUCCESS('✅ Administrateur général créé avec succès !'))
            self.stdout.write(self.style.SUCCESS('=' * 60))
            self.stdout.write('')
            self.stdout.write(self.style.SUCCESS(f'   Nom : {user.get_full_name()}'))
            self.stdout.write(self.style.SUCCESS(f'   Username : {user.username}'))
            self.stdout.write(self.style.SUCCESS(f'   Email : {user.email}'))
            self.stdout.write(self.style.SUCCESS(f'   Rôle : Administrateur Général'))
            self.stdout.write('')
            self.stdout.write(self.style.WARNING('📌 Prochaines étapes :'))
            self.stdout.write('   1. Connectez-vous sur l\'interface web')
            self.stdout.write('   2. Accédez à "Gestion des utilisateurs"')
            self.stdout.write('   3. Créez d\'autres administrateurs si nécessaire')
            self.stdout.write('')

        except KeyboardInterrupt:
            self.stdout.write('')
            self.stdout.write(self.style.ERROR('❌ Opération annulée par l\'utilisateur.'))
            return
        except IntegrityError as e:
            self.stdout.write(self.style.ERROR(f'❌ Erreur lors de la création : {e}'))
            return
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Erreur inattendue : {e}'))
            return
