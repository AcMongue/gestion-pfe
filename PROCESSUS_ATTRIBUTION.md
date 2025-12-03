# 📋 PROCESSUS D'ATTRIBUTION DES PROJETS

## Vue d'ensemble

L'attribution des projets dans le système suit un **processus en 3 étapes** qui garantit une affectation équitable et transparente des sujets aux étudiants.

## 🔄 Les 3 étapes du processus

```
1. PROPOSITION DE SUJET      2. CANDIDATURE         3. AFFECTATION
   (Encadreur)                  (Étudiant)              (Admin/Encadreur)
        ↓                            ↓                        ↓
   Crée un sujet      →     Étudiant candidate    →    Évaluation et
   et le publie              avec motivation           attribution finale
```

---

## 📝 ÉTAPE 1: Proposition de sujet (Encadreur)

### Qui peut créer des sujets?
- ✅ Uniquement les utilisateurs avec le rôle **"supervisor"** (encadreur)
- ❌ Les étudiants, jurys et admins ne peuvent PAS créer de sujets

### Comment créer un sujet?

**Via l'interface web:**
1. Connexion en tant qu'encadreur
2. Aller dans: **"Mes sujets"** → **"Créer un nouveau sujet"**
3. URL: `http://127.0.0.1:8000/subjects/create/`

**Via l'interface admin Django:**
1. Connexion admin: `http://127.0.0.1:8000/admin/`
2. Aller dans: **Subjects** → **Add Subject**

### Informations requises:

```python
Informations obligatoires:
- Titre du sujet
- Description détaillée
- Niveau (L3, M2, Doctorat)
- Domaine (Informatique, IA, Web, Réseaux, etc.)
- Type (Recherche, Développement, Mixte)
- Encadreur (automatiquement l'utilisateur connecté)

Informations optionnelles:
- Objectifs spécifiques
- Prérequis
- Mots-clés
- Co-encadreur
- Nombre maximum d'étudiants (défaut: 1)
- Période de disponibilité
```

### Statuts d'un sujet:

| Statut | Description | Visible aux étudiants? |
|--------|-------------|------------------------|
| **draft** | Brouillon - En cours de rédaction | ❌ Non |
| **published** | Publié - Disponible pour candidatures | ✅ Oui |
| **assigned** | Attribué - Un étudiant a été affecté | ❌ Non (complet) |
| **archived** | Archivé - Projet terminé | ❌ Non |

**Code du modèle:**
```python
class Subject(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Brouillon'),
        ('published', 'Publié'),        # ← Seul statut visible pour candidatures
        ('assigned', 'Attribué'),
        ('archived', 'Archivé'),
    ]
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='published'
    )
```

---

## 🎓 ÉTAPE 2: Candidature (Étudiant)

### Qui peut candidater?
- ✅ Uniquement les utilisateurs avec le rôle **"student"** (étudiant)
- ✅ Seulement si l'étudiant n'a **pas déjà une affectation active**
- ✅ Seulement pour les sujets avec le statut **"published"**

### Comment candidater?

**Via l'interface web:**
1. Connexion en tant qu'étudiant
2. Parcourir le catalogue: `http://127.0.0.1:8000/subjects/`
3. Cliquer sur un sujet pour voir les détails
4. Cliquer sur **"Candidater à ce sujet"**
5. Remplir le formulaire de candidature

### Filtres disponibles pour les étudiants:

```python
# Le système filtre automatiquement par niveau
if request.user.is_student():
    if request.user.level:
        subjects = subjects.filter(level=request.user.level)
```

**Exemple:** Un étudiant en L3 voit uniquement les sujets de niveau L3.

### Informations de candidature:

```python
Informations obligatoires:
- Lettre de motivation (TextField)
  → Expliquer pourquoi vous voulez ce sujet
  → Vos compétences pertinentes
  → Vos objectifs

Informations optionnelles:
- CV (fichier PDF, DOCX, etc.)
- Priorité (1-5, où 1 = priorité maximale)
```

### Vérifications automatiques avant candidature:

```python
# 1. Le sujet est-il disponible?
if not subject.is_available():
    return "Ce sujet n'est plus disponible"

# 2. L'étudiant a-t-il déjà candidaté?
if Application.objects.filter(subject=subject, student=request.user).exists():
    return "Vous avez déjà candidaté à ce sujet"

# 3. L'étudiant a-t-il déjà une affectation?
if Assignment.objects.filter(student=request.user, status='active').exists():
    return "Vous avez déjà un sujet affecté"
```

### Statuts d'une candidature:

| Statut | Description | Action de l'étudiant |
|--------|-------------|---------------------|
| **pending** | En attente d'évaluation | ⏳ Attendre la réponse |
| **accepted** | Acceptée par l'encadreur | ✅ Attendre l'affectation admin |
| **rejected** | Rejetée par l'encadreur | ❌ Candidater ailleurs |
| **withdrawn** | Retirée par l'étudiant | 🔙 L'étudiant a annulé |

**Code du modèle:**
```python
class Application(models.Model):
    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('accepted', 'Acceptée'),
        ('rejected', 'Rejetée'),
        ('withdrawn', 'Retirée'),
    ]
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    
    priority = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
```

### Système de priorité:

Les étudiants peuvent candidater à **plusieurs sujets** avec des priorités différentes:

```
Priorité 1 = Choix préféré (priorité maximale)
Priorité 2 = Deuxième choix
Priorité 3 = Troisième choix
Priorité 4 = Choix alternatif
Priorité 5 = Dernier recours (priorité minimale)
```

---

## ✅ ÉTAPE 3: Évaluation et affectation

### A. Évaluation par l'encadreur (optionnel)

**Qui peut évaluer?**
- L'encadreur qui a proposé le sujet

**Comment évaluer?**
1. Connexion en tant qu'encadreur
2. Aller dans: **"Mes sujets"**
3. Cliquer sur un sujet
4. Voir la liste des candidatures
5. Cliquer sur une candidature pour l'évaluer

**Actions possibles:**
```python
# L'encadreur peut:
- Accepter la candidature (status = 'accepted')
- Rejeter la candidature (status = 'rejected')
- Ajouter des notes d'évaluation
```

**Code de la vue d'évaluation:**
```python
@login_required
def application_review_view(request, pk):
    application = get_object_or_404(Application, pk=pk)
    
    # Vérification: seul le superviseur du sujet peut évaluer
    if application.subject.supervisor != request.user:
        return error("Vous ne pouvez évaluer que les candidatures pour vos sujets")
    
    if request.method == 'POST':
        form = ApplicationReviewForm(request.POST, instance=application)
        if form.is_valid():
            app = form.save(commit=False)
            app.reviewed_by = request.user
            app.reviewed_at = timezone.now()
            app.save()
```

### B. Affectation finale (Admin ou via interface admin)

**Qui peut créer une affectation?**
- ✅ Les administrateurs (role = 'admin' ou superuser)
- ✅ Via l'interface admin Django

**Comment créer une affectation?**

**Méthode 1: Interface admin Django (recommandée)**
```
1. Connexion admin: http://127.0.0.1:8000/admin/
2. Aller dans: Subjects → Assignments
3. Cliquer "Add Assignment"
4. Remplir:
   - Subject: Sélectionner le sujet
   - Student: Sélectionner l'étudiant
   - Application: Optionnel (lier à une candidature)
   - Status: active
   - Assigned by: Automatique (admin connecté)
   - Start date: Date de début
   - Expected end date: Date de fin prévue
5. Sauvegarder
```

**Méthode 2: Script Python**
```python
from subjects.models import Assignment, Subject
from users.models import User

# Récupérer le sujet et l'étudiant
subject = Subject.objects.get(id=1)
student = User.objects.get(email='alice@student.enspd.cm')

# Créer l'affectation
assignment = Assignment.objects.create(
    subject=subject,
    student=student,
    status='active',
    start_date=timezone.now().date()
)

# Mettre à jour le statut du sujet
subject.status = 'assigned'
subject.save()
```

### Modèle Assignment:

```python
class Assignment(models.Model):
    STATUS_CHOICES = [
        ('active', 'Actif'),
        ('completed', 'Terminé'),
        ('cancelled', 'Annulé'),
    ]
    
    subject = models.ForeignKey(Subject, ...)
    student = models.ForeignKey(User, ...)
    application = models.OneToOneField(Application, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    assigned_by = models.ForeignKey(User, ...)
    start_date = models.DateField(null=True, blank=True)
    expected_end_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    
    class Meta:
        unique_together = ['student']  # Un étudiant = Une seule affectation
```

**Contrainte importante:**
```python
unique_together = ['student']
```
→ Un étudiant ne peut avoir qu'**une seule affectation active** à la fois.

### C. Création automatique du projet

**Après l'affectation, un projet est créé automatiquement!**

Le script `create_test_projects.py` montre comment:

```python
from projects.models import Project

# Récupérer les affectations actives
assignments = Assignment.objects.filter(status='active')

for assignment in assignments:
    # Vérifier si un projet existe déjà
    if not hasattr(assignment, 'project'):
        # Créer le projet
        project = Project.objects.create(
            assignment=assignment,
            title=assignment.subject.title,
            description=assignment.subject.description,
            objectives=assignment.subject.objectives,
            status='in_progress',
            progress_percentage=0,
            start_date=timezone.now().date()
        )
```

**Relation entre les modèles:**
```
Subject (1) ←→ (N) Application
    ↓
Assignment (1) ←→ (1) Project
    ↓
Student reçoit le projet et peut commencer à travailler
```

---

## 🔐 Permissions et contrôles d'accès

### Tableau récapitulatif:

| Action | Admin | Encadreur | Étudiant | Jury |
|--------|-------|-----------|----------|------|
| **Créer un sujet** | ✅ (via admin) | ✅ | ❌ | ❌ |
| **Voir tous les sujets** | ✅ | ✅ | ✅ (filtrés) | ✅ |
| **Modifier un sujet** | ✅ | ✅ (son sujet) | ❌ | ❌ |
| **Candidater** | ❌ | ❌ | ✅ | ❌ |
| **Évaluer candidature** | ✅ | ✅ (ses sujets) | ❌ | ❌ |
| **Créer affectation** | ✅ | ❌ | ❌ | ❌ |
| **Voir ses candidatures** | ✅ | ❌ | ✅ | ❌ |
| **Retirer candidature** | ❌ | ❌ | ✅ (pending) | ❌ |

### Contrôles dans le code:

```python
# Vérification du rôle pour créer un sujet
@login_required
def subject_create_view(request):
    if not request.user.is_supervisor():
        return error('Seuls les encadreurs peuvent proposer des sujets')

# Vérification pour candidater
@login_required
def application_create_view(request, subject_pk):
    if not request.user.is_student():
        return error('Seuls les étudiants peuvent candidater')
    
    # Vérifier qu'il n'a pas déjà une affectation
    if Assignment.objects.filter(student=request.user, status='active').exists():
        return error('Vous avez déjà un sujet affecté')

# Vérification pour évaluer
@login_required
def application_review_view(request, pk):
    if application.subject.supervisor != request.user:
        return error('Vous ne pouvez évaluer que les candidatures pour vos sujets')
```

---

## 📊 Exemple de flux complet

### Scénario: Alice veut faire un PFE sur l'IA

**JOUR 1 - Proposition du sujet**
```
👨‍🏫 Dr. Kamga (encadreur):
1. Se connecte: kamga@enspd.cm
2. Crée un sujet: "Chatbot intelligent pour le service client"
   - Niveau: M2
   - Domaine: Intelligence Artificielle
   - Type: Mixte
   - Status: published
3. Le sujet est maintenant visible aux étudiants M2
```

**JOUR 2 - Candidature**
```
👩‍🎓 Alice (étudiante M2):
1. Se connecte: alice@student.enspd.cm
2. Parcourt le catalogue /subjects/
3. Trouve le sujet de Dr. Kamga
4. Candidate avec:
   - Lettre de motivation
   - CV
   - Priorité: 1 (choix préféré)
5. Status de candidature: "pending"
```

**JOUR 5 - Évaluation**
```
👨‍🏫 Dr. Kamga:
1. Va dans "Mes sujets"
2. Voit 1 nouvelle candidature (Alice)
3. Lit la lettre de motivation
4. Accepte la candidature
5. Status: "accepted"
6. Ajoute une note: "Excellent profil, motivation claire"
```

**JOUR 7 - Affectation**
```
👨‍💼 Admin:
1. Se connecte sur /admin/
2. Va dans Subjects → Assignments
3. Crée une affectation:
   - Subject: "Chatbot intelligent..."
   - Student: Alice
   - Application: (lie à la candidature d'Alice)
   - Status: active
   - Start date: 15/12/2025
   - Expected end date: 15/06/2026
4. Sauvegarde
```

**JOUR 8 - Création automatique du projet**
```
🤖 Système (automatique ou script):
1. Détecte la nouvelle affectation
2. Crée un projet:
   - Title: "Chatbot intelligent pour le service client"
   - Assignment: Alice ↔ Sujet Dr. Kamga
   - Status: in_progress
   - Progress: 0%
3. Alice peut maintenant accéder à son projet dans /projects/
```

**JOUR 9 et suivants - Travail sur le projet**
```
👩‍🎓 Alice:
- Accède à son projet
- Crée des jalons (milestones)
- Soumet des livrables
- Communique avec Dr. Kamga
- Met à jour la progression

👨‍🏫 Dr. Kamga:
- Suit l'avancement
- Commente le travail
- Valide les livrables
```

---

## 🔍 Vérifier les affectations

### Via l'interface admin Django:

```
URL: http://127.0.0.1:8000/admin/subjects/assignment/

Vous verrez toutes les affectations avec:
- Étudiant
- Sujet
- Encadreur (via le sujet)
- Statut (active, completed, cancelled)
- Dates
```

### Via un script Python:

```python
from subjects.models import Assignment

# Toutes les affectations actives
active_assignments = Assignment.objects.filter(status='active')

for assignment in active_assignments:
    print(f"Étudiant: {assignment.student.get_full_name()}")
    print(f"Sujet: {assignment.subject.title}")
    print(f"Encadreur: {assignment.subject.supervisor.get_full_name()}")
    print(f"Date début: {assignment.start_date}")
    print("---")
```

### Via les templates:

```django
<!-- Pour un étudiant: voir son affectation -->
{% if request.user.assignment %}
    <p>Votre sujet: {{ request.user.assignment.subject.title }}</p>
    <p>Encadreur: {{ request.user.assignment.subject.supervisor.get_full_name }}</p>
{% else %}
    <p>Vous n'avez pas encore de sujet affecté.</p>
{% endif %}
```

---

## 🎯 Points clés à retenir

1. **Trois étapes distinctes:**
   - Proposition (encadreur)
   - Candidature (étudiant)
   - Affectation (admin)

2. **Un étudiant = Une affectation:**
   - Contrainte au niveau de la base de données
   - Vérification dans le code

3. **Plusieurs candidatures possibles:**
   - Un étudiant peut candidater à plusieurs sujets
   - Système de priorité (1-5)

4. **Statuts clairs:**
   - Sujet: draft → published → assigned → archived
   - Candidature: pending → accepted/rejected
   - Affectation: active → completed/cancelled

5. **Permissions strictes:**
   - Chaque rôle a des actions spécifiques
   - Contrôles d'accès à chaque étape

6. **Création automatique du projet:**
   - Une fois l'affectation créée
   - Le projet est prêt pour le suivi

---

## 📚 Fichiers concernés

```
subjects/
├── models.py          # Modèles Subject, Application, Assignment
├── views.py           # Toute la logique métier
├── forms.py           # Formulaires de candidature, évaluation
├── admin.py           # Interface admin pour gérer tout
└── urls.py            # Routes

projects/
├── models.py          # Modèle Project (créé après affectation)
└── views.py           # Gestion du projet après affectation

templates/subjects/
├── subject_list.html           # Catalogue
├── subject_detail.html         # Détails + bouton candidater
├── application_form.html       # Formulaire de candidature
├── my_applications.html        # Candidatures de l'étudiant
├── subject_applications.html   # Candidatures pour un sujet (encadreur)
└── application_review.html     # Évaluation (encadreur)
```

---

**Créé le:** 03/12/2025  
**Système:** Gestion PFE ENSPD  
**Version:** 1.0
