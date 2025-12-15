# Guide de test - Système de réinitialisation de mot de passe

## Mode actuel : CONSOLE (Développement)

Le système fonctionne en **mode console** où les emails s'affichent dans le terminal au lieu d'être envoyés par email.

---

## 🧪 Test manuel via l'interface web

### Étape 1 : Aller sur la page de réinitialisation

1. Démarrez le serveur : `python manage.py runserver`
2. Ouvrez http://localhost:8000/users/login/
3. Cliquez sur **"Mot de passe oublié ?"**

### Étape 2 : Demander la réinitialisation

1. Entrez l'email d'un utilisateur existant
2. Cliquez sur **"Envoyer le lien"**
3. Vous serez redirigé vers une page de confirmation

### Étape 3 : Récupérer le lien

**Dans la console du serveur Django**, vous verrez quelque chose comme :

```
Content-Type: text/plain; charset="utf-8"
MIME-Version: 1.0
Content-Transfer-Encoding: 7bit
Subject: [GradEase] Réinitialisation de mot de passe - GradEase
From: noreply@gradease.enspd.cm
To: utilisateur@email.com
...

Bonjour Prénom Nom,

Vous avez demandé la réinitialisation de votre mot de passe sur GradEase.

Pour définir un nouveau mot de passe, cliquez sur le lien ci-dessous :

http://localhost:8000/users/password-reset-confirm/MQ/abc123-def456.../
```

### Étape 4 : Utiliser le lien

1. **COPIEZ** le lien qui commence par `http://localhost:8000/users/password-reset-confirm/`
2. **COLLEZ-LE** dans votre navigateur
3. Vous arriverez sur le formulaire de nouveau mot de passe

### Étape 5 : Définir le nouveau mot de passe

1. Entrez un nouveau mot de passe
2. Confirmez-le
3. Cliquez sur **"Réinitialiser le mot de passe"**
4. Vous serez redirigé vers une page de succès

### Étape 6 : Se connecter

1. Cliquez sur **"Se connecter maintenant"**
2. Utilisez votre nouveau mot de passe

---

## 🚀 Test automatique avec le script

```bash
python manage.py shell < scripts/demo_password_reset.py
```

Ce script :
- Liste tous les utilisateurs
- Vous permet de choisir un utilisateur
- Génère un lien de réinitialisation
- Affiche l'email dans la console
- Vous donne le lien direct à copier

---

## 📧 Activer l'envoi d'emails réels (Gmail)

### Pour tester avec de vrais emails :

1. **Modifiez `.env` :**
```env
EMAIL_HOST_USER=votre.email@gmail.com
EMAIL_HOST_PASSWORD=xxxx xxxx xxxx xxxx  # Mot de passe d'application Gmail
EMAIL_USE_GMAIL=True
```

2. **Obtenez un mot de passe d'application Gmail :**
   - Allez sur https://myaccount.google.com/security
   - Activez la validation en 2 étapes
   - Générez un mot de passe d'application

3. **Redémarrez le serveur**

4. **Testez à nouveau** - L'email sera envoyé réellement !

---

## ✅ Vérification que tout fonctionne

### Mode Console (actuel)
- ✅ Email affiché dans la console du serveur
- ✅ Lien de réinitialisation visible et copiable
- ✅ Formulaire de nouveau mot de passe fonctionne
- ✅ Connexion avec nouveau mot de passe fonctionne

### Mode Gmail (après configuration)
- ✅ Email reçu dans la boîte de réception
- ✅ Email au format HTML avec design ENSPD
- ✅ Bouton cliquable dans l'email
- ✅ Lien alternatif si le bouton ne marche pas

---

## 🔒 Fonctionnalités de sécurité

✅ **Ne révèle jamais si un email existe**
- Message identique que l'email soit enregistré ou non
- Empêche l'énumération des comptes

✅ **Token sécurisé**
- Token cryptographique unique
- Expire après 1 heure
- Ne peut être utilisé qu'une seule fois

✅ **Validation du mot de passe**
- Minimum 8 caractères
- Doit contenir lettres et chiffres
- Indicateur de force du mot de passe

---

## 🐛 Dépannage

### "Je ne vois pas l'email dans la console"
- Vérifiez que le serveur Django tourne
- L'email s'affiche dans le terminal où vous avez lancé `python manage.py runserver`
- Pas dans un autre terminal

### "Le lien ne fonctionne pas"
- Vérifiez qu'il n'y a pas de retour à la ligne dans le lien copié
- Le lien expire après 1 heure
- Générez un nouveau lien si nécessaire

### "Erreur SMTP avec Gmail"
- Vérifiez que vous utilisez un mot de passe d'application (pas votre mot de passe Gmail normal)
- Vérifiez que la validation en 2 étapes est activée
- Vérifiez votre connexion Internet

---

## 📝 Notes

- En **développement** : Mode console (pas besoin de configuration)
- En **production** : Configurez Gmail ou un autre service SMTP
- Les emails HTML fonctionnent en mode console ET en mode Gmail
- Le système est entièrement sécurisé contre l'énumération d'utilisateurs
