# Améliorations du système de gestion PFE

## 1. Barre de progression du projet

### État actuel
- Le champ `progress_percentage` existe mais est manuel (0-100%)
- Pas de calcul automatique basé sur les jalons

### À implémenter
**Calcul automatique basé sur les jalons complétés :**
```python
def calculate_progress(self):
    """Calcule automatiquement le pourcentage basé sur les jalons validés."""
    total_milestones = self.milestones.count()
    if total_milestones == 0:
        return 0
    validated_milestones = self.milestones.filter(validated_by_supervisor=True).count()
    return int((validated_milestones / total_milestones) * 100)
```

---

## 2. Fin du projet et archivage

### Processus proposé
1. **Projet terminé quand :**
   - ✅ Tous les jalons validés
   - ✅ Rapport final soumis
   - ✅ Soutenance effectuée
   - ✅ Note finale attribuée par le jury

2. **Archivage automatique :**
   - Après la soutenance et notation
   - Statut passe à `archived`
   - Déplacement vers l'app `archives`

---

## 3. Simplification des rôles utilisateurs

### Changement majeur : Supprimer le rôle "jury"

**Nouveau système :**
- **student** : Étudiant
- **teacher** : Enseignant (remplace "supervisor" et "jury")
- **admin** : Administration

**Rôles d'un enseignant (teacher) :**
- Peut être **encadreur** (supervisor d'un projet)
- Peut être **co-encadreur** (co_supervisor)
- Peut être membre du **jury** (président, examinateur, rapporteur)

**Hiérarchie académique :**
```python
ACADEMIC_TITLE_CHOICES = [
    ('assistant', 'Assistant'),
    ('maitre_assistant', 'Maître Assistant'),
    ('maitre_conference', 'Maître de Conférences'),
    ('professeur', 'Professeur'),  # Seul grade pouvant présider
]
```

---

## 4. Système de jury

### Structure du jury

**Composition standard :**
- 1 **Président** (obligatoirement un Professeur)
- 2 **Examinateurs** (Maître Assistant minimum)
- 1 **Rapporteur** (l'encadreur principal)

**Composition pluridisciplinaire :**
- 1 **Président** (Professeur)
- 2 **Examinateurs** (un par filière)
- 2 **Rapporteurs** (les 2 encadreurs)

### Nouveau modèle DefenseJury

```python
class DefenseJury(models.Model):
    ROLE_CHOICES = [
        ('president', 'Président'),
        ('examiner', 'Examinateur'),
        ('rapporteur', 'Rapporteur'),
    ]
    
    defense = models.ForeignKey(Defense, on_delete=models.CASCADE, related_name='jury_members')
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'teacher'})
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    grade = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)  # Note sur 20
    comments = models.TextField(blank=True)
    
    class Meta:
        unique_together = ['defense', 'teacher', 'role']
```

### Règles de validation

1. **Président uniquement Professeur**
```python
def clean(self):
    if self.role == 'president' and self.teacher.academic_title != 'professeur':
        raise ValidationError("Seul un Professeur peut présider un jury.")
```

2. **Maximum 4 présidences par jour et par département**
```python
def validate_president_availability(teacher, defense_date, department):
    presidencies_count = DefenseJury.objects.filter(
        teacher=teacher,
        role='president',
        defense__date=defense_date,
        defense__project__assignment__subject__filiere=department
    ).count()
    
    if presidencies_count >= 4:
        raise ValidationError(f"Le professeur a déjà 4 présidences ce jour dans ce département.")
```

3. **Présidence interdépartementale autorisée**
- Un professeur peut présider dans un département différent du sien

4. **Gestion du rapporteur absent**
```python
# Si encadreur principal absent, le co-encadreur devient rapporteur
if not supervisor_available:
    rapporteur = project.assignment.subject.co_supervisor
```

---

## 5. Binômes d'étudiants

### Nouveau champ dans Subject
```python
class Subject(models.Model):
    # ... champs existants ...
    
    allows_pair = models.BooleanField(
        default=False,
        verbose_name="Accepte un binôme",
        help_text="Le sujet peut être réalisé par 2 étudiants"
    )
    
    max_students = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(2)],
        help_text="1 pour individuel, 2 pour binôme"
    )
```

### Nouveau modèle ProjectTeam
```python
class ProjectTeam(models.Model):
    project = models.OneToOneField(Project, on_delete=models.CASCADE, related_name='team')
    student1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects_as_student1')
    student2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects_as_student2', null=True, blank=True)
    
    def clean(self):
        # Vérifier même filière si pas pluridisciplinaire
        if self.student2:
            subject = self.project.assignment.subject
            if not subject.is_interdisciplinary:
                if self.student1.filiere != self.student2.filiere:
                    raise ValidationError("Les 2 étudiants doivent être de la même filière pour un sujet mono-disciplinaire.")
```

---

## 6. Sujets pluridisciplinaires par les étudiants

### Extension du modèle StudentProposal
```python
class StudentProposal(models.Model):
    # ... champs existants ...
    
    is_interdisciplinary = models.BooleanField(default=False)
    additional_filieres = models.JSONField(default=list, blank=True)
    is_pair_project = models.BooleanField(default=False, verbose_name="Projet en binôme")
    partner_student = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='partner_proposals',
        limit_choices_to={'role': 'student'}
    )
    
    def clean(self):
        # Si binôme et pas pluridisciplinaire, même filière
        if self.is_pair_project and self.partner_student:
            if not self.is_interdisciplinary:
                if self.student.filiere != self.partner_student.filiere:
                    raise ValidationError("Binôme mono-disciplinaire : les 2 étudiants doivent être de la même filière.")
```

---

## 7. Notation du projet

### Système de notation

**Note finale = Moyenne simple (non pondérée) :**
- Chaque membre du jury attribue une note sur 20
- Note finale = Moyenne arithmétique de toutes les notes

### Implémentation
```python
class Defense(models.Model):
    # ... champs existants ...
    
    def calculate_final_grade(self):
        """Calcule la note finale comme moyenne simple des notes du jury."""
        jury_members = self.jury_members.all()
        
        if not jury_members.exists():
            return None
        
        # Vérifier que tous les membres ont noté
        grades = [member.grade for member in jury_members if member.grade is not None]
        
        if len(grades) != jury_members.count():
            return None  # Toutes les notes pas encore saisies
        
        # Moyenne simple
        return round(sum(grades) / len(grades), 2)
```

---

## 8. Date limite de soumission et notifications

### Date limite de dépôt du mémoire

**Nouveau champ dans AcademicYear :**
```python
class AcademicYear(models.Model):
    year = models.CharField(max_length=9, unique=True)  # Ex: "2025-2026"
    start_date = models.DateField()
    end_date = models.DateField()
    
    # Nouvelle date limite
    thesis_submission_deadline = models.DateField(
        verbose_name="Date limite de dépôt des mémoires",
        help_text="Date à laquelle les étudiants doivent soumettre leur mémoire"
    )
    
    is_active = models.BooleanField(default=False)
```

### Workflow de soumission du mémoire

1. **Notification automatique J-7 avant la deadline :**
   - Email à tous les étudiants en M2 avec projet actif
   - Rappel de la date limite

2. **Soumission du mémoire :**
   - Étudiant uploade le mémoire validé par encadreur(s)
   - Statut projet passe à "thesis_submitted"

3. **Distribution automatique au jury :**
   - Email automatique à tous les membres du jury avec pièce jointe
   - Notification dans l'interface

```python
class Project(models.Model):
    # ... champs existants ...
    
    thesis_file = models.FileField(
        upload_to='theses/%Y/',
        null=True,
        blank=True,
        verbose_name="Mémoire final"
    )
    thesis_submitted_at = models.DateTimeField(null=True, blank=True)
    thesis_approved_by_supervisor = models.BooleanField(default=False)
```

---

## 9. Système de notifications par email

### Types de notifications

#### 1. Notifications de date limite (J-7)
```python
def notify_thesis_deadline():
    """Rappel 7 jours avant la date limite."""
    deadline = AcademicYear.objects.get(is_active=True).thesis_submission_deadline
    
    if (deadline - timezone.now().date()).days == 7:
        students = User.objects.filter(
            role='student',
            level='M2',
            assignments__project__status='in_progress'
        ).distinct()
        
        for student in students:
            send_mail(
                subject="Rappel : Date limite de dépôt du mémoire",
                message=f"Bonjour {student.get_full_name()},\n\n"
                        f"La date limite de soumission de votre mémoire est le {deadline}.\n"
                        f"Veuillez soumettre votre document validé par votre encadreur.",
                recipient_list=[student.email]
            )
```

#### 2. Distribution du mémoire au jury
```python
def distribute_thesis_to_jury(project):
    """Envoie le mémoire à tous les membres du jury."""
    defense = project.defense
    jury_members = defense.jury_members.all()
    
    for member in jury_members:
        send_mail(
            subject=f"Mémoire à évaluer - {project.title}",
            message=f"Bonjour {member.teacher.get_full_name()},\n\n"
                    f"Le mémoire du projet '{project.title}' est disponible.\n"
                    f"Soutenance prévue le {defense.date}.",
            recipient_list=[member.teacher.email],
            attachments=[('memoire.pdf', project.thesis_file.read(), 'application/pdf')]
        )
```

#### 3. Notifications de soutenance (J-3)
```python
def notify_defense_participants():
    """Notifie tous les concernés 3 jours avant la soutenance."""
    upcoming_defenses = Defense.objects.filter(
        date__date=(timezone.now() + timedelta(days=3)).date()
    )
    
    for defense in upcoming_defenses:
        project = defense.project
        
        # Liste des destinataires
        recipients = []
        
        # Étudiant(s)
        team = project.team
        recipients.append(team.student1.email)
        if team.student2:
            recipients.append(team.student2.email)
        
        # Membres du jury
        for member in defense.jury_members.all():
            recipients.append(member.teacher.email)
        
        # Email
        send_mail(
            subject=f"Rappel : Soutenance dans 3 jours - {project.title}",
            message=f"Soutenance prévue le {defense.date.strftime('%d/%m/%Y à %H:%M')}\n"
                    f"Lieu : {defense.location}\n"
                    f"Projet : {project.title}",
            recipient_list=recipients
        )
```

#### 4. Notifications d'actions importantes

**Actions déclenchant une notification :**
- ✉️ Nouveau sujet proposé → Email à admin
- ✉️ Sujet validé → Email à superviseur
- ✉️ Affectation de sujet → Email à étudiant et superviseur
- ✉️ Jalon validé → Email à étudiant
- ✉️ Jalon rejeté → Email à étudiant avec commentaires
- ✉️ Message dans communication → Email aux participants
- ✉️ Programmation de soutenance → Email à tous les concernés
- ✉️ Soumission mémoire → Email au jury
- ✉️ Notation complète → Email à étudiant avec résultat

```python
# Dans subjects/signals.py
@receiver(post_save, sender=Subject)
def notify_subject_status_change(sender, instance, created, **kwargs):
    """Notification lors de création ou validation d'un sujet."""
    if created:
        # Nouveau sujet → Admin
        send_notification_email(
            recipients=[admin.email for admin in User.objects.filter(role='admin')],
            subject="Nouveau sujet proposé",
            template='emails/new_subject.html',
            context={'subject': instance}
        )
    elif instance.status == 'validated':
        # Sujet validé → Superviseur
        send_notification_email(
            recipients=[instance.supervisor.email],
            subject="Votre sujet a été validé",
            template='emails/subject_validated.html',
            context={'subject': instance}
        )
```

### Système centralisé de notifications

```python
# communications/utils.py
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

def send_notification_email(recipients, subject, template, context, attachments=None):
    """
    Fonction centralisée pour envoyer des emails de notification.
    
    Args:
        recipients: Liste d'emails
        subject: Objet du mail
        template: Template HTML à utiliser
        context: Contexte pour le template
        attachments: Liste de tuples (filename, content, mimetype)
    """
    html_content = render_to_string(template, context)
    
    email = EmailMultiAlternatives(
        subject=subject,
        body=html_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=recipients
    )
    email.attach_alternative(html_content, "text/html")
    
    if attachments:
        for filename, content, mimetype in attachments:
            email.attach(filename, content, mimetype)
    
    email.send()
    
    # Enregistrer dans la base
    Notification.objects.create(
        recipients=recipients,
        subject=subject,
        sent_at=timezone.now()
    )
```

---

## 10. Archivage des soutenances

### Localisation de l'archive

**L'archivage se fait dans l'app `archives` avec :**

```python
class ArchivedProject(models.Model):
    # Copie des infos du projet
    original_project_id = models.IntegerField()
    title = models.CharField(max_length=200)
    student1_name = models.CharField(max_length=200)
    student1_matricule = models.CharField(max_length=20)
    student2_name = models.CharField(max_length=200, blank=True)
    student2_matricule = models.CharField(max_length=20, blank=True)
    
    # Encadrement
    supervisor_name = models.CharField(max_length=200)
    co_supervisor_name = models.CharField(max_length=200, blank=True)
    
    # Soutenance
    defense_date = models.DateTimeField()
    defense_location = models.CharField(max_length=200)
    
    # Jury
    president_name = models.CharField(max_length=200)
    examiner1_name = models.CharField(max_length=200)
    examiner2_name = models.CharField(max_length=200, blank=True)
    rapporteur_name = models.CharField(max_length=200)
    
    # Notation
    final_grade = models.DecimalField(max_digits=4, decimal_places=2)
    jury_grades = models.JSONField()  # Détail des notes par membre
    
    # Documents
    thesis_file = models.FileField(upload_to='archives/theses/%Y/')
    presentation_file = models.FileField(upload_to='archives/presentations/%Y/', blank=True)
    defense_report = models.FileField(upload_to='archives/reports/%Y/', blank=True)
    
    # Métadonnées
    archived_at = models.DateTimeField(auto_now_add=True)
    academic_year = models.CharField(max_length=9)
    filiere = models.CharField(max_length=10)
    is_interdisciplinary = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-defense_date']
        indexes = [
            models.Index(fields=['academic_year', 'filiere']),
            models.Index(fields=['defense_date']),
        ]
```

### Processus d'archivage automatique

```python
def archive_project_after_defense(defense):
    """Archive le projet après notation complète de la soutenance."""
    project = defense.project
    team = project.team
    
    # Vérifier que toutes les notes sont saisies
    if defense.final_grade is None:
        return False
    
    # Créer l'archive
    archived = ArchivedProject.objects.create(
        original_project_id=project.id,
        title=project.title,
        student1_name=team.student1.get_full_name(),
        student1_matricule=team.student1.matricule,
        student2_name=team.student2.get_full_name() if team.student2 else '',
        student2_matricule=team.student2.matricule if team.student2 else '',
        supervisor_name=project.assignment.subject.supervisor.get_full_name(),
        co_supervisor_name=project.assignment.subject.co_supervisor.get_full_name() 
            if project.assignment.subject.co_supervisor else '',
        defense_date=defense.date,
        defense_location=defense.location,
        president_name=defense.jury_members.get(role='president').teacher.get_full_name(),
        examiner1_name=defense.jury_members.filter(role='examiner').first().teacher.get_full_name(),
        examiner2_name=defense.jury_members.filter(role='examiner').last().teacher.get_full_name()
            if defense.jury_members.filter(role='examiner').count() > 1 else '',
        rapporteur_name=defense.jury_members.get(role='rapporteur').teacher.get_full_name(),
        final_grade=defense.final_grade,
        jury_grades={
            member.get_role_display(): float(member.grade)
            for member in defense.jury_members.all()
        },
        thesis_file=project.thesis_file,
        presentation_file=project.presentation,
        academic_year=get_current_academic_year(),
        filiere=project.assignment.subject.filiere,
        is_interdisciplinary=project.assignment.subject.is_interdisciplinary
    )
    
    # Marquer le projet comme archivé
    project.status = 'archived'
    project.save()
    
    # Notification à l'étudiant
    send_notification_email(
        recipients=[team.student1.email] + ([team.student2.email] if team.student2 else []),
        subject=f"Résultat de soutenance - Note finale : {defense.final_grade}/20",
        template='emails/defense_result.html',
        context={'defense': defense, 'project': project}
    )
    
    return True
```

---

## Résumé des modifications à faire

### Priorité 1 - Rôles et utilisateurs
1. ✅ Supprimer le rôle "jury"
2. ✅ Renommer "supervisor" en "teacher"
3. ✅ Ajouter champs academic_title obligatoire

### Priorité 2 - Jury et Defense
1. ✅ Créer modèle Defense
2. ✅ Créer modèle DefenseJury avec notation
3. ✅ Implémenter validation président = Professeur
4. ✅ Limite 4 présidences/jour/département
5. ✅ Gestion rapporteur absent (co-encadreur)
6. ✅ Calcul note finale (moyenne simple)

### Priorité 3 - Binômes
1. ✅ Champ allows_pair dans Subject
2. ✅ Modèle ProjectTeam
3. ✅ Validation même filière si mono-disciplinaire
4. ✅ Support binôme dans StudentProposal

### Priorité 4 - Date limite et soumission mémoire
1. ✅ AcademicYear avec thesis_submission_deadline
2. ✅ Champs thesis_file dans Project
3. ✅ Notification J-7 avant deadline
4. ✅ Distribution automatique du mémoire au jury

### Priorité 5 - Système de notifications email
1. ✅ Fonction centralisée send_notification_email
2. ✅ Templates HTML pour emails
3. ✅ Notification J-3 avant soutenance (tous les concernés)
4. ✅ Notifications sur actions importantes (signaux)
5. ✅ Notification résultat après notation complète

### Priorité 6 - Archivage
1. ✅ Modèle ArchivedProject dans app archives
2. ✅ Fonction archive_project_after_defense
3. ✅ Stockage fichiers dans archives/
4. ✅ Notification étudiant avec note finale

### Priorité 7 - Progression automatique
1. ✅ Calcul auto progress_percentage basé sur jalons
2. ✅ Suppression du champ manuel

---

## Ordre d'implémentation

### **Phase 1 : Refonte des rôles** ⭐ EN COURS
   - Migration User model : supervisor → teacher
   - Ajout academic_title
   - Mise à jour templates et vues

### **Phase 2 : Defense et Jury**
   - Modèles Defense et DefenseJury
   - Validations contraintes jury
   - Interface de programmation soutenance

### **Phase 3 : Binômes**
   - Extension Subject (allows_pair)
   - Modèle ProjectTeam
   - Validations filières

### **Phase 4 : Notifications email**
   - Configuration email Django
   - Fonction centralisée
   - Templates HTML
   - Signaux pour actions importantes

### **Phase 5 : Date limite et soumission**
   - AcademicYear avec deadline
   - Upload mémoire
   - Distribution au jury
   - Notifications J-7

### **Phase 6 : Notation et archivage**
   - Interface notation jury
   - Calcul moyenne simple
   - Archivage automatique
   - Notification résultat

### **Phase 7 : Progression automatique**
   - Calcul basé sur jalons validés
   - Migration suppression champ manuel
