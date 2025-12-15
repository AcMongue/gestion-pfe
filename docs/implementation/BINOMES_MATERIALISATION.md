# 🎯 Matérialisation des Binômes dans GradEase

**Date**: 7 décembre 2025  
**Application**: GradEase - Gestion PFE ENSPD

---

## ✅ État actuel du système

### Backend - Modèle ProjectTeam (100% complet)

Le système possède déjà **une modélisation complète des binômes** :

```python
# projects/models.py
class ProjectTeam(models.Model):
    """
    Modèle représentant l'équipe d'un projet (1 ou 2 étudiants).
    Gère les binômes avec validation de filière.
    """
    
    project = models.OneToOneField(Project, related_name='team')
    
    # Étudiant principal (toujours présent)
    student1 = models.ForeignKey(
        User, 
        related_name='projects_as_student1',
        verbose_name='Étudiant 1 (principal)'
    )
    
    # Binôme (optionnel)
    student2 = models.ForeignKey(
        User, 
        related_name='projects_as_student2',
        verbose_name='Étudiant 2 (binôme)',
        null=True,
        blank=True
    )
    
    @property
    def is_pair(self):
        """Indique si c'est un binôme."""
        return self.student2 is not None
    
    @property
    def student_count(self):
        """Nombre d'étudiants dans l'équipe."""
        return 2 if self.student2 else 1
    
    def get_all_students(self):
        """Retourne la liste de tous les étudiants."""
        if self.student2:
            return [self.student1, self.student2]
        return [self.student1]
```

### ✅ Validations automatiques

Le système valide automatiquement :

1. **Même filière** si sujet mono-disciplinaire
   ```python
   if self.student2:
       if not subject.is_interdisciplinary:
           if self.student1.filiere != self.student2.filiere:
               raise ValidationError(
                   "Les 2 étudiants doivent être de la même filière"
               )
   ```

2. **Sujet accepte binômes**
   ```python
   if self.student2:
       if not subject.allows_pair:
           raise ValidationError("Ce sujet n'accepte pas les binômes.")
   ```

3. **Étudiants différents**
   ```python
   if self.student2 and self.student1 == self.student2:
       raise ValidationError("Les deux étudiants doivent être différents.")
   ```

---

## 🎨 Améliorations de l'interface (Réalisées)

### 1. Nom de l'application : **GradEase** ✅

**Avant** :
```html
<title>Gestion PFE - ENSPD</title>
<a class="navbar-brand">Gestion PFE</a>
```

**Après** :
```html
<title>GradEase - Gestion PFE ENSPD</title>
<a class="navbar-brand">
    <i class="fas fa-graduation-cap"></i> GradEase
</a>
```

---

### 2. Page Détail du Projet - Affichage Équipe ✅

**Avant** (affichage basique) :
```html
<div class="card-body">
    <p><strong>Étudiant:</strong><br>{{ project.assignment.student.get_full_name }}</p>
    <p><strong>Encadreur:</strong><br>{{ project.assignment.subject.supervisor.get_full_name }}</p>
</div>
```

**Après** (avec matérialisation des binômes) :
```html
<div class="card-body">
    {% if project.team %}
        {% if project.team.is_pair %}
            <!-- Badge visuel BINÔME -->
            <div class="alert alert-info mb-3">
                <i class="fas fa-user-friends"></i> <strong>Projet en BINÔME</strong>
            </div>
            
            <!-- Étudiant 1 avec détails -->
            <p><strong>Étudiant 1:</strong><br>
                <i class="fas fa-user"></i> {{ project.team.student1.get_full_name }}<br>
                <small class="text-muted">
                    {{ project.team.student1.matricule }} - 
                    {{ project.team.student1.get_filiere_display }}
                </small>
            </p>
            
            <!-- Étudiant 2 avec détails -->
            <p><strong>Étudiant 2:</strong><br>
                <i class="fas fa-user"></i> {{ project.team.student2.get_full_name }}<br>
                <small class="text-muted">
                    {{ project.team.student2.matricule }} - 
                    {{ project.team.student2.get_filiere_display }}
                </small>
            </p>
        {% else %}
            <!-- Badge visuel INDIVIDUEL -->
            <div class="alert alert-secondary mb-3">
                <i class="fas fa-user"></i> <strong>Projet INDIVIDUEL</strong>
            </div>
            
            <p><strong>Étudiant:</strong><br>
                <i class="fas fa-user"></i> {{ project.team.student1.get_full_name }}<br>
                <small class="text-muted">
                    {{ project.team.student1.matricule }} - 
                    {{ project.team.student1.get_filiere_display }}
                </small>
            </p>
        {% endif %}
    {% endif %}
    
    <hr>
    
    <!-- Encadreur avec grade académique -->
    <p><strong>Encadreur:</strong><br>
        <i class="fas fa-chalkboard-teacher"></i> {{ project.assignment.subject.supervisor.get_full_name }}<br>
        <small class="text-muted">{{ project.assignment.subject.supervisor.get_academic_title_display }}</small>
    </p>
</div>
```

**Rendu visuel** :

#### Projet en BINÔME :
```
┌─────────────────────────────────────────┐
│  ℹ️  Projet en BINÔME                    │
├─────────────────────────────────────────┤
│  Étudiant 1:                            │
│  👤 Alice Dupont                         │
│  21G00001 - GIT                         │
│                                         │
│  Étudiant 2:                            │
│  👤 Bob Martin                           │
│  21G00002 - GIT                         │
│                                         │
│  ─────────────────────────────────────  │
│  Encadreur:                             │
│  👨‍🏫 Prof. Jean Kamga                    │
│  Professeur                             │
└─────────────────────────────────────────┘
```

#### Projet INDIVIDUEL :
```
┌─────────────────────────────────────────┐
│  Projet INDIVIDUEL                      │
├─────────────────────────────────────────┤
│  Étudiant:                              │
│  👤 Carol Nkembe                         │
│  21G00003 - GESI                        │
│                                         │
│  ─────────────────────────────────────  │
│  Encadreur:                             │
│  👨‍🏫 Prof. Marie Mballa                  │
│  Professeur                             │
└─────────────────────────────────────────┘
```

---

### 3. Page "Mes Projets" - Liste avec badges ✅

**Avant** :
```html
<h5 class="card-title">{{ project.assignment.subject.title }}</h5>
<p class="card-text text-muted">
    <small>
        {% if user.is_teacher %}
            Étudiant: {{ project.assignment.student.get_full_name }}
        {% endif %}
    </small>
</p>
```

**Après** :
```html
<h5 class="card-title">{{ project.assignment.subject.title }}</h5>

<!-- Badge type de projet -->
{% if project.team and project.team.is_pair %}
    <span class="badge bg-info mb-2">
        <i class="fas fa-user-friends"></i> BINÔME
    </span>
{% else %}
    <span class="badge bg-secondary mb-2">
        <i class="fas fa-user"></i> INDIVIDUEL
    </span>
{% endif %}

<p class="card-text text-muted">
    <small>
        {% if user.is_teacher %}
            {% if project.team and project.team.is_pair %}
                Étudiants: {{ project.team.student1.get_full_name }} & {{ project.team.student2.get_full_name }}
            {% else %}
                Étudiant: {{ project.assignment.student.get_full_name }}
            {% endif %}
        {% endif %}
    </small>
</p>
```

**Rendu visuel** :

```
┌─────────────────────────────────────────┐
│  Système de recommandation ML           │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│  [🧑‍🤝‍🧑 BINÔME]                          │
│                                         │
│  Étudiants: Alice Dupont & Bob Martin   │
│  Progression: 75%                       │
│  ████████████░░░░░░                     │
│                                         │
│  [Voir le projet]                       │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│  Blockchain pour l'agriculture          │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│  [👤 INDIVIDUEL]                         │
│                                         │
│  Étudiant: Carol Nkembe                 │
│  Progression: 50%                       │
│  ████████░░░░░░░░░░░░                   │
│                                         │
│  [Voir le projet]                       │
└─────────────────────────────────────────┘
```

---

## 📊 Récapitulatif des éléments visuels

| Élément | Binôme | Individuel |
|---------|--------|------------|
| **Badge** | 🧑‍🤝‍🧑 BINÔME (bleu) | 👤 INDIVIDUEL (gris) |
| **Alerte (détail)** | `alert-info` avec icône `fa-user-friends` | `alert-secondary` avec icône `fa-user` |
| **Informations affichées** | 2 étudiants avec matricules et filières | 1 étudiant avec matricule et filière |
| **Vue encadreur** | "Alice Dupont & Bob Martin" | "Carol Nkembe" |
| **Propriété utilisée** | `project.team.is_pair = True` | `project.team.is_pair = False` |

---

## 🔍 Comment vérifier dans l'interface

### 1. Créer un projet en binôme

```python
# Dans le shell Django
from users.models import User
from subjects.models import Subject, Assignment
from projects.models import Project, ProjectTeam

# Créer 2 étudiants de la même filière
alice = User.objects.create_user(
    username='alice',
    matricule='21G00001',
    filiere='GIT',
    role='student'
)
bob = User.objects.create_user(
    username='bob',
    matricule='21G00002',
    filiere='GIT',  # Même filière !
    role='student'
)

# Créer un sujet autorisant binôme
subject = Subject.objects.create(
    title="Projet test binôme",
    allows_pair=True,  # Important !
    is_interdisciplinary=False
)

# Créer affectation et projet
assignment = Assignment.objects.create(
    subject=subject,
    student=alice
)
project = Project.objects.create(
    assignment=assignment,
    title="Projet test"
)

# Créer l'équipe binôme
team = ProjectTeam.objects.create(
    project=project,
    student1=alice,
    student2=bob  # Binôme !
)

print(f"Binôme créé: {team.is_pair}")  # True
print(f"Étudiants: {team.get_all_students()}")  # [alice, bob]
```

### 2. Accéder à l'interface web

1. **Se connecter** avec un compte encadreur
2. **Aller dans "Mes Projets"** → Voir le badge `[🧑‍🤝‍🧑 BINÔME]`
3. **Cliquer sur "Voir le projet"** → Voir l'alerte bleue avec les 2 étudiants détaillés

---

## ✅ Avantages de cette implémentation

### Pour les étudiants :
- ✅ Voient clairement si leur projet est individuel ou en binôme
- ✅ Identification rapide du binôme sur la page du projet

### Pour les encadreurs :
- ✅ Vue d'ensemble immédiate : binômes vs individuels dans la liste
- ✅ Accès rapide aux 2 matricules et filières
- ✅ Validation automatique des contraintes (même filière, sujet accepte binôme)

### Pour l'administration :
- ✅ Données structurées dans ProjectTeam
- ✅ Requêtes SQL faciles : `ProjectTeam.objects.filter(student2__isnull=False)` → tous les binômes
- ✅ Statistiques : `ProjectTeam.objects.filter(student2__isnull=False).count()` → nombre de binômes

---

## 🎯 Prochaines améliorations possibles

1. **Tableau de bord statistiques**
   - Nombre de projets en binôme vs individuels
   - Répartition par filière
   - Graphiques visuels

2. **Filtre de recherche**
   - Filtrer uniquement les binômes
   - Filtrer par filière commune

3. **Export Excel/PDF**
   - Liste complète avec colonnes "Type" (Binôme/Individuel)
   - Matricules des 2 étudiants pour binômes

4. **Notifications spécifiques**
   - Email envoyé aux **2 étudiants** d'un binôme
   - Mention explicite du binôme dans les emails

---

## 📝 Résumé

| Aspect | État |
|--------|------|
| **Backend (Modèle)** | ✅ 100% complet depuis le début |
| **Validations** | ✅ Même filière, sujet accepte, étudiants différents |
| **Propriétés** | ✅ `is_pair`, `student_count`, `get_all_students()` |
| **Interface visuelle** | ✅ **AMÉLIORÉ** (badges, alertes, détails) |
| **Nom application** | ✅ **GradEase** |

**Conclusion** : Le système **matérialise maintenant complètement les binômes** à tous les niveaux (backend + frontend) avec une interface visuelle claire et intuitive ! 🎉

---

**Fichiers modifiés** :
- `templates/base.html` : Nom "GradEase"
- `templates/projects/project_detail.html` : Badges et détails binômes
- `templates/projects/my_projects.html` : Badges dans la liste

**Fichiers backend** (déjà complets) :
- `projects/models.py` : Modèle ProjectTeam avec validations
- `projects/admin.py` : Interface admin pour gérer les équipes
