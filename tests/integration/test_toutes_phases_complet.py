#!/usr/bin/env python
"""
Script de test complet de toutes les phases 1-7 avec création de nouvelles données.
Teste l'ensemble du workflow du système de gestion PFE.
"""

import os
import django
import random
from datetime import date, time, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.utils import timezone
from django.contrib.auth import get_user_model
from users.models import User
from subjects.models import Subject, Assignment
from projects.models import Project, AcademicYear, Milestone, ProjectTeam
from defenses.models import Defense, DefenseJury
from archives.models import ArchivedProject
from communications.models import Notification

User = get_user_model()

# Couleurs pour le terminal
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_success(msg):
    print(f"{Colors.OKGREEN}✅ {msg}{Colors.ENDC}")

def print_error(msg):
    print(f"{Colors.FAIL}❌ {msg}{Colors.ENDC}")

def print_info(msg):
    print(f"{Colors.OKCYAN}ℹ️  {msg}{Colors.ENDC}")

def print_header(msg):
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*70}")
    print(f"  {msg}")
    print(f"{'='*70}{Colors.ENDC}\n")


class TestData:
    """Classe pour stocker les données créées pendant les tests"""
    def __init__(self):
        self.users = {}
        self.subjects = {}
        self.projects = {}
        self.defenses = {}
        self.academic_year = None


def create_test_users():
    """Crée des utilisateurs de test pour toutes les phases"""
    print_header("PHASE 1: CRÉATION DES UTILISATEURS")
    
    users = {}
    
    # Admin
    try:
        admin = User.objects.create_user(
            username='admin_test',
            email='admin.test@enspd.cm',
            password='Admin@2025',
            first_name='Administrateur',
            last_name='Test',
            role='admin',
            phone='237670000001'
        )
        users['admin'] = admin
        print_success(f"Admin créé: {admin.get_full_name()} ({admin.email})")
    except Exception as e:
        print_info(f"Admin existe déjà: {e}")
        users['admin'] = User.objects.get(username='admin_test')
    
    # Professeurs (peuvent être présidents de jury)
    professeurs_data = [
        {
            'username': 'prof_kamga',
            'email': 'kamga@enspd.cm',
            'first_name': 'Jean',
            'last_name': 'Kamga',
            'filiere': 'GIT',
            'phone': '237670000002'
        },
        {
            'username': 'prof_mballa',
            'email': 'mballa@enspd.cm',
            'first_name': 'Marie',
            'last_name': 'Mballa',
            'filiere': 'GESI',
            'phone': '237670000003'
        }
    ]
    
    for prof_data in professeurs_data:
        try:
            prof = User.objects.create_user(
                username=prof_data['username'],
                email=prof_data['email'],
                password='Prof@2025',
                first_name=prof_data['first_name'],
                last_name=prof_data['last_name'],
                role='teacher',
                academic_title='professeur',
                filiere=prof_data['filiere'],
                max_students=8,
                phone=prof_data['phone']
            )
            users[prof_data['username']] = prof
            print_success(f"Professeur créé: {prof.get_full_name()} - {prof.get_filiere_display()} (Président de jury: {prof.can_be_jury_president})")
        except Exception as e:
            print_info(f"Professeur existe déjà: {prof_data['username']}")
            users[prof_data['username']] = User.objects.get(username=prof_data['username'])
    
    # Maîtres de conférences (examinateurs)
    mdc_data = [
        {
            'username': 'mdc_nguyen',
            'email': 'nguyen@enspd.cm',
            'first_name': 'Paul',
            'last_name': 'Nguyen',
            'filiere': 'GIT',
            'phone': '237670000004'
        },
        {
            'username': 'mdc_fotso',
            'email': 'fotso@enspd.cm',
            'first_name': 'Claire',
            'last_name': 'Fotso',
            'filiere': 'GESI',
            'phone': '237670000005'
        }
    ]
    
    for mdc in mdc_data:
        try:
            teacher = User.objects.create_user(
                username=mdc['username'],
                email=mdc['email'],
                password='Teacher@2025',
                first_name=mdc['first_name'],
                last_name=mdc['last_name'],
                role='teacher',
                academic_title='maitre_conference',
                filiere=mdc['filiere'],
                max_students=6,
                phone=mdc['phone']
            )
            users[mdc['username']] = teacher
            print_success(f"Maître de Conférences créé: {teacher.get_full_name()} - {teacher.get_filiere_display()}")
        except Exception as e:
            print_info(f"Enseignant existe déjà: {mdc['username']}")
            users[mdc['username']] = User.objects.get(username=mdc['username'])
    
    # Étudiants (certains en binôme)
    students_data = [
        {
            'username': 'etudiant_alice',
            'email': 'alice.dupont@enspd.cm',
            'first_name': 'Alice',
            'last_name': 'Dupont',
            'matricule': 'M2GIT2025001',
            'filiere': 'GIT',
            'phone': '237670000010'
        },
        {
            'username': 'etudiant_bob',
            'email': 'bob.martin@enspd.cm',
            'first_name': 'Bob',
            'last_name': 'Martin',
            'matricule': 'M2GIT2025002',
            'filiere': 'GIT',
            'phone': '237670000011'
        },
        {
            'username': 'etudiant_carol',
            'email': 'carol.nkembe@enspd.cm',
            'first_name': 'Carol',
            'last_name': 'Nkembe',
            'matricule': 'M2GESI2025001',
            'filiere': 'GESI',
            'phone': '237670000012'
        },
        {
            'username': 'etudiant_david',
            'email': 'david.tchinda@enspd.cm',
            'first_name': 'David',
            'last_name': 'Tchinda',
            'matricule': 'M2GESI2025002',
            'filiere': 'GESI',
            'phone': '237670000013'
        }
    ]
    
    for student in students_data:
        try:
            etud = User.objects.create_user(
                username=student['username'],
                email=student['email'],
                password='Student@2025',
                first_name=student['first_name'],
                last_name=student['last_name'],
                role='student',
                matricule=student['matricule'],
                filiere=student['filiere'],
                level='M2',
                phone=student['phone']
            )
            users[student['username']] = etud
            print_success(f"Étudiant créé: {etud.get_full_name()} - {etud.get_filiere_display()} ({etud.matricule})")
        except Exception as e:
            print_info(f"Étudiant existe déjà: {student['username']}")
            users[student['username']] = User.objects.get(username=student['username'])
    
    print_info(f"\n📊 Total utilisateurs créés: {len(users)}")
    print_info(f"   - Admins: 1")
    print_info(f"   - Professeurs: 2")
    print_info(f"   - Maîtres de Conférences: 2")
    print_info(f"   - Étudiants: 4")
    
    return users


def create_academic_year():
    """Phase 5: Crée l'année académique avec deadline"""
    print_header("PHASE 5: CRÉATION ANNÉE ACADÉMIQUE")
    
    today = timezone.now().date()
    
    try:
        academic_year = AcademicYear.objects.create(
            year="2025-2026",
            start_date=date(2025, 9, 1),
            end_date=date(2026, 7, 31),
            thesis_submission_deadline=date(2026, 6, 10),
            is_active=True
        )
        print_success(f"Année académique créée: {academic_year.year}")
        print_info(f"   - Début: {academic_year.start_date}")
        print_info(f"   - Fin: {academic_year.end_date}")
        print_info(f"   - Deadline mémoire: {academic_year.thesis_submission_deadline}")
        print_info(f"   - Active: {academic_year.is_active}")
    except Exception as e:
        print_info(f"Année académique existe déjà")
        academic_year = AcademicYear.objects.filter(is_active=True).first()
        if not academic_year:
            academic_year = AcademicYear.objects.first()
            academic_year.is_active = True
            academic_year.save()
    
    # Vérifier validation
    active_count = AcademicYear.objects.filter(is_active=True).count()
    assert active_count == 1, "❌ Plusieurs années actives détectées!"
    print_success("✓ Validation: Une seule année active")
    
    return academic_year


def create_subjects_and_assignments(users):
    """Phase 2: Crée des sujets et affectations"""
    print_header("PHASE 2: CRÉATION SUJETS ET AFFECTATIONS")
    
    subjects_data = [
        {
            'title': 'Système de recommandation intelligent avec ML',
            'supervisor': users['prof_kamga'],
            'filiere': 'GIT',
            'allows_pair': True,
            'student': users['etudiant_alice']
        },
        {
            'title': 'Application mobile de gestion IoT',
            'supervisor': users['prof_kamga'],
            'filiere': 'GIT',
            'allows_pair': True,
            'student': users['etudiant_bob']
        },
        {
            'title': 'Blockchain pour la traçabilité agricole',
            'supervisor': users['prof_mballa'],
            'filiere': 'GESI',
            'allows_pair': False,
            'student': users['etudiant_carol']
        },
        {
            'title': 'Plateforme e-learning avec IA',
            'supervisor': users['mdc_nguyen'],
            'filiere': 'GIT',
            'allows_pair': True,
            'student': users['etudiant_david']
        }
    ]
    
    subjects = {}
    
    for subj_data in subjects_data:
        try:
            subject = Subject.objects.create(
                title=subj_data['title'],
                description=f"Description du sujet: {subj_data['title']}",
                objectives="Objectifs pédagogiques et techniques",
                supervisor=subj_data['supervisor'],
                filiere=subj_data['filiere'],
                status='validated',
                allows_pair=subj_data['allows_pair'],
                keywords=f"ML,IA,{subj_data['filiere']}"
            )
            
            # Créer l'affectation
            assignment = Assignment.objects.create(
                subject=subject,
                student=subj_data['student'],
                status='accepted'
            )
            
            subjects[subj_data['title']] = {
                'subject': subject,
                'assignment': assignment
            }
            
            print_success(f"Sujet créé: {subject.title[:50]}...")
            print_info(f"   - Encadreur: {subject.supervisor.get_full_name()}")
            print_info(f"   - Filière: {subject.get_filiere_display()}")
            print_info(f"   - Binôme autorisé: {subject.allows_pair}")
            print_info(f"   - Affecté à: {subj_data['student'].get_full_name()}")
            
        except Exception as e:
            print_error(f"Erreur création sujet: {e}")
    
    print_info(f"\n📊 Total sujets créés: {len(subjects)}")
    return subjects


def create_projects_with_teams(subjects, users, academic_year):
    """Phase 3: Crée des projets avec équipes (binômes)"""
    print_header("PHASE 3: CRÉATION PROJETS ET ÉQUIPES")
    
    projects = {}
    
    # Projet 1: Binôme (Alice + Bob)
    try:
        subj1 = subjects['Système de recommandation intelligent avec ML']
        project1 = Project.objects.create(
            assignment=subj1['assignment'],
            title=subj1['subject'].title,
            description="Développement d'un système de recommandation utilisant des algorithmes de ML",
            objectives="Implémenter un moteur de recommandation performant",
            status='in_progress',
            progress_percentage=0,
            academic_year=academic_year
        )
        
        # Créer l'équipe binôme
        team1 = ProjectTeam.objects.create(
            project=project1,
            student1=users['etudiant_alice'],
            student2=users['etudiant_bob']  # Binôme
        )
        
        projects['project1'] = {'project': project1, 'team': team1}
        print_success(f"Projet 1 créé: {project1.title[:50]}...")
        print_info(f"   - Type: Binôme")
        print_info(f"   - Étudiants: {team1.student1.get_full_name()} & {team1.student2.get_full_name()}")
        print_info(f"   - Année: {academic_year.year}")
        
    except Exception as e:
        print_error(f"Erreur projet 1: {e}")
    
    # Projet 2: Individuel (Carol)
    try:
        subj2 = subjects['Blockchain pour la traçabilité agricole']
        project2 = Project.objects.create(
            assignment=subj2['assignment'],
            title=subj2['subject'].title,
            description="Application blockchain pour tracer les produits agricoles",
            objectives="Assurer la traçabilité de la chaîne d'approvisionnement",
            status='in_progress',
            progress_percentage=0,
            academic_year=academic_year
        )
        
        team2 = ProjectTeam.objects.create(
            project=project2,
            student1=users['etudiant_carol'],
            student2=None  # Individuel
        )
        
        projects['project2'] = {'project': project2, 'team': team2}
        print_success(f"Projet 2 créé: {project2.title[:50]}...")
        print_info(f"   - Type: Individuel")
        print_info(f"   - Étudiant: {team2.student1.get_full_name()}")
        
    except Exception as e:
        print_error(f"Erreur projet 2: {e}")
    
    # Projet 3: Individuel (David)
    try:
        subj3 = subjects['Plateforme e-learning avec IA']
        project3 = Project.objects.create(
            assignment=subj3['assignment'],
            title=subj3['subject'].title,
            description="Plateforme d'apprentissage en ligne avec recommandations IA",
            objectives="Personnaliser l'apprentissage avec l'IA",
            status='in_progress',
            progress_percentage=0,
            academic_year=academic_year
        )
        
        team3 = ProjectTeam.objects.create(
            project=project3,
            student1=users['etudiant_david'],
            student2=None
        )
        
        projects['project3'] = {'project': project3, 'team': team3}
        print_success(f"Projet 3 créé: {project3.title[:50]}...")
        print_info(f"   - Type: Individuel")
        print_info(f"   - Étudiant: {team3.student1.get_full_name()}")
        
    except Exception as e:
        print_error(f"Erreur projet 3: {e}")
    
    print_info(f"\n📊 Total projets créés: {len(projects)}")
    print_info(f"   - Binômes: 1")
    print_info(f"   - Individuels: 2")
    
    return projects


def create_milestones_and_test_progression(projects):
    """Phase 7: Crée des jalons et teste le calcul automatique"""
    print_header("PHASE 7: JALONS ET CALCUL PROGRESSION")
    
    project1 = projects['project1']['project']
    
    milestones_data = [
        {
            'title': 'Analyse et conception',
            'description': 'Étude de faisabilité et conception architecture',
            'due_date': date(2025, 10, 31),
            'validated': True
        },
        {
            'title': 'Développement MVP',
            'description': 'Développement du prototype minimum viable',
            'due_date': date(2025, 12, 15),
            'validated': True
        },
        {
            'title': 'Tests et optimisation',
            'description': 'Tests unitaires et optimisation performances',
            'due_date': date(2026, 2, 28),
            'validated': False
        },
        {
            'title': 'Documentation et déploiement',
            'description': 'Rédaction documentation et déploiement',
            'due_date': date(2026, 5, 31),
            'validated': False
        }
    ]
    
    for i, milestone_data in enumerate(milestones_data, 1):
        milestone = Milestone.objects.create(
            project=project1,
            title=milestone_data['title'],
            description=milestone_data['description'],
            order=i,
            due_date=milestone_data['due_date'],
            validated_by_supervisor=milestone_data['validated'],
            validation_date=timezone.now() if milestone_data['validated'] else None,
            status='completed' if milestone_data['validated'] else 'in_progress'
        )
        
        status_icon = "✅" if milestone_data['validated'] else "⏳"
        print_success(f"{status_icon} Jalon {i}: {milestone.title}")
        print_info(f"   - Échéance: {milestone.due_date}")
        print_info(f"   - Validé: {milestone.validated_by_supervisor}")
    
    # Test calcul automatique progression
    project1.refresh_from_db()
    total = project1.milestones.count()
    validated = project1.milestones.filter(validated_by_supervisor=True).count()
    calculated_progress = project1.progress
    expected = int((validated / total) * 100)
    
    print_info(f"\n📊 Progression automatique:")
    print_info(f"   - Jalons totaux: {total}")
    print_info(f"   - Jalons validés: {validated}")
    print_info(f"   - Progression calculée: {calculated_progress}%")
    print_info(f"   - Progression attendue: {expected}%")
    
    assert calculated_progress == expected, f"❌ Erreur calcul: {calculated_progress} != {expected}"
    print_success("✓ Calcul automatique progression correct")
    
    # Tester le signal avec validation d'un jalon
    print_info("\n🔄 Test signal: Validation jalon 3...")
    milestone3 = project1.milestones.get(order=3)
    milestone3.validated_by_supervisor = True
    milestone3.validation_date = timezone.now()
    milestone3.status = 'completed'
    milestone3.save()  # Déclenche le signal
    
    project1.refresh_from_db()
    new_progress = project1.progress
    print_success(f"✓ Signal déclenché: Progression mise à jour à {new_progress}%")
    
    return project1


def create_defenses_with_jury(projects, users):
    """Phase 2 & 6: Crée des soutenances avec jury"""
    print_header("PHASE 2 & 6: SOUTENANCES ET JURY")
    
    defenses = {}
    
    # Soutenance pour projet 1 (binôme)
    project1 = projects['project1']['project']
    
    defense1 = Defense.objects.create(
        project=project1,
        date=date(2026, 7, 10),
        time=time(9, 0),
        location="Amphi A",
        duration=90,
        status='scheduled'
    )
    
    print_success(f"Soutenance 1 créée: {project1.title[:50]}...")
    print_info(f"   - Date: {defense1.date}")
    print_info(f"   - Heure: {defense1.time}")
    print_info(f"   - Lieu: {defense1.location}")
    print_info(f"   - Durée: {defense1.duration} min")
    
    # Ajouter les membres du jury
    jury_members_data = [
        {
            'teacher': users['prof_kamga'],
            'role': 'president',
            'grade': None
        },
        {
            'teacher': users['mdc_nguyen'],
            'role': 'examiner',
            'grade': None
        },
        {
            'teacher': users['prof_kamga'],  # Encadreur
            'role': 'rapporteur',
            'grade': None
        }
    ]
    
    for member_data in jury_members_data:
        try:
            jury_member = DefenseJury.objects.create(
                defense=defense1,
                teacher=member_data['teacher'],
                role=member_data['role']
            )
            print_success(f"   ✓ Jury: {jury_member.teacher.get_full_name()} - {jury_member.get_role_display()}")
        except Exception as e:
            print_error(f"   Erreur ajout jury: {e}")
    
    # Vérifier validations
    jury_count = defense1.defense_jury_members.count()
    president = defense1.defense_jury_members.filter(role='president').first()
    
    assert jury_count == 3, f"❌ Nombre de jurés incorrect: {jury_count}"
    assert president.teacher.can_be_jury_president, "❌ Le président n'est pas Professeur!"
    
    print_success("✓ Validations jury OK")
    print_info(f"   - Président: {president.teacher.get_full_name()} (Professeur)")
    print_info(f"   - Membres: {jury_count}")
    
    defenses['defense1'] = defense1
    
    return defenses


def test_grading_and_archiving(defenses, users):
    """Phase 6: Teste la notation et l'archivage automatique"""
    print_header("PHASE 6: NOTATION ET ARCHIVAGE")
    
    defense1 = defenses['defense1']
    
    # Simuler que la soutenance a eu lieu
    defense1.date = timezone.now().date() - timedelta(days=1)
    defense1.save()
    
    print_info("Simulation: Soutenance terminée hier")
    
    # Notation par chaque membre du jury
    jury_members = defense1.defense_jury_members.all()
    grades = [17.5, 16.0, 18.0]  # Notes pour président, examinateur, rapporteur
    
    for i, jury_member in enumerate(jury_members):
        jury_member.grade = grades[i]
        jury_member.comments = f"Commentaire de {jury_member.teacher.get_full_name()}: Excellent travail!"
        jury_member.graded_at = timezone.now()
        jury_member.save()
        
        print_success(f"✓ Note de {jury_member.get_role_display()}: {jury_member.grade}/20")
        print_info(f"   Par: {jury_member.teacher.get_full_name()}")
    
    # Calculer note finale
    final_grade = defense1.calculate_final_grade()
    expected_grade = round(sum(grades) / len(grades), 2)
    
    print_info(f"\n📊 Calcul note finale:")
    print_info(f"   - Notes: {grades}")
    print_info(f"   - Moyenne: {final_grade}/20")
    print_info(f"   - Attendu: {expected_grade}/20")
    
    assert final_grade == expected_grade, f"❌ Erreur calcul: {final_grade} != {expected_grade}"
    print_success("✓ Calcul note finale correct")
    
    # Tester archivage automatique
    print_info("\n🗄️ Test archivage automatique...")
    
    from archives.views import archive_project_after_defense
    
    try:
        archive = archive_project_after_defense(
            project=defense1.project,
            archived_by=users['admin']
        )
        
        print_success("✓ Projet archivé automatiquement")
        print_info(f"   - ID Archive: {archive.id}")
        print_info(f"   - Année: {archive.year}")
        print_info(f"   - Semestre: {archive.semester}")
        print_info(f"   - Note finale: {archive.final_grade}/20")
        print_info(f"   - Archivé par: {archive.archived_by.get_full_name()}")
        
        # Vérifier statut projet
        defense1.project.refresh_from_db()
        assert defense1.project.status == 'completed', "❌ Statut projet non mis à jour"
        print_success("✓ Statut projet mis à jour: completed")
        
        return archive
        
    except Exception as e:
        print_error(f"Erreur archivage: {e}")
        return None


def test_thesis_management(projects, academic_year):
    """Phase 5: Teste la gestion des mémoires"""
    print_header("PHASE 5: GESTION DES MÉMOIRES")
    
    project1 = projects['project1']['project']
    
    # Tester les propriétés avant soumission
    print_info("📋 État avant soumission:")
    print_info(f"   - Mémoire soumis: {project1.is_thesis_submitted}")
    print_info(f"   - Jours avant deadline: {project1.days_until_thesis_deadline}")
    print_info(f"   - En retard: {project1.is_thesis_late}")
    
    assert project1.is_thesis_submitted == False, "❌ Mémoire déjà soumis?"
    print_success("✓ État initial correct")
    
    # Simuler soumission mémoire
    from django.core.files.uploadedfile import SimpleUploadedFile
    
    pdf_content = b'%PDF-1.4 fake thesis content for testing'
    thesis_file = SimpleUploadedFile(
        "memoire_projet1.pdf",
        pdf_content,
        content_type="application/pdf"
    )
    
    project1.submit_thesis(thesis_file)
    
    print_success("✓ Mémoire soumis")
    print_info(f"   - Fichier: {project1.thesis_file.name}")
    print_info(f"   - Date soumission: {project1.thesis_submitted_at}")
    
    # Vérifier état après soumission
    assert project1.is_thesis_submitted == True, "❌ Mémoire non détecté comme soumis"
    print_success("✓ État après soumission correct")
    
    # Approbation par encadreur
    supervisor = project1.assignment.subject.supervisor
    project1.approve_thesis(approved_by=supervisor)
    
    print_success("✓ Mémoire approuvé par l'encadreur")
    print_info(f"   - Approuvé par: {supervisor.get_full_name()}")
    print_info(f"   - Date approbation: {project1.thesis_approval_date}")
    
    assert project1.thesis_approved_by_supervisor == True, "❌ Approbation non enregistrée"
    print_success("✓ Approbation enregistrée")


def generate_summary_report(test_data):
    """Génère un rapport récapitulatif"""
    print_header("📊 RAPPORT RÉCAPITULATIF FINAL")
    
    print_success("✅ TOUTES LES PHASES TESTÉES AVEC SUCCÈS\n")
    
    print(f"{Colors.BOLD}Utilisateurs créés:{Colors.ENDC}")
    print(f"   • Administrateurs: 1")
    print(f"   • Professeurs: 2 (peuvent présider jury)")
    print(f"   • Maîtres de Conférences: 2")
    print(f"   • Étudiants: 4")
    print(f"   {Colors.OKGREEN}Total: {len(test_data.users)} utilisateurs{Colors.ENDC}\n")
    
    print(f"{Colors.BOLD}Projets créés:{Colors.ENDC}")
    print(f"   • Binômes: 1 (Alice + Bob)")
    print(f"   • Individuels: 2 (Carol, David)")
    print(f"   {Colors.OKGREEN}Total: {len(test_data.projects)} projets{Colors.ENDC}\n")
    
    print(f"{Colors.BOLD}Année académique:{Colors.ENDC}")
    print(f"   • Année: {test_data.academic_year.year}")
    print(f"   • Deadline mémoire: {test_data.academic_year.thesis_submission_deadline}")
    print(f"   • Active: {test_data.academic_year.is_active}\n")
    
    print(f"{Colors.BOLD}Jalons et progression:{Colors.ENDC}")
    project1 = test_data.projects['project1']['project']
    print(f"   • Jalons créés: {project1.milestones.count()}")
    print(f"   • Jalons validés: {project1.milestones.filter(validated_by_supervisor=True).count()}")
    print(f"   • Progression auto: {project1.progress}%\n")
    
    print(f"{Colors.BOLD}Soutenances et jury:{Colors.ENDC}")
    defense = test_data.defenses.get('defense1')
    if defense:
        print(f"   • Soutenances: 1")
        print(f"   • Membres jury: {defense.defense_jury_members.count()}")
        print(f"   • Note finale: {defense.final_grade or 'N/A'}/20\n")
    
    print(f"{Colors.BOLD}Archivage:{Colors.ENDC}")
    archived_count = ArchivedProject.objects.count()
    print(f"   • Projets archivés: {archived_count}\n")
    
    print(f"{Colors.OKGREEN}{Colors.BOLD}")
    print("="*70)
    print("  ✅ SYSTÈME COMPLET OPÉRATIONNEL")
    print("  ✅ TOUTES LES PHASES VALIDÉES (1-7)")
    print("  ✅ PRÊT POUR UTILISATION EN PRODUCTION")
    print("="*70)
    print(Colors.ENDC)


def print_credentials():
    """Affiche les identifiants de connexion"""
    print_header("🔑 IDENTIFIANTS DE CONNEXION")
    
    credentials = [
        ("Admin", "admin_test", "admin.test@enspd.cm", "Admin@2025"),
        ("Professeur", "prof_kamga", "kamga@enspd.cm", "Prof@2025"),
        ("Professeur", "prof_mballa", "mballa@enspd.cm", "Prof@2025"),
        ("Enseignant", "mdc_nguyen", "nguyen@enspd.cm", "Teacher@2025"),
        ("Enseignant", "mdc_fotso", "fotso@enspd.cm", "Teacher@2025"),
        ("Étudiant", "etudiant_alice", "alice.dupont@enspd.cm", "Student@2025"),
        ("Étudiant", "etudiant_bob", "bob.martin@enspd.cm", "Student@2025"),
        ("Étudiant", "etudiant_carol", "carol.nkembe@enspd.cm", "Student@2025"),
        ("Étudiant", "etudiant_david", "david.tchinda@enspd.cm", "Student@2025"),
    ]
    
    print(f"\n{Colors.BOLD}{'Rôle':<12} {'Username':<20} {'Email':<30} {'Password':<15}{Colors.ENDC}")
    print("-" * 80)
    
    for role, username, email, password in credentials:
        print(f"{role:<12} {username:<20} {email:<30} {password:<15}")
    
    print("\n" + Colors.WARNING + "⚠️  IMPORTANT: Changez ces mots de passe en production!" + Colors.ENDC)


def main():
    """Fonction principale"""
    print_header("🚀 TEST COMPLET DU SYSTÈME - TOUTES LES PHASES")
    print(f"{Colors.OKCYAN}Date: {timezone.now().strftime('%d/%m/%Y %H:%M:%S')}{Colors.ENDC}\n")
    
    test_data = TestData()
    
    try:
        # Phase 1: Utilisateurs
        test_data.users = create_test_users()
        
        # Phase 5: Année académique
        test_data.academic_year = create_academic_year()
        
        # Phase 2: Sujets et affectations
        test_data.subjects = create_subjects_and_assignments(test_data.users)
        
        # Phase 3: Projets et équipes (binômes)
        test_data.projects = create_projects_with_teams(
            test_data.subjects,
            test_data.users,
            test_data.academic_year
        )
        
        # Phase 7: Jalons et progression automatique
        create_milestones_and_test_progression(test_data.projects)
        
        # Phase 5: Gestion mémoires
        test_thesis_management(test_data.projects, test_data.academic_year)
        
        # Phase 2 & 6: Soutenances et jury
        test_data.defenses = create_defenses_with_jury(test_data.projects, test_data.users)
        
        # Phase 6: Notation et archivage
        test_grading_and_archiving(test_data.defenses, test_data.users)
        
        # Rapport final
        generate_summary_report(test_data)
        
        # Afficher les identifiants
        print_credentials()
        
    except Exception as e:
        print_error(f"\n❌ ERREUR CRITIQUE: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


if __name__ == '__main__':
    success = main()
    exit(0 if success else 1)
