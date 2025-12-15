# 🎓 GradEase - Gestion des PFE ENSPD

**Système complet de gestion des Projets de Fin d'Études**  
École Nationale Supérieure Polytechnique de Douala

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-4.2.27-green.svg)](https://www.djangoproject.com/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple.svg)](https://getbootstrap.com/)
[![Status](https://img.shields.io/badge/Status-Production%20Ready-success.svg)]()

---

## 📋 Table des matières

- [Vue d'ensemble](#-vue-densemble)
- [Installation rapide](#-installation-rapide)
- [Documentation](#-documentation)
- [Fonctionnalités](#-fonctionnalités)
- [Tests](#-tests)
- [Structure](#-structure-du-projet)
- [Support](#-support)

---

## 🎯 Vue d'ensemble

**GradEase** est une plateforme complète de gestion des projets de fin d'études qui couvre l'ensemble du workflow :

```
Choix sujet → Affectation → Suivi projet → Soutenance → Archivage
```

### Stack Technique
- **Backend** : Django 4.2.27 (Python 3.11+)
- **Frontend** : HTML5, CSS3, JavaScript + Bootstrap 5.3
- **Base de données** : MySQL (production) / SQLite (développement)
- **Architecture** : Monolithique 2-tiers

---

## ⚡ Installation rapide

### Prérequis
- Python 3.11+
- MySQL (optionnel, SQLite par défaut)
- Git

### Étapes

```bash
# 1. Cloner le projet
git clone https://github.com/AcMongue/gestion-pfe.git
cd gestion-pfe

# 2. Créer et activer l'environnement virtuel
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Appliquer les migrations
python manage.py migrate

# 5. Créer un superuser
python manage.py createsuperuser

# 6. Lancer le serveur
python manage.py runserver
```

**Accéder à l'application** : http://127.0.0.1:8000/

👉 **Guide détaillé** : [docs/guides/DEMARRAGE_RAPIDE.md](docs/guides/DEMARRAGE_RAPIDE.md)

---

## 📚 Documentation

Toute la documentation est organisée dans le dossier `docs/` :

### 📖 Guides Utilisateur
- **[Manuel Utilisateur](docs/guides/MANUEL_UTILISATEUR.md)** - Guide complet par rôle
- **[Démarrage Rapide](docs/guides/DEMARRAGE_RAPIDE.md)** - Installation et configuration
- **[Commandes Rapides](docs/guides/COMMANDES_RAPIDES.md)** - Commandes courantes
- **[Guide Admin Django](docs/guides/GUIDE_ADMIN_DJANGO.md)** - Administration avancée

### 🔧 Documentation Technique
- **[Implémentation Complète](docs/implementation/IMPLEMENTATION_COMPLETE.md)** - Architecture système
- **[Phases 5-6-7](docs/implementation/PHASES_5_6_7_COMPLETE.md)** - Année académique, notation, archivage
- **[Système Binômes](docs/implementation/BINOMES_MATERIALISATION.md)** - Gestion des binômes
- **[Workflow Phase 1](docs/implementation/PHASE_1_WORKFLOW_COMPLET.md)** - Authentification

### 🧪 Tests
- **[Plan de Test Détaillé](docs/tests/PLAN_TEST_DETAILLE.md)** - Tests complets des 7 phases
- **[Rapport Audit Système](docs/tests/RAPPORT_AUDIT_SYSTEME.md)** - Audit complet

👉 **Index complet** : [docs/README.md](docs/README.md)

---

## ✨ Fonctionnalités

### 👤 Gestion des Utilisateurs
- ✅ 3 rôles : Étudiant, Enseignant, Admin
- ✅ Hiérarchie académique (Professeur, MCF, Assistant)
- ✅ Profils personnalisés avec matricule (format `21G00001`)

### 📚 Catalogue de Sujets
- ✅ Proposition de sujets par encadreurs
- ✅ Support binômes et projets interdisciplinaires
- ✅ Validation et affectation automatisée

### 🚀 Suivi de Projets
- ✅ Gestion jalons avec validation encadreur
- ✅ Soumission livrables (documents, code)
- ✅ **Progression automatique** basée sur jalons validés
- ✅ **Système binômes** visuellement matérialisé

### 🎓 Soutenances
- ✅ Composition jury (président, examinateur, rapporteur)
- ✅ Validation : seul un **Professeur** peut présider
- ✅ Interface notation pour jury
- ✅ Calcul automatique note finale

### 📧 Communication
- ✅ Notifications email automatiques (10 types)
- ✅ Templates HTML personnalisés
- ✅ Pièces jointes (mémoires PDF)

### 📁 Archivage
- ✅ **Archivage automatique** après notation complète
- ✅ Détection semestre (S1/S2)
- ✅ Rapports et statistiques

### 📅 Année Académique
- ✅ Gestion années avec deadlines
- ✅ Workflow mémoire : soumission → approbation → distribution
- ✅ Validation dates et délais

---

## 🧪 Tests

### Lancer les tests complets

```bash
# Test de toutes les phases (recommandé) ⭐
python tests/integration/test_toutes_phases_complet.py

# Tests Django unitaires
python manage.py test

# Tests spécifiques
python tests/integration/test_features.py
python tests/integration/test_communication.py
python tests/integration/test_notifications.py
```

### Données de test

Le script `test_toutes_phases_complet.py` crée automatiquement :
- 9 utilisateurs (1 admin, 4 enseignants, 4 étudiants)
- 1 année académique 2025-2026
- 4 sujets (2 GIT, 2 GESI)
- 3 projets (1 binôme, 2 individuels)
- 1 soutenance complète avec jury

**Identifiants de test** :
```
Admin      : admin_test / Admin@2025
Professeur : prof_kamga / Prof@2025
Étudiant   : etudiant_alice / Student@2025
```

👉 **Documentation tests** : [tests/README.md](tests/README.md)  
👉 **Plan détaillé** : [docs/tests/PLAN_TEST_DETAILLE.md](docs/tests/PLAN_TEST_DETAILLE.md)

---

## 📂 Structure du Projet

```
gestion-pfe/
├── manage.py           # ⭐ Script principal Django
│
├── 📁 Applications Django
│   ├── users/              # Authentification et profils
│   ├── subjects/           # Catalogue sujets et affectations
│   ├── projects/           # Gestion projets, jalons, livrables
│   ├── defenses/           # Soutenances et jury
│   ├── communications/     # Notifications et messages
│   ├── archives/           # Archivage projets
│   └── config/             # Configuration Django
│
├── 📚 Documentation (docs/)
│   ├── README.md           # Index principal
│   ├── guides/             # Guides utilisateur (5)
│   ├── implementation/     # Documentation technique (7)
│   ├── tests/              # Documentation tests (7)
│   └── archived/           # Archives (13)
│
├── 🐍 Scripts (scripts/)
│   ├── README.md           # Documentation scripts
│   ├── setup/              # Configuration système (4)
│   ├── diagnostic/         # Vérification & analyse (7)
│   └── data/               # Création données test (4)
│
├── 🧪 Tests (tests/)
│   ├── README.md           # Documentation tests
│   ├── integration/        # Tests d'intégration (6)
│   └── archived/           # Anciens tests (21)
│
├── 🎨 Frontend
│   ├── templates/          # Templates HTML
│   ├── static/             # CSS, JS, images
│   └── media/              # Fichiers uploadés
│
└── 📄 Configuration
    ├── requirements.txt    # Dépendances Python
    ├── .env.example        # Variables d'environnement
    └── README.md           # ← Vous êtes ici
```

---

## 🆘 Support

### Problèmes courants

**Erreur de migration** :
```bash
python manage.py migrate --run-syncdb
```

**Réinitialiser la base** :
```bash
python manage.py flush
python manage.py migrate
```

**Créer des données de test** :
```bash
python scripts/data/create_test_data.py
```

**Vérifier le système** :
```bash
python scripts/diagnostic/check_system.py
```

### Ressources
- 📖 [Manuel Utilisateur](docs/guides/MANUEL_UTILISATEUR.md)
- 🔧 [Guide Admin](docs/guides/GUIDE_ADMIN_DJANGO.md)
- 🧪 [Documentation Tests](tests/README.md)
- 🐍 [Documentation Scripts](scripts/README.md)
- 💬 Issues GitHub : [github.com/AcMongue/gestion-pfe/issues](https://github.com/AcMongue/gestion-pfe/issues)

---

## 🗂️ Fichiers & Dossiers Principaux

### 🎯 Essentiels
| Fichier/Dossier | Description |
|-----------------|-------------|
| `manage.py` | Script de gestion Django |
| `requirements.txt` | Dépendances Python |
| `db.sqlite3` | Base de données (développement) |

### 🧪 Tests ([tests/](tests/))
| Fichier | Description |
|---------|-------------|
| `integration/test_toutes_phases_complet.py` ⭐ | Test complet des 7 phases |
| `integration/test_features.py` | Tests fonctionnalités |
| `integration/test_communication.py` | Tests notifications |

### 🐍 Scripts ([scripts/](scripts/))

**Configuration** ([scripts/setup/](scripts/setup/))
- `set_admin_password.py` - Réinitialiser mot de passe admin
- `set_student_levels.py` - Définir niveaux étudiants
- `update_subjects_status.py` - Mettre à jour statuts

**Diagnostic** ([scripts/diagnostic/](scripts/diagnostic/))
- `check_system.py` - Vérification système complète
- `analyze_workflows.py` - Analyser flux de travail
- `audit_projects.py` - Auditer les projets

**Données** ([scripts/data/](scripts/data/))
- `create_test_data.py` - Créer données de test
- `create_test_projects.py` - Créer projets de test

---

## 👥 Contributeurs

**Développement** : Équipe ENSPD  
**Version** : 2.0  
**Date** : Décembre 2025  
**Statut** : ✅ Production Ready

---

## 📄 Licence

Ce projet est destiné à l'usage interne de l'ENSPD.

---

## 🚀 Quick Start

```bash
# Installation complète en 3 commandes
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

# Accéder : http://127.0.0.1:8000
```

**Premier pas ?** → [docs/guides/DEMARRAGE_RAPIDE.md](docs/guides/DEMARRAGE_RAPIDE.md)

---

<div align="center">
<b>Développé avec ❤️ pour l'ENSPD</b><br>
<i>GradEase - Simplifier la gestion des PFE</i>
</div>
