# 🛠️ Scripts - GradEase

Scripts utilitaires pour la gestion et maintenance de l'application.

---

## 📂 Organisation

```
scripts/
├── setup/          Configuration et initialisation
├── diagnostic/     Vérification et analyse système
└── data/           Création de données de test
```

---

## ⚙️ Setup (Configuration)

Scripts pour configurer et initialiser le système.

### 📄 Fichiers

| Script | Description | Usage |
|--------|-------------|-------|
| `set_admin_password.py` | Réinitialiser le mot de passe admin | `python scripts/setup/set_admin_password.py` |
| `set_student_levels.py` | Définir les niveaux des étudiants | `python scripts/setup/set_student_levels.py` |
| `fix_student_levels.py` | Corriger les niveaux invalides | `python scripts/setup/fix_student_levels.py` |
| `update_subjects_status.py` | Mettre à jour le statut des sujets | `python scripts/setup/update_subjects_status.py` |

### 🚀 Exemples

```bash
# Réinitialiser le mot de passe admin
python scripts/setup/set_admin_password.py

# Mettre à jour les niveaux étudiants
python scripts/setup/set_student_levels.py
```

---

## 🔍 Diagnostic (Vérification)

Scripts pour diagnostiquer et analyser le système.

### 📄 Fichiers

| Script | Description | Usage |
|--------|-------------|-------|
| `check_system.py` | Vérification complète du système | `python scripts/diagnostic/check_system.py` |
| `diagnostic_workflow.py` | Diagnostiquer les workflows | `python scripts/diagnostic/diagnostic_workflow.py` |
| `diagnostic_problemes.py` | Identifier les problèmes | `python scripts/diagnostic/diagnostic_problemes.py` |
| `analyze_workflows.py` | Analyser les flux de travail | `python scripts/diagnostic/analyze_workflows.py` |
| `audit_projects.py` | Auditer les projets | `python scripts/diagnostic/audit_projects.py` |
| `debug_subjects.py` | Déboguer les sujets | `python scripts/diagnostic/debug_subjects.py` |
| `verify_template_syntax.py` | Vérifier la syntaxe des templates | `python scripts/diagnostic/verify_template_syntax.py` |

### 🚀 Exemples

```bash
# Vérifier l'état du système
python scripts/diagnostic/check_system.py

# Analyser les workflows
python scripts/diagnostic/analyze_workflows.py

# Auditer les projets
python scripts/diagnostic/audit_projects.py
```

---

## 📊 Data (Données de Test)

Scripts pour créer des données de test et démonstration.

### 📄 Fichiers

| Script | Description | Usage |
|--------|-------------|-------|
| `create_test_data.py` | Créer données de test complètes | `python scripts/data/create_test_data.py` |
| `create_test_projects.py` | Créer des projets de test | `python scripts/data/create_test_projects.py` |
| `create_demo_supervisor.py` | Créer un encadreur de démo | `python scripts/data/create_demo_supervisor.py` |
| `guide_test_manuel.py` | Guide pour tests manuels | `python scripts/data/guide_test_manuel.py` |

### 🚀 Exemples

```bash
# Créer des données de test complètes
python scripts/data/create_test_data.py

# Créer des projets de démonstration
python scripts/data/create_test_projects.py
```

---

## 📋 Commandes Courantes

### Configuration initiale
```bash
# 1. Réinitialiser admin
python scripts/setup/set_admin_password.py

# 2. Créer données de test
python scripts/data/create_test_data.py

# 3. Vérifier le système
python scripts/diagnostic/check_system.py
```

### Maintenance
```bash
# Vérifier l'état du système
python scripts/diagnostic/check_system.py

# Mettre à jour les statuts
python scripts/setup/update_subjects_status.py

# Analyser les workflows
python scripts/diagnostic/analyze_workflows.py
```

### Dépannage
```bash
# Diagnostiquer les problèmes
python scripts/diagnostic/diagnostic_problemes.py

# Vérifier les templates
python scripts/diagnostic/verify_template_syntax.py

# Auditer les projets
python scripts/diagnostic/audit_projects.py
```

---

## ⚠️ Notes Importantes

### Environnement virtuel
Toujours activer l'environnement virtuel avant d'exécuter les scripts :

```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### Base de données
Les scripts de setup et data peuvent modifier la base de données. Faites une sauvegarde avant :

```bash
# Sauvegarder
copy db.sqlite3 db.sqlite3.backup

# Restaurer si besoin
copy db.sqlite3.backup db.sqlite3
```

### Ordre d'exécution
Pour une installation complète :
1. Setup (configuration)
2. Data (données de test)
3. Diagnostic (vérification)

---

## 🆘 Support

### Problèmes courants

**Script introuvable** :
```bash
# Vérifier le chemin
python scripts/setup/set_admin_password.py
```

**Erreur d'import** :
```bash
# S'assurer que manage.py est accessible
export DJANGO_SETTINGS_MODULE=config.settings  # Linux
$env:DJANGO_SETTINGS_MODULE="config.settings"  # Windows
```

**Base de données verrouillée** :
```bash
# Arrêter le serveur Django
# Puis relancer le script
```

---

## 📚 Documentation Associée

- [Guide Utilisateur](../docs/guides/MANUEL_UTILISATEUR.md)
- [Guide Admin](../docs/guides/GUIDE_ADMIN_DJANGO.md)
- [Commandes Rapides](../docs/guides/COMMANDES_RAPIDES.md)
- [Tests](../tests/README.md)

---

**Dernière mise à jour** : 7 décembre 2025  
**Version** : 2.0
