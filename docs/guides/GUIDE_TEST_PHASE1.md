# 🧪 GUIDE DE TEST - PHASE 1 WORKFLOW COMPLET

## 🚀 Démarrage

Le serveur est démarré sur: **http://127.0.0.1:8000/**

## 📝 Comptes de test

### Étudiant
- **Username:** `etudiant_test` ou un étudiant existant
- **Password:** `test123` ou le mot de passe configuré

### Encadreur
- **Username:** `encadreur_test` ou un encadreur existant
- **Password:** `test123` ou le mot de passe configuré

### Admin (si nécessaire)
- **Username:** `admin`
- **Password:** Le mot de passe admin configuré

---

## ✅ SCÉNARIO DE TEST COMPLET

### PARTIE 1: ÉTUDIANT - PROPOSITION D'UN SUJET

#### Étape 1: Connexion
1. Aller sur http://127.0.0.1:8000/
2. Cliquer sur "Connexion"
3. Se connecter avec un compte **étudiant**

#### Étape 2: Vérifier le tableau de bord
- ✅ Vérifier que le menu latéral contient:
  - "Proposer un sujet" (en vert/en évidence)
  - "Mes propositions"
- ✅ Vérifier les statistiques affichées

#### Étape 3: Créer une proposition
1. Cliquer sur **"Proposer un sujet"** dans le menu
2. URL: http://127.0.0.1:8000/subjects/proposals/create/
3. Remplir le formulaire:

**Informations de base:**
- **Titre:** "Plateforme de e-learning avec IA"
- **Description:** "Une plateforme d'apprentissage en ligne qui utilise l'intelligence artificielle pour personnaliser le parcours de chaque étudiant..."
- **Objectifs:** 
  ```
  - Développer une interface utilisateur intuitive
  - Implémenter un système de recommandation basé sur l'IA
  - Créer un tableau de bord pour les enseignants
  - Assurer la sécurité des données
  ```

**Détails du projet:**
- **Méthodologie:** "Développement agile avec sprints de 2 semaines, tests unitaires et intégration continue"
- **Technologies:** "Django, React, TensorFlow, PostgreSQL, Docker"
- **Domaine:** Génie Logiciel
- **Type:** Développement

**Choix des encadreurs:**
- **Encadreur préféré 1:** Sélectionner un encadreur
- **Encadreur préféré 2:** (Optionnel) Sélectionner un autre encadreur
- **Encadreur préféré 3:** (Optionnel) Sélectionner un troisième encadreur
- **Justification:** "Le Dr. X est spécialisé en IA et apprentissage automatique, ce qui correspond parfaitement aux besoins techniques du projet..."

4. Cliquer sur **"Soumettre ma proposition"**

**Résultats attendus:**
- ✅ Message de succès: "Votre proposition a été soumise avec succès!"
- ✅ Redirection vers "Mes propositions"
- ✅ La proposition apparaît avec le statut "En attente" (badge orange)
- ✅ Les 3 encadreurs choisis sont listés

#### Étape 4: Vérifier "Mes propositions"
1. Aller dans **"Mes propositions"**
2. URL: http://127.0.0.1:8000/subjects/proposals/my-proposals/

**Vérifications:**
- ✅ La proposition créée est visible
- ✅ Statut: "En attente" avec badge orange
- ✅ Bouton "Voir les détails"
- ✅ Liste des encadreurs choisis

3. Cliquer sur **"Voir les détails"**

**Vérifications du détail:**
- ✅ Toutes les informations sont affichées correctement
- ✅ Encadreurs listés par ordre de préférence
- ✅ Bouton "Retour" fonctionne

---

### PARTIE 2: ENCADREUR - RÉCEPTION ET ACCEPTATION

#### Étape 5: Déconnexion et connexion encadreur
1. Se déconnecter (icône utilisateur → Déconnexion)
2. Se reconnecter avec un compte **encadreur** (celui choisi dans la proposition)

#### Étape 6: Vérifier les notifications
**Vérifications du tableau de bord:**
- ✅ Badge rouge sur "Propositions reçues" avec le nombre (1)
- ✅ Carte "Propositions reçues" avec le chiffre 1
- ✅ Bouton "Voir les propositions"

#### Étape 7: Consulter les propositions reçues
1. Cliquer sur **"Propositions reçues"** dans le menu
2. URL: http://127.0.0.1:8000/subjects/proposals/

**Vérifications:**
- ✅ Boutons de filtre: Toutes / En attente / Acceptées / Rejetées
- ✅ Filtre "En attente" actif par défaut
- ✅ Carte de la proposition avec:
  - Titre du projet
  - Nom de l'étudiant (niveau, filière)
  - Description courte
  - Technologies
  - Domaine et type
  - Bouton "Voir les détails"
  - Bouton "Accepter" (vert)

3. Cliquer sur **"Voir les détails"**

**Vérifications du détail:**
- ✅ Toutes les informations complètes
- ✅ Badge du statut (En attente)
- ✅ Informations sur l'étudiant
- ✅ Description complète
- ✅ Objectifs, méthodologie, technologies
- ✅ Liste des 3 encadreurs choisis
- ✅ Justification du choix
- ✅ Boutons: "Retour", "Accepter", "Décliner"

#### Étape 8: Accepter la proposition
1. Cliquer sur le bouton **"Accepter d'encadrer ce projet"** (vert)
2. URL: http://127.0.0.1:8000/subjects/proposals/X/accept/

**Vérifications page d'acceptation:**
- ✅ En-tête vert avec icône de validation
- ✅ Résumé de la proposition
- ✅ Lien vers proposition complète (nouvel onglet)
- ✅ Champ "Commentaires" (optionnel)
- ✅ Alerte bleue expliquant les conséquences:
  - Sujet créé automatiquement
  - Étudiant assigné
  - Projet créé en "En attente de cadrage"
  - Réunion de cadrage à planifier
  - Étudiant notifié
- ✅ Checkbox de confirmation obligatoire

3. Remplir les commentaires (optionnel):
```
Excellent projet! Quelques suggestions:
- Prévoir une phase de prototypage pour valider l'interface
- Considérer l'utilisation de scikit-learn en plus de TensorFlow
- Planifier des tests utilisateurs dès le premier sprint
```

4. Cocher la case de confirmation
5. Cliquer sur **"Confirmer l'acceptation"**

**Résultats attendus:**
- ✅ Message de succès
- ✅ Redirection vers "Mes étudiants"
- ✅ **Automatique:** Un Subject a été créé
- ✅ **Automatique:** Une Assignment a été créée
- ✅ **Automatique:** Un Project a été créé en statut "awaiting_kickoff"
- ✅ **Automatique:** L'étudiant a reçu une notification

---

### PARTIE 3: CADRAGE DU PROJET

#### Étape 9: Vérifier "Mes étudiants"
1. Toujours connecté en tant qu'**encadreur**
2. Aller dans **"Mes étudiants"**
3. URL: http://127.0.0.1:8000/projects/supervisor/students/

**Vérifications:**
- ✅ L'étudiant apparaît dans la liste
- ✅ Badge "En attente de cadrage" (orange)
- ✅ Informations de l'étudiant (niveau, filière)
- ✅ Projet associé
- ✅ Bouton "Voir les détails"

#### Étape 10: Accéder au détail de l'étudiant
1. Cliquer sur **"Voir les détails"**
2. URL: http://127.0.0.1:8000/projects/supervisor/student/X/

**Vérifications:**
- ✅ Onglets: Vue d'ensemble / Projet / Jalons / Livrables
- ✅ Informations complètes de l'étudiant
- ✅ Statut du projet: "En attente de cadrage"
- ✅ Alerte orange: "Réunion de cadrage nécessaire"
- ✅ Bouton **"Organiser la réunion de cadrage"**

#### Étape 11: Organiser la réunion de cadrage
1. Cliquer sur **"Organiser la réunion de cadrage"**
2. URL: http://127.0.0.1:8000/projects/X/kickoff/

**Vérifications de la page:**
- ✅ En-tête bleu "Réunion de Cadrage du Projet"
- ✅ Informations projet, étudiant, encadreur
- ✅ Alerte bleue expliquant les objectifs
- ✅ Description du projet
- ✅ Formulaire avec sections:
  - Information sur la réunion (date, lieu)
  - Compte-rendu (discussions, décisions, actions)
  - Planification du suivi (prochaine réunion)

3. Remplir le formulaire:

**Information sur la réunion:**
- **Date et heure:** Aujourd'hui à 14:00
- **Lieu:** "Bureau B203" ou "Salle de réunion A" ou "Teams"

**Compte-rendu:**
- **Points discutés:**
```
Réunion de cadrage du projet de plateforme e-learning avec IA.

Points abordés:
- Architecture globale du système (frontend React, backend Django, ML avec TensorFlow)
- Méthodologie agile avec sprints de 2 semaines
- Technologies validées: Django REST, React, PostgreSQL, Docker, TensorFlow
- Planning: prototype en 2 mois, version beta en 4 mois
- Livrables attendus: cahier des charges, maquettes, prototypes, rapports de sprints

L'étudiant a démontré une bonne compréhension des enjeux techniques.
```

- **Décisions prises:**
```
1. Sprint 1-2: Mise en place de l'infrastructure et architecture de base
2. Sprint 3-4: Développement des fonctionnalités core (authentification, cours, quiz)
3. Sprint 5-6: Intégration du module IA de recommandation
4. Sprint 7-8: Tests, optimisations et documentation
5. Réunions hebdomadaires tous les lundis à 14h
6. Utilisation de GitLab pour le versioning, Jira pour le suivi
```

- **Actions à mener:**
```
Étudiant:
- Installer l'environnement de développement (Django 4.2, React 18, Docker)
- Créer le repository GitLab et configurer CI/CD
- Rédiger le cahier des charges détaillé (deadline: dans 1 semaine)
- Préparer les premières maquettes de l'interface

Encadreur:
- Fournir les ressources sur les algorithmes de recommandation
- Relire le cahier des charges
- Organiser une session sur l'architecture microservices
```

**Planification du suivi:**
- **Date de la prochaine réunion:** Dans 1 semaine (même heure)

4. Cocher la case **"Je confirme que la réunion de cadrage a eu lieu..."**
5. Cliquer sur **"Valider et Démarrer le Projet"** (bouton vert)

**Résultats attendus:**
- ✅ Message de succès: "Réunion de cadrage enregistrée. Le projet est maintenant en cours!"
- ✅ **Automatique:** Meeting créé en base de données
- ✅ **Automatique:** Projet passe de "awaiting_kickoff" à "in_progress"
- ✅ **Automatique:** Étudiant reçoit une notification
- ✅ Redirection vers le détail du projet

---

### PARTIE 4: VÉRIFICATIONS FINALES

#### Étape 12: Vérifier le projet (encadreur)
**Vérifications:**
- ✅ Statut du projet: "En cours" (badge bleu)
- ✅ Plus d'alerte de cadrage
- ✅ Compte-rendu de la réunion visible quelque part
- ✅ Onglets du projet accessibles et fonctionnels

#### Étape 13: Vérifier côté étudiant
1. Se déconnecter
2. Se reconnecter avec le compte **étudiant**
3. Aller dans **"Mes projets"**

**Vérifications:**
- ✅ Le projet créé apparaît
- ✅ Statut: "En cours" (badge bleu)
- ✅ Barre de progression
- ✅ Notification reçue

4. Cliquer sur le projet pour voir les détails

**Vérifications:**
- ✅ Toutes les informations du projet
- ✅ Onglets: jalons, livrables, etc.
- ✅ Possibilité de travailler sur le projet

#### Étape 14: Vérifier "Mes propositions" (étudiant)
1. Aller dans **"Mes propositions"**

**Vérifications:**
- ✅ Statut de la proposition: "Acceptée" (badge vert)
- ✅ Nom de l'encadreur qui a accepté
- ✅ Date d'acceptation
- ✅ Commentaires de l'encadreur visibles

---

## 🧪 TESTS ADDITIONNELS

### Test A: Refus d'une proposition
1. Créer une nouvelle proposition en tant qu'étudiant
2. Se connecter avec un encadreur choisi
3. Aller dans "Propositions reçues"
4. Cliquer sur "Décliner"
5. Remplir des commentaires constructifs
6. Confirmer

**Vérifications:**
- ✅ Proposition passe en "Rejetée"
- ✅ Étudiant notifié avec commentaires
- ✅ Commentaires visibles dans "Mes propositions"
- ✅ Badge rouge "Rejetée"

### Test B: Filtres des propositions (encadreur)
1. Avoir plusieurs propositions (en attente, acceptées, rejetées)
2. Tester les boutons de filtre

**Vérifications:**
- ✅ Filtre "En attente": n'affiche que les propositions pendantes
- ✅ Filtre "Acceptées": n'affiche que les acceptées
- ✅ Filtre "Rejetées": n'affiche que les rejetées
- ✅ Filtre "Toutes": affiche tout

### Test C: Validation des choix d'encadreurs
1. Créer une proposition
2. Essayer de choisir le même encadreur 2 ou 3 fois

**Vérifications:**
- ✅ Message d'erreur: "Vous devez choisir des encadreurs différents"
- ✅ Formulaire non soumis

### Test D: Étudiant avec affectation existante
1. Connecté avec un étudiant qui a déjà un projet
2. Essayer d'accéder à "Proposer un sujet"

**Vérifications:**
- ✅ Message d'avertissement ou redirection
- ✅ Indication qu'il a déjà un projet en cours

---

## 📊 VÉRIFICATIONS EN BASE DE DONNÉES

### Après acceptation de proposition
```sql
-- Vérifier la création automatique
SELECT * FROM subjects_studentproposal WHERE status = 'accepted';
SELECT * FROM subjects_subject WHERE title LIKE '%e-learning%';
SELECT * FROM subjects_assignment ORDER BY created_at DESC LIMIT 1;
SELECT * FROM projects_project WHERE status = 'awaiting_kickoff';
```

### Après réunion de cadrage
```sql
-- Vérifier la réunion et le changement de statut
SELECT * FROM projects_meeting WHERE type = 'kickoff';
SELECT * FROM projects_project WHERE status = 'in_progress';
```

---

## ✅ CHECKLIST COMPLÈTE

### Fonctionnalités étudiants
- [ ] Proposer un sujet - formulaire complet
- [ ] Choisir 1 à 3 encadreurs
- [ ] Justifier le choix
- [ ] Voir "Mes propositions"
- [ ] Voir détail d'une proposition
- [ ] Voir statut (en attente/acceptée/rejetée)
- [ ] Recevoir notification d'acceptation
- [ ] Recevoir notification de refus avec commentaires
- [ ] Voir commentaires de l'encadreur

### Fonctionnalités encadreurs
- [ ] Badge "Propositions reçues" avec compteur
- [ ] Page "Propositions reçues"
- [ ] Filtres par statut
- [ ] Voir détails d'une proposition
- [ ] Accepter une proposition
- [ ] Ajouter des commentaires à l'acceptation
- [ ] Refuser une proposition avec raison
- [ ] Voir "Mes étudiants"
- [ ] Voir badge "En attente de cadrage"
- [ ] Organiser réunion de cadrage
- [ ] Formulaire de cadrage complet
- [ ] Planifier prochaine réunion

### Automatisations
- [ ] Notification aux encadreurs lors de proposition
- [ ] Création automatique du Subject
- [ ] Création automatique de l'Assignment
- [ ] Création automatique du Project (awaiting_kickoff)
- [ ] Notification à l'étudiant lors acceptation
- [ ] Notification à l'étudiant lors refus
- [ ] Création du Meeting lors du cadrage
- [ ] Passage du projet en "in_progress"
- [ ] Notification à l'étudiant du démarrage

### Interface et UX
- [ ] Menus étudiants mis à jour
- [ ] Menus encadreurs mis à jour
- [ ] Badges de compteur fonctionnels
- [ ] Filtres fonctionnels
- [ ] Design responsive
- [ ] Messages de succès/erreur
- [ ] États vides gérés
- [ ] Breadcrumbs et navigation

---

## 🎯 RÉSULTATS ATTENDUS

À la fin de tous ces tests, vous devriez avoir:

1. ✅ Au moins 1 proposition créée et acceptée
2. ✅ Un Subject, Assignment et Project créés automatiquement
3. ✅ Une réunion de cadrage documentée
4. ✅ Un projet passé de "awaiting_kickoff" à "in_progress"
5. ✅ Des notifications envoyées et reçues
6. ✅ Navigation fluide entre toutes les pages
7. ✅ Toutes les informations cohérentes partout

---

## 🐛 PROBLÈMES POTENTIELS

### Si le serveur ne démarre pas
```bash
python manage.py check
python manage.py makemigrations
python manage.py migrate
```

### Si les templates ne s'affichent pas
Vérifier:
- Les fichiers existent bien dans `templates/`
- `TEMPLATES` configuré correctement dans `settings.py`
- Les `{% extends 'base.html' %}` corrects

### Si les formulaires ne fonctionnent pas
Vérifier:
- `{% csrf_token %}` présent
- Méthode POST dans les vues
- Validation des formulaires

### Si les notifications ne sont pas envoyées
Vérifier:
- Les signaux dans `config/signals.py`
- `AppConfig.ready()` charge les signaux
- Le modèle `Notification` existe

---

## 📞 SUPPORT

Si vous rencontrez des problèmes:
1. Vérifier les logs du serveur Django
2. Consulter le fichier `PHASE_1_WORKFLOW_COMPLET.md`
3. Vérifier que toutes les migrations sont appliquées
4. Tester en mode DEBUG=True pour plus d'informations

**Le workflow est maintenant complet et prêt à être testé ! 🎉**
