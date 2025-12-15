# Test des Formulaires d'Inscription ENSPD

## Modifications Effectuées ✅

### 1. Formulaire UserRegistrationForm (users/forms.py)
- ✅ Ajout de la liste déroulante pour **filière/département** (9 filières ENSPD)
- ✅ Ajout de la liste déroulante pour **grade académique** (4 titres)
- ✅ Ajout de la liste déroulante pour **niveau** (L3, M2, DOC)
- ✅ Champs dynamiques selon le rôle:
  - **Étudiants**: matricule, niveau, filière
  - **Encadreurs**: filière (département), grade académique, spécialité, max étudiants
  - **Admins**: filière (département)
- ✅ Validation automatique selon le rôle

### 2. Template d'Inscription (templates/users/register.html)
- ✅ Interface divisée en sections par rôle
- ✅ JavaScript pour afficher/masquer les champs selon le rôle sélectionné
- ✅ Labels clarifiés (département au lieu de filière pour encadreurs/admins)
- ✅ Alertes informatives par type d'utilisateur

### 3. Formulaire UserUpdateForm (users/forms.py)
- ✅ Listes déroulantes pour filière, grade académique, niveau
- ✅ Masquage automatique des champs non pertinents selon le rôle

## Les 9 Filières de l'ENSPD

Les utilisateurs peuvent maintenant choisir parmi:
1. **GIT** - Génie Informatique & Télécommunications
2. **GESI** - Génie Électrique et Systèmes Intelligents
3. **GQHSEI** - Génie de la Qualité Hygiène, Sécurité et Environnement Industriel
4. **GAM** - Génie Automobile et Mécatronique
5. **GMP** - Génie Maritime et Portuaire
6. **GP** - Génie des Procédés
7. **GE** - Génie Énergétique
8. **GM** - Génie Mécanique
9. **GC** - Génie Civil

## Les 4 Grades Académiques

Pour les encadreurs:
1. **Assistant**
2. **Maître Assistant**
3. **Maître de Conférences**
4. **Professeur** (seul ce grade peut être président de jury)

## Test Manuel

### URL: http://127.0.0.1:8000/users/register/

### Test 1: Inscription Étudiant
1. Ouvrir la page d'inscription
2. Sélectionner le rôle **Étudiant**
3. Vérifier que les champs suivants apparaissent:
   - ✅ Matricule (texte)
   - ✅ Niveau (liste déroulante: L3, M2, DOC)
   - ✅ Filière (liste déroulante: 9 filières)
4. Vérifier que les champs encadreurs/admins sont masqués
5. Remplir le formulaire et soumettre
6. Vérifier que la validation fonctionne (champs obligatoires)

### Test 2: Inscription Encadreur
1. Ouvrir la page d'inscription
2. Sélectionner le rôle **Encadreur**
3. Vérifier que les champs suivants apparaissent:
   - ✅ Département (liste déroulante: 9 filières)
   - ✅ Grade Académique (liste déroulante: 4 grades)
   - ✅ Spécialité (texte)
   - ✅ Max étudiants (nombre, défaut: 5)
4. Vérifier que les champs étudiants sont masqués
5. Remplir le formulaire et soumettre
6. Vérifier que la validation fonctionne

### Test 3: Inscription Admin
1. Ouvrir la page d'inscription
2. Sélectionner le rôle **Administration**
3. Vérifier que seul le champ **Département** apparaît
4. Vérifier que tous les autres champs spécifiques sont masqués
5. Remplir le formulaire et soumettre

### Test 4: Changement de Rôle Dynamique
1. Ouvrir la page d'inscription
2. Sélectionner **Étudiant** → vérifier les champs affichés
3. Changer pour **Encadreur** → vérifier que les champs changent
4. Changer pour **Admin** → vérifier que les champs changent
5. Revenir à **Étudiant** → vérifier que les champs sont corrects

## Vérification Base de Données

```sql
-- Vérifier les filières des étudiants
SELECT username, role, filiere, level FROM users_user WHERE role = 'student';

-- Vérifier les départements et grades des encadreurs
SELECT username, role, filiere, academic_title, specialite FROM users_user WHERE role = 'supervisor';

-- Vérifier les départements des admins
SELECT username, role, filiere FROM users_user WHERE role = 'admin';
```

## Prochaines Étapes

1. ✅ Formulaires avec listes déroulantes - COMPLÉTÉ
2. ⏳ Filtrage des encadreurs par département (vues)
3. ⏳ Support des projets interdisciplinaires
4. ⏳ Validation des jurys (président = Professeur uniquement)
5. ⏳ Détection des conflits de planning des soutenances

## Notes Importantes

- Le champ `filiere` est utilisé pour:
  - Les **étudiants**: leur filière d'études
  - Les **encadreurs**: leur département d'appartenance
  - Les **admins**: leur département de gestion

- Le champ `department` n'existe pas dans le modèle - on utilise `filiere` pour tous

- Les valeurs des rôles dans la base de données sont en minuscules:
  - `'student'` (pas `'STUDENT'`)
  - `'supervisor'` (pas `'SUPERVISOR'`)
  - `'admin'` (pas `'ADMIN'`)

## Statut

✅ **FORMULAIRES COMPLETS ET FONCTIONNELS**

Le serveur démarre sans erreur. Les formulaires utilisent maintenant des listes déroulantes pour:
- Filière/département (9 choix)
- Grade académique (4 choix)
- Niveau étudiant (3 choix)

Les champs apparaissent/disparaissent dynamiquement selon le rôle sélectionné.
