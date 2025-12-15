# 🧪 Tests - GradEase

Suite de tests pour valider le fonctionnement de l'application.

---

## 📂 Organisation

```
tests/
├── integration/    Tests d'intégration (end-to-end)
├── unit/           Tests unitaires (à venir)
└── archived/       Anciens tests (référence)
```

---

## 🎯 Tests d'Intégration

Tests complets qui valident l'ensemble des fonctionnalités.

### 📄 Fichiers

| Test | Description | Couverture |
|------|-------------|------------|
| `test_toutes_phases_complet.py` ⭐ | **TEST PRINCIPAL** - Toutes les 7 phases | 100% |
| `test_features.py` | Tests des fonctionnalités principales | Phases 1-4 |
| `test_communication.py` | Tests du système de communication | Phase 4 |
| `test_notifications.py` | Tests des notifications email | Phase 4 |
| `test_global_projects.py` | Tests de gestion globale des projets | Phases 3-7 |
| `test_supervisor_interface.py` | Tests de l'interface encadreur | Phase 1 |

### 🚀 Lancer les Tests

#### Test complet recommandé ⭐
```bash
python tests/integration/test_toutes_phases_complet.py
```

Ce test crée automatiquement :
- 9 utilisateurs (1 admin, 4 enseignants, 4 étudiants)
- 1 année académique 2025-2026
- 4 sujets PFE (2 GIT, 2 GESI)
- 3 projets (1 binôme, 2 individuels)
- 1 soutenance complète avec jury
- Notifications et archivage

#### Tests spécifiques
```bash
# Tests des fonctionnalités
python tests/integration/test_features.py

# Tests communication
python tests/integration/test_communication.py

# Tests notifications
python tests/integration/test_notifications.py

# Tests projets globaux
python tests/integration/test_global_projects.py

# Tests interface encadreur
python tests/integration/test_supervisor_interface.py
```

---

## 🔬 Tests Unitaires

**Statut** : À venir

Les tests unitaires Django existants sont dans chaque application :
- `users/tests.py`
- `subjects/tests.py`
- `projects/tests.py`
- `defenses/tests.py`
- `communications/tests.py`
- `archives/tests.py`

### Lancer les tests unitaires Django
```bash
python manage.py test
```

---

## 📦 Tests Archivés

21 anciens tests conservés dans `archived/` pour référence historique.

### Pourquoi archivés ?
- ✅ Redondants avec `test_toutes_phases_complet.py`
- ✅ Obsolètes (anciennes versions)
- ✅ Tests spécifiques déjà couverts

### Liste des tests archivés
```
test_phase1_workflow.py
test_phases_5_6_7.py
test_workflows_complete.py
test_system_complete.py
test_supervisor_planning_fixed.py
test_supervisor_planning_simple.py
test_supervisor_pages.py
test_supervisor_defense_access.py
test_student_workflows.py
test_student_my_projects.py
test_http_pages.py
test_http_registration.py
test_registration_enspd.py
test_new_signals.py
test_new_features.py
test_form_validation.py
test_enspd_impacts.py
test_assignments.py
test_all_workflows.py
test_all_urls.py
test_defenses.py
```

---

## 📊 Couverture par Phase

| Phase | Description | Test Principal | Tests Spécifiques |
|-------|-------------|----------------|-------------------|
| **1** | Authentification & Profils | `test_toutes_phases_complet.py` | `test_features.py` |
| **2** | Système de Jury | `test_toutes_phases_complet.py` | - |
| **3** | Gestion Binômes | `test_toutes_phases_complet.py` | `test_global_projects.py` |
| **4** | Notifications | `test_toutes_phases_complet.py` | `test_communication.py`, `test_notifications.py` |
| **5** | Année Académique | `test_toutes_phases_complet.py` | - |
| **6** | Notation & Archivage | `test_toutes_phases_complet.py` | - |
| **7** | Progression Auto | `test_toutes_phases_complet.py` | - |

---

## 🎓 Données de Test

### Utilisateurs créés

| Rôle | Username | Email | Password |
|------|----------|-------|----------|
| Admin | admin_test | admin.test@enspd.cm | Admin@2025 |
| Professeur | prof_kamga | kamga@enspd.cm | Prof@2025 |
| Professeur | prof_mballa | mballa@enspd.cm | Prof@2025 |
| MCF | mdc_nguyen | nguyen@enspd.cm | Teacher@2025 |
| MCF | mdc_fotso | fotso@enspd.cm | Teacher@2025 |
| Étudiant | etudiant_alice | alice.dupont@enspd.cm | Student@2025 |
| Étudiant | etudiant_bob | bob.martin@enspd.cm | Student@2025 |
| Étudiant | etudiant_carol | carol.nkembe@enspd.cm | Student@2025 |
| Étudiant | etudiant_david | david.tchinda@enspd.cm | Student@2025 |

### Projets créés

1. **Projet Binôme GIT**
   - Alice Dupont (21G00001) + Bob Martin (21G00002)
   - Sujet : "Système de recommandation intelligent avec ML"
   - Encadreur : Prof. Kamga

2. **Projet Individuel GESI**
   - Carol Nkembe (21G00003)
   - Sujet : "Blockchain pour la traçabilité agricole"
   - Encadreur : Prof. Mballa

3. **Projet Individuel GESI**
   - David Tchinda (21G00004)
   - Sujet : "Plateforme e-learning"
   - Encadreur : MCF Nguyen

---

## ✅ Résultats Attendus

### Test Complet (test_toutes_phases_complet.py)

**Sortie terminale** :
```
✅ Phase 1 : Gestion utilisateurs - OK
✅ Phase 2 : Système jury - OK
✅ Phase 3 : Support binômes - OK
✅ Phase 4 : Notifications email - OK
✅ Phase 5 : Année académique - OK
✅ Phase 6 : Notation et archivage - OK
✅ Phase 7 : Progression automatique - OK

📊 RÉSUMÉ
   Tests réussis : 7/7
   Taux de succès : 100%
```

### Critères de succès
- ✅ Aucune erreur de validation Django
- ✅ Toutes les contraintes DB respectées
- ✅ Calculs automatiques corrects
- ✅ Notifications envoyées
- ✅ Signaux déclenchés
- ✅ Archivage automatique fonctionnel

---

## 🔧 Configuration des Tests

### Variables d'environnement
```bash
# Utiliser SQLite pour les tests
export DJANGO_SETTINGS_MODULE=config.settings

# Désactiver les emails en test (optionnel)
export EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

### Base de données de test
Les tests utilisent la base par défaut (`db.sqlite3`).

**Recommandation** : Faire une sauvegarde avant :
```bash
copy db.sqlite3 db.sqlite3.backup
```

---

## 🐛 Dépannage

### Erreur "Users already exist"
```bash
# Option 1 : Réinitialiser la base
python manage.py flush

# Option 2 : Supprimer et recréer
rm db.sqlite3
python manage.py migrate
```

### Erreur "UNIQUE constraint failed"
Les tests créent des utilisateurs avec des noms fixes. Si déjà existants :
```bash
python manage.py flush
```

### Tests lents
Le test complet peut prendre 30-60 secondes car il teste :
- Création de 9 utilisateurs
- 4 sujets + affectations
- 3 projets complets
- Workflow de soutenance
- Archivage

---

## 📈 Métriques de Test

| Métrique | Valeur |
|----------|--------|
| Tests d'intégration actifs | 6 |
| Tests archivés | 21 |
| Couverture phases | 7/7 (100%) |
| Utilisateurs de test | 9 |
| Projets de test | 3 |
| Temps d'exécution (test complet) | ~45 secondes |

---

## 🔄 Workflow de Test Recommandé

### Développement
```bash
# 1. Faire une sauvegarde
copy db.sqlite3 db.sqlite3.backup

# 2. Lancer le test complet
python tests/integration/test_toutes_phases_complet.py

# 3. Vérifier l'interface web
python manage.py runserver
# Tester manuellement avec les identifiants créés

# 4. Restaurer si besoin
copy db.sqlite3.backup db.sqlite3
```

### Avant un commit
```bash
# Tests Django unitaires
python manage.py test

# Test d'intégration complet
python tests/integration/test_toutes_phases_complet.py

# Vérifications supplémentaires
python scripts/diagnostic/check_system.py
```

---

## 📚 Documentation Associée

- **[Plan de Test Détaillé](../docs/tests/PLAN_TEST_DETAILLE.md)** - Documentation complète des tests
- **[Données de Test](../docs/tests/DONNEES_TEST_COMPLETES.md)** - Détails des données créées
- **[Rapport Audit](../docs/tests/RAPPORT_AUDIT_SYSTEME.md)** - Résultats d'audit

---

## 🎯 Prochaines Étapes

### Tests à ajouter
- [ ] Tests unitaires complets dans `unit/`
- [ ] Tests de performance
- [ ] Tests de sécurité
- [ ] Tests de charge

### Amélioration continue
- [ ] Augmenter la couverture de code
- [ ] Automatiser les tests (CI/CD)
- [ ] Tests de régression automatiques
- [ ] Benchmarking des performances

---

**Dernière mise à jour** : 7 décembre 2025  
**Version** : 2.0  
**Statut** : ✅ 100% des phases testées
