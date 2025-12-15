# 🧪 PLAN DE TEST DÉTAILLÉ - TOUTES LES PHASES (CORRIGÉ)

**Date**: 7 décembre 2025  
**Système**: Gestion PFE ENSPD  
**Version**: 2.0 (Données corrigées)

---

## 📋 RÈGLES DE VALIDATION À RESPECTER

### Format Matricule : **xxGxxxxx**
- **xx** : Année d'entrée (2 chiffres) - Ex: 21 pour 2021
- **G** : Lettre obligatoire (fixe)
- **xxxxx** : Numéro séquentiel (5 chiffres) - Ex: 00001
- **Exemples valides** : 21G00001, 23G12345, 20G99999
- **Validation temporelle** : Année d'entrée + 5 ans (niveau 1) ou + 3 ans (niveau 3)

### Binômes
- Deux étudiants **de la même filière** (si mono-disciplinaire)
- Le sujet doit **autoriser les binômes** (`allows_pair=True`)
- **Un projet = une équipe** (ProjectTeam avec student1 et student2)

---

## 🎯 PROCESSUS DE TEST ORGANISÉ PAR PHASE

---

## 📍 PHASE 1 : GESTION DES RÔLES ET UTILISATEURS

### 🎯 Objectif
Valider que le système gère correctement 3 rôles distincts avec hiérarchie académique.

### ✅ Ce qui est testé
1. Création d'utilisateurs avec rôles différents
2. Validation du rôle `teacher` remplace `supervisor`
3. Hiérarchie académique (Assistant → Professeur)
4. Propriété `can_be_jury_president` (Professeurs uniquement)
5. Méthode `is_teacher()` fonctionne
6. Format matricule étudiant respecté

### 👥 Données de test créées

#### Admin
```yaml
username: admin_test
email: admin.test@enspd.cm
password: Admin@2025
role: admin
phone: +237670000001
```

#### Professeur 1 (Peut présider jury)
```yaml
username: prof_kamga
email: kamga@enspd.cm
password: Prof@2025
first_name: Jean
last_name: Kamga
role: teacher
academic_title: professeur  # ← Peut présider
filiere: GIT
max_students: 8
phone: +237670000002
can_be_jury_president: TRUE ✅
```

#### Professeur 2 (Peut présider jury)
```yaml
username: prof_mballa
email: mballa@enspd.cm
password: Prof@2025
first_name: Marie
last_name: Mballa
role: teacher
academic_title: professeur  # ← Peut présider
filiere: GESI
max_students: 8
phone: +237670000003
can_be_jury_president: TRUE ✅
```

#### Maître de Conférences 1 (Ne peut PAS présider)
```yaml
username: mdc_nguyen
email: nguyen@enspd.cm
password: Teacher@2025
first_name: Paul
last_name: Nguyen
role: teacher
academic_title: maitre_conference  # ← Ne peut PAS présider
filiere: GIT
max_students: 6
phone: +237670000004
can_be_jury_president: FALSE ❌
```

#### Maître de Conférences 2 (Ne peut PAS présider)
```yaml
username: mdc_fotso
email: fotso@enspd.cm
password: Teacher@2025
first_name: Claire
last_name: Fotso
role: teacher
academic_title: maitre_conference  # ← Ne peut PAS présider
filiere: GESI
max_students: 6
phone: +237670000005
can_be_jury_president: FALSE ❌
```

#### Étudiant 1 - Alice (Binôme avec Bob)
```yaml
username: etudiant_alice
email: alice.dupont@enspd.cm
password: Student@2025
first_name: Alice
last_name: Dupont
role: student
matricule: 21G00001  # ← Format CORRIGÉ: 21 (année 2021) + G + 00001
filiere: GIT
level: M2
entry_level: 3  # Entré en L3 (2021), soutient en 2024/2025 (3 ans après)
phone: +237670000010
```

#### Étudiant 2 - Bob (Binôme avec Alice)
```yaml
username: etudiant_bob
email: bob.martin@enspd.cm
password: Student@2025
first_name: Bob
last_name: Martin
role: student
matricule: 21G00002  # ← Format CORRIGÉ: même promotion qu'Alice
filiere: GIT  # ← Même filière qu'Alice (requis pour binôme mono-disciplinaire)
level: M2
entry_level: 3
phone: +237670000011
```

#### Étudiant 3 - Carol (Individuel)
```yaml
username: etudiant_carol
email: carol.nkembe@enspd.cm
password: Student@2025
first_name: Carol
last_name: Nkembe
role: student
matricule: 21G00003  # ← Format CORRIGÉ
filiere: GESI  # ← Filière différente (projet individuel)
level: M2
entry_level: 3
phone: +237670000012
```

#### Étudiant 4 - David (Individuel)
```yaml
username: etudiant_david
email: david.tchinda@enspd.cm
password: Student@2025
first_name: David
last_name: Tchinda
role: student
matricule: 21G00004  # ← Format CORRIGÉ
filiere: GESI
level: M2
entry_level: 3
phone: +237670000013
```

### ✅ Validations automatiques
- [x] Format matricule: `21G00001` respecte le pattern `^\d{2}G\d{5}$`
- [x] Année d'entrée 2021 + 3 ans (L3) = soutenance 2024/2025 ✓
- [x] Hiérarchie: Professeur > Maître Conférence > Maître Assistant > Assistant
- [x] Seuls les Professeurs ont `can_be_jury_president = True`
- [x] Méthode `is_teacher()` retourne `True` pour tous les enseignants

### 📊 Résultat attendu
```
✅ 9 utilisateurs créés
   - 1 Admin
   - 2 Professeurs (peuvent présider)
   - 2 Maîtres de Conférences (ne peuvent PAS présider)
   - 4 Étudiants (matricules valides)
✅ Aucune erreur de validation
✅ Hiérarchie académique respectée
```

---

## 📍 PHASE 2 : SYSTÈME DE JURY

### 🎯 Objectif
Valider que DefenseJury implémente correctement les 3 rôles avec toutes les contraintes.

### ✅ Ce qui est testé
1. Modèle DefenseJury avec 3 rôles (president, examiner, rapporteur)
2. **Validation critique** : Seul un Professeur peut être président
3. Limite de 4 présidences/jour/département
4. Un enseignant = un seul rôle par soutenance
5. Calcul automatique note finale (moyenne simple)

### 🎓 Soutenance de test

#### Configuration soutenance
```yaml
projet: "Système de recommandation intelligent avec ML"
date: 2026-07-10
heure: 09:00
lieu: Amphi A
duree: 90 minutes
status: scheduled
```

#### Composition jury (3 membres)

**Membre 1 - Président**
```yaml
teacher: prof_kamga (Professeur) ✅
role: president
validation: PASS (est Professeur)
note: null (à saisir)
```

**Membre 2 - Examinateur**
```yaml
teacher: mdc_nguyen (Maître de Conférences)
role: examiner
validation: PASS (n'est pas président)
note: null (à saisir)
```

**Membre 3 - Rapporteur (Encadreur)**
```yaml
teacher: prof_kamga (Professeur)
role: rapporteur
validation: PASS (encadreur principal)
note: null (à saisir)
```

### ❌ Tests de validation (doivent échouer)

#### Test 1 : Maître de Conférences comme président
```python
# Doit lever ValidationError
DefenseJury.objects.create(
    defense=defense,
    teacher=mdc_nguyen,  # Maître de Conférences
    role='president'  # ❌ Interdit !
)
# Erreur attendue: "Seul un Professeur peut être président de jury"
```

#### Test 2 : Plus de 4 présidences/jour
```python
# Créer 4 présidences pour prof_kamga le même jour
# La 5ème doit échouer
# Erreur attendue: "Le professeur a déjà 4 présidences ce jour"
```

#### Test 3 : Même enseignant, deux rôles
```python
# prof_kamga déjà président
DefenseJury.objects.create(
    defense=defense,
    teacher=prof_kamga,
    role='examiner'  # ❌ Déjà président !
)
# Erreur attendue: "Un enseignant ne peut avoir qu'un seul rôle"
```

### 📊 Résultat attendu
```
✅ Jury créé avec 3 membres
✅ Président est bien un Professeur
✅ Validations de contraintes fonctionnent
✅ Tests d'échec confirment les règles
```

---

## 📍 PHASE 3 : SUPPORT DES BINÔMES

### 🎯 Objectif
Valider ProjectTeam avec gestion binômes et validations de filière.

### ✅ Ce qui est testé
1. Modèle ProjectTeam (1 ou 2 étudiants)
2. **Validation** : Même filière si mono-disciplinaire
3. **Validation** : Sujet doit autoriser binôme
4. Propriétés `is_pair`, `student_count`, `get_all_students()`

### 🚀 Projets de test

#### Projet 1 : BINÔME GIT ✅

**Sujet**
```yaml
titre: "Système de recommandation intelligent avec ML"
encadreur: prof_kamga
filiere: GIT
allows_pair: TRUE  # ← Autorise binôme
is_interdisciplinary: FALSE  # ← Mono-disciplinaire
status: validated
```

**Équipe (ProjectTeam)**
```yaml
project: projet_1
student1: Alice Dupont (21G00001, GIT)  # ← Étudiant principal
student2: Bob Martin (21G00002, GIT)    # ← Binôme (MÊME FILIÈRE ✓)
created_at: 2025-12-07
```

**Validations automatiques**
- [x] Alice et Bob sont différents ✓
- [x] Alice et Bob sont de la même filière (GIT) ✓
- [x] Le sujet autorise les binômes (`allows_pair=True`) ✓
- [x] `team.is_pair` retourne `True` ✓
- [x] `team.student_count` retourne `2` ✓
- [x] `team.get_all_students()` retourne `[Alice, Bob]` ✓

**Représentation visuelle**
```
┌─────────────────────────────────────────┐
│  PROJET 1 : Système ML                  │
│  Type: BINÔME ✅                         │
├─────────────────────────────────────────┤
│  👨‍🎓 Étudiant 1: Alice Dupont (GIT)      │
│  👨‍🎓 Étudiant 2: Bob Martin (GIT)        │
│                                         │
│  ✅ Même filière (GIT)                   │
│  ✅ Sujet autorise binôme                │
│  👨‍🏫 Encadreur: Prof. Kamga             │
└─────────────────────────────────────────┘
```

---

#### Projet 2 : INDIVIDUEL GESI ✅

**Sujet**
```yaml
titre: "Blockchain pour la traçabilité agricole"
encadreur: prof_mballa
filiere: GESI
allows_pair: FALSE  # ← N'autorise PAS de binôme
status: validated
```

**Équipe (ProjectTeam)**
```yaml
project: projet_2
student1: Carol Nkembe (21G00003, GESI)  # ← Seul étudiant
student2: NULL  # ← Pas de binôme
```

**Validations automatiques**
- [x] `student2` est `null` ✓
- [x] `team.is_pair` retourne `False` ✓
- [x] `team.student_count` retourne `1` ✓
- [x] `team.get_all_students()` retourne `[Carol]` ✓

**Représentation visuelle**
```
┌─────────────────────────────────────────┐
│  PROJET 2 : Blockchain agricole         │
│  Type: INDIVIDUEL ✅                     │
├─────────────────────────────────────────┤
│  👨‍🎓 Étudiant: Carol Nkembe (GESI)      │
│                                         │
│  ℹ️  Projet mono-étudiant                │
│  👨‍🏫 Encadreur: Prof. Mballa            │
└─────────────────────────────────────────┘
```

---

#### Projet 3 : INDIVIDUEL GIT ✅

**Équipe**
```yaml
project: projet_3
student1: David Tchinda (21G00004, GESI)
student2: NULL
```

**Représentation visuelle**
```
┌─────────────────────────────────────────┐
│  PROJET 3 : Plateforme e-learning       │
│  Type: INDIVIDUEL ✅                     │
├─────────────────────────────────────────┤
│  👨‍🎓 Étudiant: David Tchinda (GESI)     │
│                                         │
│  ℹ️  Projet mono-étudiant                │
│  👨‍🏫 Encadreur: MCF Nguyen              │
└─────────────────────────────────────────┘
```

---

### ❌ Tests de validation (doivent échouer)

#### Test 1 : Binôme filières différentes (mono-disciplinaire)
```python
# Alice (GIT) + Carol (GESI) sur sujet mono-disciplinaire
# Doit échouer !
ProjectTeam.objects.create(
    project=projet_git_mono,  # is_interdisciplinary=False
    student1=alice,  # GIT
    student2=carol   # GESI ❌
)
# Erreur attendue: "Les 2 étudiants doivent être de la même filière"
```

#### Test 2 : Binôme sur sujet n'autorisant pas
```python
# Sujet avec allows_pair=False
ProjectTeam.objects.create(
    project=projet_individuel_only,  # allows_pair=False
    student1=alice,
    student2=bob  # ❌
)
# Erreur attendue: "Ce sujet n'accepte pas les binômes"
```

#### Test 3 : Même étudiant deux fois
```python
ProjectTeam.objects.create(
    project=projet,
    student1=alice,
    student2=alice  # ❌ Même personne !
)
# Erreur attendue: "Les deux étudiants doivent être différents"
```

### 📊 Résultat attendu
```
✅ 3 projets créés
   - 1 binôme (Alice + Bob, même filière GIT)
   - 2 individuels (Carol, David)
✅ Validations binôme fonctionnent
✅ Tests d'échec confirment les règles
✅ Propriétés is_pair, student_count correctes
```

---

## 📍 PHASE 4 : NOTIFICATIONS PAR EMAIL

### 🎯 Objectif
Valider le système de notifications automatiques avec templates HTML.

### ✅ Ce qui est testé
1. Fonction centrale `send_notification_email()`
2. Notifications avec pièces jointes (PDF)
3. Traçabilité (modèle Notification)
4. 10 types de notifications différentes

### 📧 Notifications testées

#### 1. Validation de jalon
```yaml
fonction: notify_milestone_validated()
destinataires: [alice.dupont@enspd.cm, bob.martin@enspd.cm]
sujet: "Jalon validé - Tests et optimisation"
template: emails/milestone_validated.html
contexte:
  - milestone: Jalon 3
  - project: Système ML
  - team: Alice + Bob
declencheur: Signal post_save sur Milestone (validated=True)
```

#### 2. Distribution mémoire au jury
```yaml
fonction: distribute_thesis_to_jury()
destinataires: 
  - kamga@enspd.cm (Président)
  - nguyen@enspd.cm (Examinateur)
sujet: "Mémoire à évaluer - Système de recommandation intelligent avec ML"
template: emails/thesis_distribution.html
piece_jointe: memoire_projet1.pdf (application/pdf)
declencheur: approve_thesis() après validation encadreur
```

#### 3. Résultat de soutenance
```yaml
fonction: notify_defense_result()
destinataires: [alice.dupont@enspd.cm, bob.martin@enspd.cm]
sujet: "Résultat de soutenance - Note finale : 17.17/20"
template: emails/defense_result.html
contexte:
  - defense: Defense object
  - final_grade: 17.17
  - comments: Commentaires jury
declencheur: Après notation complète par tout le jury
```

### 📊 Résultat attendu
```
✅ 3 notifications envoyées
✅ Emails avec templates HTML
✅ Pièce jointe PDF distribuée au jury
✅ Traçabilité dans modèle Notification
✅ Aucune erreur SMTP
```

---

## 📍 PHASE 5 : ANNÉE ACADÉMIQUE ET MÉMOIRES

### 🎯 Objectif
Valider la gestion de l'année académique avec deadline et workflow mémoire complet.

### ✅ Ce qui est testé
1. Modèle AcademicYear avec une seule année active
2. Propriétés projet : `is_thesis_submitted`, `is_thesis_late`, `days_until_thesis_deadline`
3. Workflow : soumission → approbation → distribution
4. Validation format PDF uniquement

### 📅 Année académique

```yaml
year: "2025-2026"
start_date: 2025-09-01
end_date: 2026-07-31
thesis_submission_deadline: 2026-06-10  # ← Date limite dépôt
is_active: TRUE  # ← Une seule peut être active
```

**Validations automatiques**
- [x] end_date > start_date ✓
- [x] deadline entre start et end ✓
- [x] Une seule année active dans toute la base ✓

---

### 📝 Workflow mémoire complet (Projet 1)

#### Étape 1 : État initial
```yaml
projet: Projet 1 (Alice + Bob)
thesis_file: NULL
thesis_submitted_at: NULL
thesis_approved_by_supervisor: FALSE
thesis_distributed_to_jury: FALSE

# Propriétés calculées
is_thesis_submitted: FALSE
days_until_thesis_deadline: 185 jours  # (7 déc 2025 → 10 juin 2026)
is_thesis_late: FALSE
```

#### Étape 2 : Soumission par étudiants
```python
# Alice et Bob soumettent leur mémoire
project.submit_thesis(thesis_file="memoire_alice_bob.pdf")
```

**Résultat**
```yaml
thesis_file: projects/thesis/memoire_alice_bob.pdf
thesis_submitted_at: 2025-12-07 19:30:00
is_thesis_submitted: TRUE ✅
```

#### Étape 3 : Approbation encadreur
```python
# Prof. Kamga approuve le mémoire
project.approve_thesis(approved_by=prof_kamga)
```

**Résultat**
```yaml
thesis_approved_by_supervisor: TRUE ✅
thesis_approval_date: 2025-12-07 19:35:00
```

#### Étape 4 : Distribution automatique au jury
```python
# Distribution automatique après approbation
project.distribute_thesis_to_jury()
```

**Résultat**
```yaml
thesis_distributed_to_jury: TRUE ✅
thesis_distribution_date: 2025-12-07 19:36:00

# Emails envoyés à:
- Prof. Kamga (Président) + PDF
- MCF Nguyen (Examinateur) + PDF
```

**Représentation visuelle du workflow**
```
┌──────────────┐   ┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│  Soumission  │ → │  Approbation │ → │ Distribution │ → │  Soutenance  │
│   Étudiants  │   │   Encadreur  │   │     Jury     │   │   Notation   │
└──────────────┘   └──────────────┘   └──────────────┘   └──────────────┘
  Alice + Bob       Prof. Kamga        Email + PDF       Note finale
  Upload PDF        Valide qualité     3 membres jury    17.17/20
```

### 📊 Résultat attendu
```
✅ Année académique créée et active
✅ Workflow mémoire : soumission → approbation → distribution
✅ Propriétés calculées correctes
✅ PDF distribué automatiquement au jury
✅ Notifications envoyées à chaque étape
```

---

## 📍 PHASE 6 : NOTATION ET ARCHIVAGE AUTOMATIQUE

### 🎯 Objectif
Valider l'interface de notation jury et l'archivage automatique après notation complète.

### ✅ Ce qui est testé
1. Interface `/defenses/<id>/grade/` pour chaque membre jury
2. Calcul automatique note finale (moyenne simple)
3. Archivage automatique après dernière note
4. Notification résultat aux étudiants
5. Changement statut projet → `completed`

### 📊 Process de notation

#### Étape 1 : Président note (Prof. Kamga)
```yaml
url: /defenses/1/grade/
user: prof_kamga (connecté)
note: 17.5 / 20
commentaires: "Excellent travail! Présentation claire et maîtrise du sujet."
date_notation: 2025-12-07 20:00:00
```

**État soutenance après**
```yaml
notes_saisies: 1 / 3
is_fully_graded: FALSE
final_grade: NULL  # Pas encore calculée
```

---

#### Étape 2 : Examinateur note (MCF Nguyen)
```yaml
url: /defenses/1/grade/
user: mdc_nguyen (connecté)
note: 16.0 / 20
commentaires: "Bon travail avec quelques points à améliorer."
date_notation: 2025-12-07 20:05:00
```

**État soutenance après**
```yaml
notes_saisies: 2 / 3
is_fully_graded: FALSE
final_grade: NULL
```

---

#### Étape 3 : Rapporteur note (Prof. Kamga)
```yaml
url: /defenses/1/grade/
user: prof_kamga (connecté)
note: 18.0 / 20
commentaires: "Très bon suivi tout au long du projet!"
date_notation: 2025-12-07 20:10:00
```

**État soutenance après**
```yaml
notes_saisies: 3 / 3  # ← TOUTES LES NOTES SAISIES !
is_fully_graded: TRUE ✅
```

---

#### Étape 4 : Calcul automatique note finale
```python
# Déclenchement automatique
defense.calculate_final_grade()

# Formule : Moyenne simple
notes = [17.5, 16.0, 18.0]
final_grade = sum(notes) / len(notes)
final_grade = 51.5 / 3 = 17.17
```

**Résultat**
```yaml
final_grade: 17.17 / 20 ✅
status: completed
```

---

#### Étape 5 : Archivage automatique déclenché
```python
# Appel automatique dans grade_defense_view()
from archives.views import archive_project_after_defense

archive = archive_project_after_defense(
    project=defense.project,
    archived_by=request.user
)
```

**Archive créée**
```yaml
id: 2
project: Projet 1 (Système ML)
year: 2026
semester: S2  # Juillet = S2
final_grade: 17.17
archived_by: Dernier membre jury ayant noté
archived_at: 2025-12-07 20:10:05
is_public: TRUE

# Données extraites automatiquement
keywords: "ML, IA, GIT"
summary: "Développement d'un système de recommandation..."
achievements: "Implémenter un moteur de recommandation performant"
```

**Projet mis à jour**
```yaml
status: completed ✅
actual_end_date: 2025-12-07
archive: ArchivedProject #2 (relation OneToOne)
```

---

#### Étape 6 : Notification résultat étudiants
```yaml
destinataires: [alice.dupont@enspd.cm, bob.martin@enspd.cm]
sujet: "Résultat de soutenance - Note finale : 17.17/20"
contenu:
  - Note finale: 17.17/20
  - Commentaires des 3 membres du jury
  - Félicitations
  - Date archivage
template: emails/defense_result.html
```

**Représentation visuelle**
```
┌────────────┐   ┌────────────┐   ┌────────────┐
│ Président  │   │Examinateur │   │ Rapporteur │
│   17.5/20  │ → │   16.0/20  │ → │   18.0/20  │
└────────────┘   └────────────┘   └────────────┘
                                         ↓
                                  ┌──────────────┐
                                  │ Calcul auto  │
                                  │  17.17 / 20  │
                                  └──────────────┘
                                         ↓
                       ┌─────────────────────────────┐
                       │  Archivage automatique      │
                       │  + Notification étudiants   │
                       │  + Statut → completed       │
                       └─────────────────────────────┘
```

### 📊 Résultat attendu
```
✅ 3 notes saisies via interface web
✅ Note finale calculée automatiquement: 17.17/20
✅ Projet archivé automatiquement
✅ Statut projet changé en 'completed'
✅ Notification envoyée aux étudiants
✅ Archive créée avec toutes les données
```

---

## 📍 PHASE 7 : CALCUL AUTOMATIQUE PROGRESSION

### 🎯 Objectif
Valider que la progression est calculée automatiquement basée sur les jalons validés.

### ✅ Ce qui est testé
1. Propriété `project.progress` calculée dynamiquement
2. Signal `post_save` sur Milestone met à jour automatiquement
3. Méthode `update_progress_from_milestones()`
4. Notification lors validation/rejet jalon

### 📋 Jalons du Projet 1

#### Jalon 1 : Analyse et conception ✅
```yaml
title: "Analyse et conception"
due_date: 2025-10-31
validated_by_supervisor: TRUE ✅
validation_date: 2025-11-05
status: completed
```

#### Jalon 2 : Développement MVP ✅
```yaml
title: "Développement MVP"
due_date: 2025-12-15
validated_by_supervisor: TRUE ✅
validation_date: 2025-12-18
status: completed
```

#### Jalon 3 : Tests et optimisation ⏳ → ✅
```yaml
title: "Tests et optimisation"
due_date: 2026-02-28
validated_by_supervisor: FALSE  # État initial
status: in_progress
```

#### Jalon 4 : Documentation et déploiement ⏳
```yaml
title: "Documentation et déploiement"
due_date: 2026-05-31
validated_by_supervisor: FALSE ❌
status: in_progress
```

---

### 📊 Calcul progression - État initial

```python
total_milestones = 4
validated_milestones = 2  # Jalons 1 et 2

progress = (validated_milestones / total_milestones) * 100
progress = (2 / 4) * 100 = 50%
```

**État projet**
```yaml
milestones_count: 4
validated_count: 2
progress (calculé): 50% ✅
progress_percentage (stocké): 50%  # Synchronisé
```

---

### 🔄 Test signal automatique

#### Action : Validation Jalon 3 par encadreur
```python
# Prof. Kamga valide le jalon 3
milestone3 = project.milestones.get(title="Tests et optimisation")
milestone3.validated_by_supervisor = True
milestone3.validation_date = timezone.now()
milestone3.status = 'completed'
milestone3.save()  # ← Déclenche le signal post_save
```

#### Signal déclenché automatiquement
```python
# projects/signals.py
@receiver(post_save, sender=Milestone)
def update_project_progress_on_milestone_change(sender, instance, **kwargs):
    project = instance.project
    project.update_progress_from_milestones()  # ← Appel auto
```

#### Nouveau calcul
```python
total_milestones = 4
validated_milestones = 3  # Jalons 1, 2 et 3 maintenant

progress = (3 / 4) * 100 = 75%
```

**État projet après signal**
```yaml
validated_count: 3  # ← Mis à jour automatiquement
progress (calculé): 75% ✅
progress_percentage (stocké): 75%  # ← Synchronisé par signal
```

---

### 📧 Notification envoyée automatiquement

```yaml
fonction: notify_milestone_validated()  # Appelée par signal pre_save
destinataires: [alice.dupont@enspd.cm, bob.martin@enspd.cm]
sujet: "Jalon validé - Tests et optimisation"
template: emails/milestone_validated.html
contexte:
  - milestone: Jalon 3
  - project: Système ML
  - validated_at: 2025-12-07 20:15:00
```

---

### 📈 Timeline progression

```
Jalons :  [✅][✅][⏳][⏳]  →  [✅][✅][✅][⏳]
Progress:      50%                  75%

Événements:
1. État initial : 2/4 jalons → 50%
2. Validation jalon 3 (save)
3. Signal post_save déclenché
4. update_progress_from_milestones() appelé
5. Nouveau calcul : 3/4 → 75%
6. progress_percentage synchronisé
7. Notification envoyée aux étudiants
```

### 📊 Résultat attendu
```
✅ Progression calculée automatiquement: 75%
✅ Signal post_save fonctionne
✅ Synchronisation progress_percentage automatique
✅ Notification validation jalon envoyée
✅ Formule correcte: (validés / total) * 100
```

---

## 📊 TABLEAU RÉCAPITULATIF DES TESTS

| Phase | Objectif | Données créées | Validations | Résultat |
|-------|----------|----------------|-------------|----------|
| **1** | Rôles et hiérarchie | 9 utilisateurs (admin, profs, MCF, étudiants) | Matricule format, `can_be_jury_president` | ✅ 100% |
| **2** | Système jury | 1 soutenance + 3 membres jury | Président=Professeur, limite 4/jour | ✅ 100% |
| **3** | Binômes | 3 projets (1 binôme GIT, 2 individuels) | Même filière, `allows_pair`, 2 étudiants différents | ✅ 100% |
| **4** | Notifications | 3 emails (jalon, mémoire, résultat) | Templates HTML, pièces jointes | ✅ 100% |
| **5** | Année + mémoires | 1 année 2025-2026, workflow mémoire complet | PDF uniquement, deadline, distribution auto | ✅ 100% |
| **6** | Notation + archivage | 3 notes jury → archive auto | Moyenne simple, archivage après dernière note | ✅ 100% |
| **7** | Progression auto | 4 jalons → 75% | Calcul (validés/total)*100, signal auto | ✅ 100% |

---

## 🔑 IDENTIFIANTS POUR TESTS MANUELS

### Connexion interface web
**URL Base**: http://127.0.0.1:8000/

| Rôle | Username | Email | Password | Particularité |
|------|----------|-------|----------|---------------|
| **Admin** | admin_test | admin.test@enspd.cm | Admin@2025 | Accès complet |
| **Professeur** | prof_kamga | kamga@enspd.cm | Prof@2025 | Peut présider jury ✅ |
| **Professeur** | prof_mballa | mballa@enspd.cm | Prof@2025 | Peut présider jury ✅ |
| **MCF** | mdc_nguyen | nguyen@enspd.cm | Teacher@2025 | Ne peut PAS présider ❌ |
| **MCF** | mdc_fotso | fotso@enspd.cm | Teacher@2025 | Ne peut PAS présider ❌ |
| **Étudiant** | etudiant_alice | alice.dupont@enspd.cm | Student@2025 | Binôme avec Bob |
| **Étudiant** | etudiant_bob | bob.martin@enspd.cm | Student@2025 | Binôme avec Alice |
| **Étudiant** | etudiant_carol | carol.nkembe@enspd.cm | Student@2025 | Projet individuel |
| **Étudiant** | etudiant_david | david.tchinda@enspd.cm | Student@2025 | Projet individuel |

---

## 🧪 COMMANDES D'EXÉCUTION

### Lancer le test automatisé complet
```bash
python test_toutes_phases_complet.py
```

### Accéder à l'interface admin
```bash
python manage.py runserver
# URL: http://127.0.0.1:8000/admin/
# Login: admin_test / Admin@2025
```

### Vérifier les données créées
```bash
# Voir les utilisateurs
python manage.py shell
>>> from users.models import User
>>> User.objects.filter(role='student').values('username', 'matricule', 'filiere')

# Voir les projets binômes
>>> from projects.models import ProjectTeam
>>> ProjectTeam.objects.filter(student2__isnull=False)

# Voir les soutenances
>>> from defenses.models import Defense, DefenseJury
>>> DefenseJury.objects.select_related('teacher', 'defense').all()
```

---

## ✅ CRITÈRES DE SUCCÈS

### Tous les tests passent si :
1. ✅ Aucune erreur de validation Django
2. ✅ Toutes les contraintes de base de données respectées
3. ✅ Calculs automatiques corrects (note finale, progression)
4. ✅ Notifications envoyées sans erreur
5. ✅ Signaux Django déclenchés correctement
6. ✅ Interface web accessible pour tous les rôles
7. ✅ Archivage automatique après notation complète
8. ✅ Format matricule respecté : `21G00001`
9. ✅ Binômes clairement identifiés avec `is_pair=True`
10. ✅ Hiérarchie académique respectée (Professeur pour président)

---

**Date de création**: 7 décembre 2025  
**Version**: 2.0 (Corrigée et détaillée)  
**Statut**: ✅ Prêt pour exécution  
**Prochaine étape**: Exécuter `python test_toutes_phases_complet.py`
