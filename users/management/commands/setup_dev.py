"""
Commande Django pour créer des données de test en environnement de développement.

Usage:
    python manage.py setup_dev

Cette commande crée automatiquement :
- 1 administrateur général
- 2 administrateurs de filière (GIT et GESI)
- 3 enseignants
- 5 étudiants
- Données de test pour développement rapide

⚠️ À utiliser UNIQUEMENT en développement, JAMAIS en production !
"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import transaction

User = get_user_model()


class Command(BaseCommand):
    help = 'Crée des données de test pour l\'environnement de développement'

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset',
            action='store_true',
            help='Supprimer tous les utilisateurs existants avant de créer les nouveaux',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('=' * 70))
        self.stdout.write(self.style.SUCCESS('   🚀 Configuration de l\'environnement de développement'))
        self.stdout.write(self.style.SUCCESS('=' * 70))
        self.stdout.write('')

        # Avertissement
        self.stdout.write(self.style.WARNING('⚠️  ATTENTION : Cette commande est pour le DÉVELOPPEMENT uniquement !'))
        self.stdout.write(self.style.WARNING('   Ne JAMAIS exécuter en production.'))
        self.stdout.write('')

        if options['reset']:
            response = input('⚠️  Voulez-vous vraiment SUPPRIMER tous les utilisateurs ? (oui/non) : ')
            if response.lower() in ['oui', 'o', 'yes', 'y']:
                count = User.objects.all().count()
                User.objects.all().delete()
                self.stdout.write(self.style.WARNING(f'🗑️  {count} utilisateur(s) supprimé(s).'))
                self.stdout.write('')

        try:
            with transaction.atomic():
                created_users = []

                # 1. Administrateur Général
                self.stdout.write(self.style.SUCCESS('📋 Création de l\'administrateur général...'))
                admin_general, created = User.objects.get_or_create(
                    username='admin',
                    defaults={
                        'email': 'admin@enspd.cm',
                        'first_name': 'Admin',
                        'last_name': 'Général',
                        'role': 'admin_general'
                    }
                )
                if created:
                    admin_general.set_password('admin123')
                    admin_general.save()
                    created_users.append(('admin', 'admin123', 'Administrateur Général', 'Toutes'))
                    self.stdout.write(self.style.SUCCESS('   ✅ Admin général créé'))
                else:
                    self.stdout.write(self.style.WARNING('   ⚠️  Admin général existe déjà'))

                # 2. Administrateurs de Filière
                self.stdout.write(self.style.SUCCESS('\n📋 Création des administrateurs de filière...'))
                
                admin_git, created = User.objects.get_or_create(
                    username='admin_git',
                    defaults={
                        'email': 'admin.git@enspd.cm',
                        'first_name': 'Admin',
                        'last_name': 'GIT',
                        'role': 'admin_filiere',
                        'filiere_admin': 'GIT'
                    }
                )
                if created:
                    admin_git.set_password('admin123')
                    admin_git.save()
                    created_users.append(('admin_git', 'admin123', 'Admin Filière', 'GIT'))
                    self.stdout.write(self.style.SUCCESS('   ✅ Admin GIT créé'))

                admin_gesi, created = User.objects.get_or_create(
                    username='admin_gesi',
                    defaults={
                        'email': 'admin.gesi@enspd.cm',
                        'first_name': 'Admin',
                        'last_name': 'GESI',
                        'role': 'admin_filiere',
                        'filiere_admin': 'GESI'
                    }
                )
                if created:
                    admin_gesi.set_password('admin123')
                    admin_gesi.save()
                    created_users.append(('admin_gesi', 'admin123', 'Admin Filière', 'GESI'))
                    self.stdout.write(self.style.SUCCESS('   ✅ Admin GESI créé'))

                # 3. Enseignants
                self.stdout.write(self.style.SUCCESS('\n📋 Création des enseignants...'))
                
                teachers = [
                    {
                        'username': 'prof_kamga',
                        'email': 'prof.kamga@enspd.cm',
                        'first_name': 'Paul',
                        'last_name': 'Kamga',
                        'filiere': 'GIT',
                        'academic_title': 'professeur',
                        'specialite': 'Intelligence Artificielle'
                    },
                    {
                        'username': 'prof_njoya',
                        'email': 'prof.njoya@enspd.cm',
                        'first_name': 'Marie',
                        'last_name': 'Njoya',
                        'filiere': 'GIT',
                        'academic_title': 'maitre_conference',
                        'specialite': 'Réseaux et Sécurité'
                    },
                    {
                        'username': 'prof_fotso',
                        'email': 'prof.fotso@enspd.cm',
                        'first_name': 'Jean',
                        'last_name': 'Fotso',
                        'filiere': 'GESI',
                        'academic_title': 'maitre_assistant',
                        'specialite': 'Électronique de Puissance'
                    }
                ]

                for teacher_data in teachers:
                    teacher, created = User.objects.get_or_create(
                        username=teacher_data['username'],
                        defaults={
                            'email': teacher_data['email'],
                            'first_name': teacher_data['first_name'],
                            'last_name': teacher_data['last_name'],
                            'role': 'teacher',
                            'filiere': teacher_data['filiere'],
                            'academic_title': teacher_data['academic_title'],
                            'specialite': teacher_data['specialite'],
                            'max_students': 5
                        }
                    )
                    if created:
                        teacher.set_password('prof123')
                        teacher.save()
                        created_users.append((
                            teacher_data['username'],
                            'prof123',
                            'Enseignant',
                            teacher_data['filiere']
                        ))
                        self.stdout.write(self.style.SUCCESS(f'   ✅ {teacher.get_full_name()} créé'))

                # 4. Étudiants
                self.stdout.write(self.style.SUCCESS('\n📋 Création des étudiants...'))
                
                students = [
                    {
                        'username': 'etudiant1',
                        'email': 'etudiant1@enspd.cm',
                        'first_name': 'Alice',
                        'last_name': 'Mbarga',
                        'matricule': '21G00001',
                        'filiere': 'GIT',
                        'entry_level': '1'
                    },
                    {
                        'username': 'etudiant2',
                        'email': 'etudiant2@enspd.cm',
                        'first_name': 'Bob',
                        'last_name': 'Ngono',
                        'matricule': '21G00002',
                        'filiere': 'GIT',
                        'entry_level': '1'
                    },
                    {
                        'username': 'etudiant3',
                        'email': 'etudiant3@enspd.cm',
                        'first_name': 'Claire',
                        'last_name': 'Tchoumi',
                        'matricule': '23G00001',
                        'filiere': 'GIT',
                        'entry_level': '3'
                    },
                    {
                        'username': 'etudiant4',
                        'email': 'etudiant4@enspd.cm',
                        'first_name': 'David',
                        'last_name': 'Fouda',
                        'matricule': '21G00003',
                        'filiere': 'GESI',
                        'entry_level': '1'
                    },
                    {
                        'username': 'etudiant5',
                        'email': 'etudiant5@enspd.cm',
                        'first_name': 'Emma',
                        'last_name': 'Nkolo',
                        'matricule': '23G00002',
                        'filiere': 'GESI',
                        'entry_level': '3'
                    }
                ]

                for student_data in students:
                    student, created = User.objects.get_or_create(
                        username=student_data['username'],
                        defaults={
                            'email': student_data['email'],
                            'first_name': student_data['first_name'],
                            'last_name': student_data['last_name'],
                            'role': 'student',
                            'matricule': student_data['matricule'],
                            'filiere': student_data['filiere'],
                            'entry_level': student_data['entry_level'],
                            'level': 'M2'
                        }
                    )
                    if created:
                        student.set_password('etudiant123')
                        student.save()
                        created_users.append((
                            student_data['username'],
                            'etudiant123',
                            'Étudiant',
                            student_data['filiere']
                        ))
                        self.stdout.write(self.style.SUCCESS(f'   ✅ {student.get_full_name()} créé'))

                # Résumé
                self.stdout.write('')
                self.stdout.write(self.style.SUCCESS('=' * 70))
                self.stdout.write(self.style.SUCCESS('✅ Environnement de développement configuré avec succès !'))
                self.stdout.write(self.style.SUCCESS('=' * 70))
                self.stdout.write('')
                
                if created_users:
                    self.stdout.write(self.style.SUCCESS('📋 Comptes créés :'))
                    self.stdout.write('')
                    self.stdout.write(f'{"Username":<20} {"Mot de passe":<15} {"Rôle":<20} {"Filière":<10}')
                    self.stdout.write('-' * 70)
                    for username, password, role, filiere in created_users:
                        self.stdout.write(f'{username:<20} {password:<15} {role:<20} {filiere:<10}')
                    self.stdout.write('')

                self.stdout.write(self.style.WARNING('💡 Conseils :'))
                self.stdout.write('   • Connectez-vous avec : admin / admin123')
                self.stdout.write('   • Ou testez avec les autres comptes')
                self.stdout.write('   • URL de connexion : http://127.0.0.1:8000/users/login/')
                self.stdout.write('')

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Erreur lors de la création : {e}'))
            raise
