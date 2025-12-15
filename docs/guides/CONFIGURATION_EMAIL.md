# Configuration de l'envoi d'emails avec Gmail

## Étape 1 : Activer la validation en 2 étapes sur votre compte Gmail

1. Allez sur https://myaccount.google.com/security
2. Dans "Connexion à Google", cliquez sur "Validation en 2 étapes"
3. Suivez les instructions pour l'activer

## Étape 2 : Générer un mot de passe d'application

1. Toujours sur https://myaccount.google.com/security
2. Dans "Connexion à Google", cliquez sur "Mots de passe des applications"
3. Sélectionnez "Mail" comme application
4. Sélectionnez "Autre (nom personnalisé)" comme appareil
5. Entrez "GradEase" comme nom
6. Cliquez sur "Générer"
7. **COPIEZ** le mot de passe de 16 caractères généré (vous ne pourrez plus le revoir)

## Étape 3 : Configurer le fichier .env

Modifiez le fichier `.env` à la racine du projet :

```env
EMAIL_HOST_USER=votre.email@gmail.com
EMAIL_HOST_PASSWORD=xxxx xxxx xxxx xxxx  # Le mot de passe d'application généré (16 caractères)
EMAIL_USE_GMAIL=True
```

**Exemple :**
```env
EMAIL_HOST_USER=gradease.enspd@gmail.com
EMAIL_HOST_PASSWORD=abcd efgh ijkl mnop
EMAIL_USE_GMAIL=True
```

## Étape 4 : Redémarrer le serveur Django

```bash
# Arrêtez le serveur (CTRL+C)
# Puis redémarrez-le
python manage.py runserver
```

## Étape 5 : Tester l'envoi d'emails

1. Allez sur la page de connexion
2. Cliquez sur "Mot de passe oublié ?"
3. Entrez l'email d'un utilisateur existant
4. Vérifiez votre boîte de réception

## Alternative : Mode Console (Développement)

Si vous ne voulez pas configurer Gmail, laissez `EMAIL_USE_GMAIL=False` dans le `.env`.
Les emails seront affichés dans la console du serveur Django.

## Sécurité

⚠️ **IMPORTANT** : 
- Ne partagez JAMAIS votre mot de passe d'application
- Le fichier `.env` est dans `.gitignore` pour éviter qu'il soit commité
- Utilisez un compte Gmail dédié pour l'application, pas votre compte personnel

## Dépannage

### Erreur "SMTPAuthenticationError"
- Vérifiez que la validation en 2 étapes est activée
- Vérifiez que vous utilisez bien le mot de passe d'application (pas votre mot de passe Gmail normal)
- Assurez-vous qu'il n'y a pas d'espaces au début/fin du mot de passe

### Erreur "Connection refused"
- Vérifiez votre connexion Internet
- Vérifiez que le port 587 n'est pas bloqué par votre pare-feu

### Les emails vont dans les spams
- C'est normal pour un serveur de développement
- En production, configurez SPF, DKIM et DMARC pour votre domaine
