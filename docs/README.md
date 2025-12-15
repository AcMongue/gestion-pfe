# 📚 Documentation GradEase

**Application de Gestion des Projets de Fin d'Études - ENSPD**

---

## 📂 Structure de la Documentation

```
docs/
├── README.md                    # ← Vous êtes ici
├── guides/                      # Guides d'utilisation
│   ├── MANUEL_UTILISATEUR.md   # Guide complet pour tous les utilisateurs
│   ├── GUIDE_ADMIN_DJANGO.md   # Administration Django
│   ├── DEMARRAGE_RAPIDE.md     # Quick start
│   └── COMMANDES_RAPIDES.md    # Commandes courantes
│
├── implementation/              # Documentation technique
│   ├── IMPLEMENTATION_COMPLETE.md      # Implémentation complète du système
│   ├── PHASES_5_6_7_COMPLETE.md       # Phases 5-7 (Année, notation, archivage)
│   ├── BINOMES_MATERIALISATION.md     # Système de binômes
│   └── PHASE_1_WORKFLOW_COMPLET.md    # Workflow authentification
│
├── tests/                       # Documentation de test
│   ├── PLAN_TEST_DETAILLE.md           # Plan de test complet
│   ├── RAPPORT_AUDIT_SYSTEME.md        # Audit système
│   └── RAPPORT_TESTS_INTERFACE_ETUDIANT.md
│
└── archived/                    # Archives (anciennes versions)
```

---

## 🚀 Démarrage Rapide

### Pour commencer
1. **Installation** : Voir [DEMARRAGE_RAPIDE.md](guides/DEMARRAGE_RAPIDE.md)
2. **Utilisation** : Voir [MANUEL_UTILISATEUR.md](guides/MANUEL_UTILISATEUR.md)
3. **Commandes** : Voir [COMMANDES_RAPIDES.md](guides/COMMANDES_RAPIDES.md)

### Pour les développeurs
1. **Architecture** : Voir [IMPLEMENTATION_COMPLETE.md](implementation/IMPLEMENTATION_COMPLETE.md)
2. **Tests** : Voir [PLAN_TEST_DETAILLE.md](tests/PLAN_TEST_DETAILLE.md)
3. **Admin Django** : Voir [GUIDE_ADMIN_DJANGO.md](guides/GUIDE_ADMIN_DJANGO.md)

---

## 📖 Guides par Rôle

### 👨‍🎓 Étudiants
- Inscription et connexion
- Choix de sujets PFE
- Gestion de projet (jalons, livrables)
- Soumission de mémoire
- Préparation soutenance

→ [MANUEL_UTILISATEUR.md](guides/MANUEL_UTILISATEUR.md#étudiants)

### 👨‍🏫 Enseignants (Encadreurs)
- Proposer des sujets
- Valider les affectations
- Suivre les projets
- Valider jalons et livrables
- Organiser soutenances
- Notation

→ [MANUEL_UTILISATEUR.md](guides/MANUEL_UTILISATEUR.md#enseignants)

### 👔 Administrateurs
- Gestion des utilisateurs
- Création années académiques
- Planification soutenances
- Archivage et rapports

→ [GUIDE_ADMIN_DJANGO.md](guides/GUIDE_ADMIN_DJANGO.md)

---

## 🎯 Fonctionnalités Principales

### ✅ Phase 1 : Authentification et Profils
- Système de rôles (étudiant, enseignant, admin)
- Profils personnalisés avec matricule
- Hiérarchie académique

### ✅ Phase 2 : Système de Jury
- Composition jury 3 membres (président, examinateur, rapporteur)
- Validation : seul un Professeur peut présider
- Limite 4 présidences/jour/enseignant

### ✅ Phase 3 : Gestion des Binômes
- Projets individuels ou binômes
- Validation filière (même filière si mono-disciplinaire)
- Interface visuelle claire (badges BINÔME/INDIVIDUEL)

### ✅ Phase 4 : Notifications Email
- 10 types de notifications automatiques
- Templates HTML personnalisés
- Pièces jointes (mémoires PDF)

### ✅ Phase 5 : Année Académique et Mémoires
- Gestion années académiques
- Workflow mémoire : soumission → approbation → distribution
- Deadline automatique

### ✅ Phase 6 : Notation et Archivage
- Interface notation pour jury
- Calcul automatique note finale
- Archivage automatique après notation complète

### ✅ Phase 7 : Progression Automatique
- Calcul progression basé sur jalons validés
- Mise à jour automatique (Django signals)
- Formule : (jalons validés / total jalons) × 100

---

## 🧪 Tests

### Tests Principaux
- **test_toutes_phases_complet.py** : Test complet des 7 phases
- **test_features.py** : Tests fonctionnalités
- **test_communication.py** : Tests notifications
- **test_notifications.py** : Tests emails
- **test_global_projects.py** : Tests projets globaux
- **test_supervisor_interface.py** : Interface encadreur

### Tests Archivés
Les anciens tests sont dans `tests/archived/` pour référence historique.

→ [PLAN_TEST_DETAILLE.md](tests/PLAN_TEST_DETAILLE.md)

---

## 🛠️ Commandes Courantes

```bash
# Démarrer le serveur
python manage.py runserver

# Créer un superuser
python manage.py createsuperuser

# Migrations
python manage.py makemigrations
python manage.py migrate

# Tests complets
python test_toutes_phases_complet.py

# Shell Django
python manage.py shell
```

→ [COMMANDES_RAPIDES.md](guides/COMMANDES_RAPIDES.md)

---

## 📊 Architecture Technique

### Backend
- **Framework** : Django 4.2.27
- **Base de données** : MySQL (production) / SQLite (développement)
- **Python** : 3.11+

### Applications Django
```
users/          # Authentification et profils
subjects/       # Catalogue sujets et affectations
projects/       # Gestion projets, jalons, livrables
defenses/       # Soutenances et jury
communications/ # Notifications et messages
archives/       # Archivage projets
```

### Frontend
- **HTML5** + **CSS3** + **JavaScript** (vanilla)
- **Bootstrap 5.3**
- **Font Awesome 6.4**

→ [IMPLEMENTATION_COMPLETE.md](implementation/IMPLEMENTATION_COMPLETE.md)

---

## 🔑 Identifiants de Test

### Comptes par défaut (après script de test)
```
Admin       : admin_test / Admin@2025
Professeur  : prof_kamga / Prof@2025
MCF         : mdc_nguyen / Teacher@2025
Étudiant    : etudiant_alice / Student@2025
```

→ [PLAN_TEST_DETAILLE.md](tests/PLAN_TEST_DETAILLE.md#identifiants-pour-tests-manuels)

---

## 📝 Changelog

### Version 2.0 (Décembre 2025)
- ✅ Phases 5-7 implémentées
- ✅ Système binômes amélioré visuellement
- ✅ Nom application : **GradEase**
- ✅ Documentation réorganisée

### Version 1.0 (Novembre 2025)
- ✅ Phases 1-4 implémentées
- ✅ Système de base fonctionnel
- ✅ Tests complets

---

## 🆘 Support et Contacts

### Problèmes courants
Voir [GUIDE_ADMIN_DJANGO.md](guides/GUIDE_ADMIN_DJANGO.md#dépannage)

### Contribuer
1. Créer une branche feature
2. Implémenter les changements
3. Tester avec `test_toutes_phases_complet.py`
4. Créer une Pull Request

---

**Dernière mise à jour** : 7 décembre 2025  
**Version** : 2.0  
**Statut** : ✅ Production Ready
