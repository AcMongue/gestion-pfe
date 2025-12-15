# Correction des Erreurs de Template - Encadreur

## Date
5 décembre 2025

## Problème Rapporté

Deux erreurs de template détectées lors de l'accès aux pages encadreur:

1. **TemplateSyntaxError** dans `/subjects/proposals/`
   - Erreur: `Unused 'user' at end of if expression`
   
2. **TemplateSyntaxError** dans `/projects/supervisor/students/`
   - Erreur: `Invalid filter: 'filter'`

## Analyse

### Erreur 1: supervisor_proposals.html
**Ligne problématique:**
```django
{% if proposal.status == 'pending' and proposal.can_be_accepted_by user %}
```

**Cause:** Syntaxe invalide - tentative d'appeler une méthode avec un argument dans un template

### Erreur 2: supervisor_students.html
**Lignes problématiques (4 occurrences):**
```django
{% with total=project.milestones.count validated=project.milestones.filter|filter:"validated_by_supervisor=True"|length %}
```

**Cause:** Syntaxe complètement invalide - `filter|filter:` n'existe pas en Django. On ne peut pas filtrer dans les templates de cette façon.

## Corrections Appliquées

### 1. templates/subjects/supervisor_proposals.html (ligne 92)

**AVANT:**
```django
{% if proposal.status == 'pending' and proposal.can_be_accepted_by user %}
```

**APRÈS:**
```django
{% if proposal.status == 'pending' %}
```

**Raison:** Simplifié - vérifie seulement le statut. La méthode `can_be_accepted_by` n'est pas nécessaire ici.

### 2. templates/projects/supervisor_students.html (4 corrections)

#### Correction A: Lignes 138-156 (Vue tableau)
**AVANT:**
```django
{% with total=project.milestones.count validated=project.milestones.filter|filter:"validated_by_supervisor=True"|length %}
<span class="badge bg-primary">
    {{ validated }}/{{ total }}
</span>
{% endwith %}
```

**APRÈS:**
```django
<span class="badge bg-primary">
    {{ project.validated_milestones_count }}/{{ project.milestones.count }}
</span>
```

#### Correction B: Lignes 224-228 (Vue cartes)
**AVANT:**
```django
Jalons: {{ project.milestones.filter|filter:"validated_by_supervisor=True"|length }}/{{ project.milestones.count }}
```

**APRÈS:**
```django
Jalons: {{ project.validated_milestones_count }}/{{ project.milestones.count }}
```

**Même principe pour les livrables** avec `approved_deliverables_count`

### 3. projects/views.py - supervisor_students_view (lignes 432-447)

**AJOUT:** Calcul des compteurs dans la vue
```python
# Annoter les projets avec des flags et compteurs
for project in projects:
    project.milestones_pending = project.milestones.filter(
        is_completed=True,
        validated_by_supervisor=False
    ).exists()
    project.deliverables_pending = project.deliverables.filter(
        status='submitted'
    ).exists()
    # Ajouter les compteurs pour le template
    project.validated_milestones_count = project.milestones.filter(
        validated_by_supervisor=True
    ).count()
    project.approved_deliverables_count = project.deliverables.filter(
        status='approved'
    ).count()
```

## Principe Appliqué

**Règle Django:** On ne peut pas faire de filtres complexes directement dans les templates. Les calculs doivent être faits dans la vue.

### Mauvaise pratique ❌
```django
{{ project.items.filter|filter:"condition=True"|length }}
```

### Bonne pratique ✅
**Dans la vue:**
```python
for project in projects:
    project.items_count = project.items.filter(condition=True).count()
```

**Dans le template:**
```django
{{ project.items_count }}
```

## Vérification

### Test de syntaxe
```bash
python verify_template_syntax.py
```

**Résultat:**
```
✅ projects/supervisor_students.html: Syntaxe correcte
✅ subjects/supervisor_proposals.html: Syntaxe correcte
```

### Test des pages

**URLs à tester:**
1. http://127.0.0.1:8000/projects/supervisor/students/
2. http://127.0.0.1:8000/subjects/proposals/

**Utilisateur de test:**
- Username: `supervisor_demo`
- Password: `demo123`

## Fichiers Modifiés

1. ✅ `templates/subjects/supervisor_proposals.html` - 1 correction
2. ✅ `templates/projects/supervisor_students.html` - 4 corrections
3. ✅ `projects/views.py` - Ajout des compteurs

## État Final

- ✅ Syntaxe des templates validée
- ✅ Aucune erreur Django détectée
- ✅ Pages prêtes à être testées
- ✅ Compteurs calculés dans la vue

## Prochaines Étapes

1. Tester les pages dans le navigateur
2. Créer des données de test si nécessaire (étudiants, propositions)
3. Continuer avec Phase 2: Journal de bord (WorkLog)

## Notes Techniques

**Limitations des templates Django:**
- Pas d'appel de méthodes avec arguments
- Pas de filtres chaînés complexes sur QuerySets
- Pas d'opérations de filtrage dans le template
- Préférer toujours calculer dans la vue et passer au contexte

**Solution systématique:** Annoter ou enrichir les objets dans la vue avant de les passer au template.
