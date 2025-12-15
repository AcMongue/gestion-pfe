# Guide de gestion des emails multiples

## Problème : Plusieurs comptes avec le même email

### Solution actuelle (IMPLÉMENTÉE) ✅

Quand un utilisateur demande une réinitialisation avec un email partagé par plusieurs comptes :

**Le système envoie un email séparé pour CHAQUE compte**

Exemple : Si `jean@email.com` est utilisé par 3 comptes (`jean.student`, `jean.teacher`, `jean.admin`), l'utilisateur recevra **3 emails distincts**, un pour chaque compte.

### Fonctionnement détaillé

1. **Utilisateur demande réinitialisation** pour `jean@email.com`

2. **Système détecte 3 comptes** avec cet email

3. **Système envoie 3 emails** :
   ```
   Email 1 : Pour le compte "jean.student"
   Email 2 : Pour le compte "jean.teacher"  
   Email 3 : Pour le compte "jean.admin"
   ```

4. **Chaque email indique clairement** :
   - ⚠️ Qu'il y a plusieurs comptes avec cet email
   - 📝 Le nom d'utilisateur concerné par CE lien
   - 🔗 Un lien unique pour CE compte spécifique

5. **L'utilisateur choisit** quel lien cliquer selon le compte qu'il veut réinitialiser

### Avantages de cette approche

✅ **Sécurité** : Chaque compte a son propre token
✅ **Clarté** : L'utilisateur sait quel compte il réinitialise
✅ **Flexibilité** : Peut réinitialiser un ou tous ses comptes
✅ **Traçabilité** : Logs indiquent quand plusieurs comptes sont détectés

### Monitoring

Le système log automatiquement quand plusieurs comptes partagent un email :

```
⚠️  ATTENTION: 3 comptes utilisent l'email jean@email.com
   Comptes: jean.student, jean.teacher, jean.admin
✅ Email de réinitialisation envoyé à jean@email.com (compte: jean.student)
✅ Email de réinitialisation envoyé à jean@email.com (compte: jean.teacher)
✅ Email de réinitialisation envoyé à jean@email.com (compte: jean.admin)
```

---

## Meilleure pratique : Email unique par compte

### Pourquoi imposer des emails uniques ?

1. **Sécurité** : Un email = une personne = un compte
2. **Communication claire** : Pas de confusion sur le destinataire
3. **Conformité RGPD** : Identification claire de la personne
4. **Gestion simplifiée** : Pas de cas particuliers

### Comment migrer vers des emails uniques

**Option 1 : Migration en douceur (RECOMMANDÉ)**

1. Identifier les doublons actuels :
```python
python manage.py shell
>>> from users.models import User
>>> from django.db.models import Count
>>> duplicates = User.objects.values('email').annotate(count=Count('email')).filter(count__gt=1)
>>> for dup in duplicates:
...     print(f"Email {dup['email']}: {dup['count']} comptes")
```

2. Contacter les utilisateurs concernés pour qu'ils mettent à jour leurs emails

3. Une fois résolus, ajouter la contrainte unique

**Option 2 : Migration forcée**

1. Créer une migration pour rendre l'email unique
2. Avant de l'appliquer, générer des emails temporaires pour les doublons
3. Envoyer un email aux utilisateurs pour qu'ils mettent à jour

### Ajouter la contrainte unique

Une fois les doublons résolus, modifiez le modèle User :

```python
# users/models.py
class User(AbstractUser):
    email = models.EmailField(
        _('adresse email'),
        unique=True,  # Ajouter cette contrainte
        help_text='Email unique pour chaque compte'
    )
```

Puis créez et appliquez la migration :
```bash
python manage.py makemigrations
python manage.py migrate
```

---

## Résumé

**Solution actuelle** : ✅ Fonctionne avec ou sans doublons
- Envoie un email par compte
- Indique clairement quel compte est concerné
- Sécurisé et transparent

**Recommandation long terme** : 
- Imposer `unique=True` sur le champ email
- Évite les problèmes de confusion
- Meilleure pratique industrielle

**Le système actuel gère les deux cas de manière professionnelle !** 🎯
