"""
Script pour créer des données de test complètes pour le système de gestion PFE
Ce script crée:
- Un administrateur
- Des encadreurs
- Des étudiants
- Des sujets
- Des candidatures
- Des affectations
- Des projets avec jalons et livrables
- Des messages
- Des notifications
"""

import os
import django
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from users.models import Profile
from subjects.models import Subject, Application, Assignment
from projects.models import Project, Milestone, Deliverable, Comment
from communications.models import Message, Notification
from defenses.models import Defense, JuryMember, DefenseEvaluation

User = get_user_model()

def create_test_data():
    print("🚀 Création des données de test...")
    
    # 1. Créer un administrateur
    print("\n1️⃣ Création de l'administrateur...")
    admin, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@enspd.cm',
            'first_name': 'Admin',
            'last_name': 'Système',
            'role': 'admin',
            'is_staff': True,
            'is_superuser': True,
        }
    )
    if created:
        admin.set_password('admin123')
        admin.save()
        print("   ✅ Admin créé: admin / admin123")
    else:
        print("   ℹ️  Admin existe déjà")
    
    # 2. Créer des encadreurs
    print("\n2️⃣ Création des encadreurs...")
    supervisors_data = [
        {'username': 'prof_kamga', 'first_name': 'Jean', 'last_name': 'Kamga', 'email': 'kamga@enspd.cm', 'grade': 'Professeur'},
        {'username': 'dr_mbarga', 'first_name': 'Marie', 'last_name': 'Mbarga', 'email': 'mbarga@enspd.cm', 'grade': 'Maître de Conférences'},
    ]
    
    supervisors = []
    for data in supervisors_data:
        user, created = User.objects.get_or_create(
            username=data['username'],
            defaults={
                'email': data['email'],
                'first_name': data['first_name'],
                'last_name': data['last_name'],
                'role': 'supervisor',
                'grade': data['grade'],
            }
        )
        if created:
            user.set_password('password123')
            user.save()
            print(f"   ✅ Encadreur créé: {data['username']} / password123")
        else:
            print(f"   ℹ️  Encadreur {data['username']} existe déjà")
        supervisors.append(user)
    
    # 3. Créer des membres de jury
    print("\n3️⃣ Création des membres de jury...")
    jury_data = [
        {'username': 'jury_nkengue', 'first_name': 'Paul', 'last_name': 'Nkengue', 'email': 'nkengue@enspd.cm', 'grade': 'Professeur'},
        {'username': 'jury_foko', 'first_name': 'Sylvie', 'last_name': 'Foko', 'email': 'foko@enspd.cm', 'grade': 'Maître de Conférences'},
    ]
    
    jury_members = []
    for data in jury_data:
        user, created = User.objects.get_or_create(
            username=data['username'],
            defaults={
                'email': data['email'],
                'first_name': data['first_name'],
                'last_name': data['last_name'],
                'role': 'jury',
                'grade': data['grade'],
            }
        )
        if created:
            user.set_password('password123')
            user.save()
            print(f"   ✅ Jury créé: {data['username']} / password123")
        else:
            print(f"   ℹ️  Jury {data['username']} existe déjà")
        jury_members.append(user)
    
    # 4. Créer des étudiants
    print("\n4️⃣ Création des étudiants...")
    students_data = [
        {'username': 'etudiant1', 'first_name': 'Alice', 'last_name': 'Nguemo', 'email': 'alice@student.enspd.cm', 'level': 'L3', 'filiere': 'GL'},
        {'username': 'etudiant2', 'first_name': 'Bob', 'last_name': 'Tchounkeu', 'email': 'bob@student.enspd.cm', 'level': 'L3', 'filiere': 'RT'},
        {'username': 'etudiant3', 'first_name': 'Claire', 'last_name': 'Simo', 'email': 'claire@student.enspd.cm', 'level': 'M2', 'filiere': 'IA'},
    ]
    
    students = []
    for data in students_data:
        user, created = User.objects.get_or_create(
            username=data['username'],
            defaults={
                'email': data['email'],
                'first_name': data['first_name'],
                'last_name': data['last_name'],
                'role': 'student',
                'level': data['level'],
                'filiere': data['filiere'],
            }
        )
        if created:
            user.set_password('password123')
            user.save()
            print(f"   ✅ Étudiant créé: {data['username']} / password123")
        else:
            print(f"   ℹ️  Étudiant {data['username']} existe déjà")
        students.append(user)
    
    # 5. Créer des sujets
    print("\n5️⃣ Création des sujets...")
    subjects_data = [
        {
            'title': 'Développement d\'une application mobile de gestion des transports',
            'description': 'Conception et développement d\'une application Android/iOS pour gérer les réservations de transport en commun.',
            'supervisor': supervisors[0],
            'level': 'L3',
            'keywords': 'mobile, android, ios, transport',
        },
        {
            'title': 'Système de détection d\'intrusion réseau par apprentissage automatique',
            'description': 'Mise en place d\'un IDS utilisant des algorithmes de machine learning pour détecter les anomalies réseau.',
            'supervisor': supervisors[1],
            'level': 'L3',
            'keywords': 'sécurité, machine learning, réseau, IDS',
        },
        {
            'title': 'Chatbot intelligent pour le service client',
            'description': 'Développement d\'un chatbot basé sur le NLP pour automatiser les réponses aux clients.',
            'supervisor': supervisors[0],
            'level': 'M2',
            'keywords': 'IA, NLP, chatbot, service client',
        },
    ]
    
    subjects = []
    for data in subjects_data:
        subject, created = Subject.objects.get_or_create(
            title=data['title'],
            defaults={
                'description': data['description'],
                'supervisor': data['supervisor'],
                'level': data['level'],
                'keywords': data['keywords'],
                'status': 'published',
            }
        )
        if created:
            print(f"   ✅ Sujet créé: {data['title'][:50]}...")
        else:
            print(f"   ℹ️  Sujet existe déjà: {data['title'][:50]}...")
        subjects.append(subject)
    
    # 6. Créer des candidatures et affectations
    print("\n6️⃣ Création des candidatures et affectations...")
    
    # Candidature 1: Alice -> Sujet 1 (acceptée)
    app1, created = Application.objects.get_or_create(
        student=students[0],
        subject=subjects[0],
        defaults={
            'motivation': 'Je suis très motivée par le développement mobile et j\'ai déjà de l\'expérience avec React Native.',
            'priority': 1,
            'status': 'accepted',
        }
    )
    if created:
        print(f"   ✅ Candidature créée: {students[0].get_full_name()} -> {subjects[0].title[:30]}...")
    
    # Affectation pour Alice
    assign1, created = Assignment.objects.get_or_create(
        student=students[0],
        subject=subjects[0],
        defaults={'status': 'active'}
    )
    if created:
        print(f"   ✅ Affectation créée: {students[0].get_full_name()} assigné à {subjects[0].title[:30]}...")
    
    # Candidature 2: Bob -> Sujet 2 (acceptée)
    app2, created = Application.objects.get_or_create(
        student=students[1],
        subject=subjects[1],
        defaults={
            'motivation': 'La sécurité réseau m\'intéresse beaucoup et je souhaite approfondir mes connaissances en ML.',
            'priority': 1,
            'status': 'accepted',
        }
    )
    if created:
        print(f"   ✅ Candidature créée: {students[1].get_full_name()} -> {subjects[1].title[:30]}...")
    
    # Affectation pour Bob
    assign2, created = Assignment.objects.get_or_create(
        student=students[1],
        subject=subjects[1],
        defaults={'status': 'active'}
    )
    if created:
        print(f"   ✅ Affectation créée: {students[1].get_full_name()} assigné à {subjects[1].title[:30]}...")
    
    # 7. Créer des projets
    print("\n7️⃣ Création des projets...")
    
    # Projet 1 pour Alice
    project1, created = Project.objects.get_or_create(
        assignment=assign1,
        defaults={
            'title': subjects[0].title,
            'description': subjects[0].description,
            'status': 'in_progress',
            'progress': 45,
        }
    )
    if created:
        print(f"   ✅ Projet créé pour {students[0].get_full_name()}")
        
        # Ajouter des jalons
        Milestone.objects.create(
            project=project1,
            title='Étude de l\'existant et cahier des charges',
            description='Analyse des solutions existantes et rédaction du cahier des charges',
            due_date=datetime.now().date() - timedelta(days=30),
            is_completed=True
        )
        Milestone.objects.create(
            project=project1,
            title='Conception de l\'architecture',
            description='Diagrammes UML et architecture technique',
            due_date=datetime.now().date() - timedelta(days=15),
            is_completed=True
        )
        Milestone.objects.create(
            project=project1,
            title='Développement du backend',
            description='API REST et base de données',
            due_date=datetime.now().date() + timedelta(days=15),
            is_completed=False
        )
        print("   ✅ 3 jalons ajoutés")
        
        # Ajouter un commentaire
        Comment.objects.create(
            project=project1,
            author=supervisors[0],
            content='Excellent travail sur la phase de conception. Continue comme ça!',
            is_private=False
        )
        print("   ✅ Commentaire ajouté")
    
    # Projet 2 pour Bob
    project2, created = Project.objects.get_or_create(
        assignment=assign2,
        defaults={
            'title': subjects[1].title,
            'description': subjects[1].description,
            'status': 'in_progress',
            'progress': 30,
        }
    )
    if created:
        print(f"   ✅ Projet créé pour {students[1].get_full_name()}")
        
        # Ajouter des jalons
        Milestone.objects.create(
            project=project2,
            title='Revue de littérature sur les IDS',
            description='État de l\'art des systèmes de détection d\'intrusion',
            due_date=datetime.now().date() - timedelta(days=20),
            is_completed=True
        )
        Milestone.objects.create(
            project=project2,
            title='Collecte et préparation des données',
            description='Dataset pour l\'entraînement du modèle',
            due_date=datetime.now().date() + timedelta(days=10),
            is_completed=False
        )
        print("   ✅ 2 jalons ajoutés")
    
    # 8. Créer des messages
    print("\n8️⃣ Création des messages...")
    
    # Message de l'encadreur à l'étudiant
    msg1, created = Message.objects.get_or_create(
        sender=supervisors[0],
        recipient=students[0],
        subject='Point sur l\'avancement du projet',
        defaults={
            'content': 'Bonjour Alice,\n\nPouvez-vous me faire un point sur l\'avancement de votre projet? J\'aimerais voir votre travail sur le backend.\n\nCordialement,\nProf. Kamga',
            'is_read': False,
        }
    )
    if created:
        print("   ✅ Message créé: Encadreur -> Étudiant")
        
        # Créer une notification
        Notification.objects.create(
            user=students[0],
            notification_type='message',
            title='Nouveau message',
            message=f'{supervisors[0].get_full_name()} vous a envoyé un message',
            link=f'/communications/message/{msg1.pk}/',
            is_read=False
        )
    
    # 9. Créer une soutenance
    print("\n9️⃣ Création d\'une soutenance...")
    
    defense_date = datetime.now().date() + timedelta(days=60)
    defense, created = Defense.objects.get_or_create(
        project=project1,
        defaults={
            'defense_date': defense_date,
            'defense_time': datetime.strptime('10:00', '%H:%M').time(),
            'room': 'Amphithéâtre A',
            'duration_minutes': 45,
            'status': 'scheduled',
        }
    )
    if created:
        print(f"   ✅ Soutenance créée pour le {defense_date}")
        
        # Ajouter des membres du jury
        JuryMember.objects.create(
            defense=defense,
            user=jury_members[0],
            role='president'
        )
        JuryMember.objects.create(
            defense=defense,
            user=supervisors[0],
            role='supervisor'
        )
        JuryMember.objects.create(
            defense=defense,
            user=jury_members[1],
            role='examiner'
        )
        print("   ✅ 3 membres de jury ajoutés")
        
        # Créer une notification pour l'étudiant
        Notification.objects.create(
            user=students[0],
            notification_type='defense',
            title='Soutenance planifiée',
            message=f'Votre soutenance a été planifiée pour le {defense_date.strftime("%d/%m/%Y")} à 10:00 en {defense.room}',
            link=f'/defenses/{defense.pk}/',
            is_read=False
        )
    
    print("\n" + "="*70)
    print("✅ DONNÉES DE TEST CRÉÉES AVEC SUCCÈS!")
    print("="*70)
    print("\n📋 Récapitulatif:")
    print(f"   - {User.objects.filter(role='admin').count()} administrateur(s)")
    print(f"   - {User.objects.filter(role='supervisor').count()} encadreur(s)")
    print(f"   - {User.objects.filter(role='jury').count()} membre(s) de jury")
    print(f"   - {User.objects.filter(role='student').count()} étudiant(s)")
    print(f"   - {Subject.objects.count()} sujet(s)")
    print(f"   - {Application.objects.count()} candidature(s)")
    print(f"   - {Assignment.objects.count()} affectation(s)")
    print(f"   - {Project.objects.count()} projet(s)")
    print(f"   - {Milestone.objects.count()} jalon(s)")
    print(f"   - {Message.objects.count()} message(s)")
    print(f"   - {Notification.objects.count()} notification(s)")
    print(f"   - {Defense.objects.count()} soutenance(s)")
    print(f"   - {JuryMember.objects.count()} membre(s) de jury assigné(s)")
    
    print("\n🔑 Comptes de connexion:")
    print("   Admin: admin / admin123")
    print("   Encadreurs: prof_kamga / password123, dr_mbarga / password123")
    print("   Jurys: jury_nkengue / password123, jury_foko / password123")
    print("   Étudiants: etudiant1 / password123, etudiant2 / password123, etudiant3 / password123")
    
    print("\n🌐 Accès au système:")
    print("   URL: http://127.0.0.1:8000/")
    print("   Admin: http://127.0.0.1:8000/admin/")
    
    print("\n🎉 Vous pouvez maintenant tester toutes les fonctionnalités!")

if __name__ == '__main__':
    create_test_data()
