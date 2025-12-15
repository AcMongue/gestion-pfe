# Guide de Déploiement PythonAnywhere

## 📋 Prérequis

- Compte PythonAnywhere (gratuit ou payant)
- Repository GitHub avec votre projet
- Adresse email Gmail pour l'envoi d'emails

## 🚀 Étapes de Déploiement

### 1️⃣ Préparation sur GitHub

```bash
# Assurez-vous que tout est commité et poussé
git add .
git commit -m "Préparation déploiement PythonAnywhere"
git push origin main
```

### 2️⃣ Création du compte PythonAnywhere

1. Allez sur [www.pythonanywhere.com](https://www.pythonanywhere.com)
2. Créez un compte (le plan Beginner gratuit suffit pour commencer)
3. Notez votre nom d'utilisateur (ex: `johnsmith`)

### 3️⃣ Configuration de la base de données MySQL

1. Dans le dashboard PythonAnywhere, allez dans **Databases**
2. Configurez un mot de passe MySQL
3. Créez une base de données nommée: `votre-username$gestionpfe`
4. Notez les informations de connexion:
   - Host: `votre-username.mysql.pythonanywhere-services.com`
   - Database: `votre-username$gestionpfe`
   - User: `votre-username`

### 4️⃣ Configuration dans le terminal Bash

Ouvrez un terminal Bash dans PythonAnywhere et exécutez:

```bash
# 1. Clonez votre repository
cd ~
git clone https://github.com/votre-compte/votre-repo.git gestion-pfe
cd gestion-pfe

# 2. Créez l'environnement virtuel
mkvirtualenv --python=/usr/bin/python3.10 gestionpfe

# 3. Installez les dépendances
pip install -r requirements_production.txt

# 4. Créez les répertoires nécessaires
mkdir -p logs staticfiles media/avatars media/documents media/projects
```

### 5️⃣ Configuration des variables d'environnement

Créez un fichier `.env` dans le répertoire du projet:

```bash
nano .env
```

Ajoutez:

```env
DJANGO_SECRET_KEY='votre-nouvelle-secret-key-super-longue-et-aleatoire'
DB_PASSWORD='votre-mot-de-passe-mysql'
EMAIL_HOST_USER='votre-email@gmail.com'
EMAIL_HOST_PASSWORD='votre-mot-de-passe-app-gmail'
```

**Comment générer une SECRET_KEY:**

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

**Comment obtenir un mot de passe d'application Gmail:**
1. Allez dans votre compte Google → Sécurité
2. Activez la validation en deux étapes
3. Créez un mot de passe d'application pour "Mail"

### 6️⃣ Mise à jour de settings_production.py

Éditez [config/settings_production.py](config/settings_production.py) et remplacez:

- `votre-username` par votre nom d'utilisateur PythonAnywhere (6 occurrences)
- `votre-username.pythonanywhere.com` par votre domaine réel

```bash
# Commande rapide pour remplacer
sed -i 's/votre-username/VOTRE_USERNAME_REEL/g' config/settings_production.py
```

### 7️⃣ Configuration de l'application Web

1. Dans PythonAnywhere, allez dans **Web**
2. Cliquez sur **Add a new web app**
3. Choisissez **Manual configuration**
4. Sélectionnez **Python 3.10**

#### Configuration du fichier WSGI:

1. Cliquez sur le lien du fichier WSGI (ex: `/var/www/votre-username_pythonanywhere_com_wsgi.py`)
2. Supprimez tout le contenu
3. Copiez le contenu de [pythonanywhere_wsgi.py](pythonanywhere_wsgi.py)
4. Remplacez `votre-username` par votre nom d'utilisateur
5. Sauvegardez

#### Configuration de l'environnement virtuel:

Dans la section **Virtualenv**:
```
/home/votre-username/.virtualenvs/gestionpfe
```

#### Configuration des fichiers statiques:

Dans la section **Static files**, ajoutez:

| URL          | Directory                                          |
|--------------|----------------------------------------------------|
| /static/     | /home/votre-username/gestion-pfe/staticfiles      |
| /media/      | /home/votre-username/gestion-pfe/media            |

### 8️⃣ Migrations et collecte des fichiers statiques

Dans le terminal Bash:

```bash
cd ~/gestion-pfe
workon gestionpfe

# Collecte des fichiers statiques
python manage.py collectstatic --settings=config.settings_production

# Migrations
python manage.py migrate --settings=config.settings_production

# Création du superutilisateur
python manage.py createsuperuser --settings=config.settings_production
```

### 9️⃣ Rechargement de l'application

1. Retournez dans l'onglet **Web**
2. Cliquez sur le bouton vert **Reload votre-username.pythonanywhere.com**

### 🎉 Vérification

1. Visitez `https://votre-username.pythonanywhere.com`
2. Vous devriez voir la page d'accueil
3. Testez la connexion avec le superutilisateur créé
4. Vérifiez l'admin: `https://votre-username.pythonanywhere.com/admin`

## 🔧 Maintenance et Mises à jour

### Mettre à jour le code depuis GitHub:

```bash
cd ~/gestion-pfe
git pull origin main
python manage.py migrate --settings=config.settings_production
python manage.py collectstatic --noinput --settings=config.settings_production
# Puis rechargez l'app dans l'onglet Web
```

### Voir les logs d'erreur:

```bash
# Logs Django
tail -f ~/gestion-pfe/logs/django.log

# Logs serveur
tail -f /var/log/votre-username.pythonanywhere.com.error.log
```

### Créer des données de test:

```bash
cd ~/gestion-pfe
workon gestionpfe
python scripts/data/create_test_data.py
```

## 🐛 Dépannage

### Erreur 500 Internal Server Error

1. Vérifiez les logs d'erreur
2. Assurez-vous que `ALLOWED_HOSTS` est configuré
3. Vérifiez que les migrations sont appliquées
4. Vérifiez les permissions des dossiers media et staticfiles

### Base de données non accessible

1. Vérifiez le mot de passe MySQL dans `.env`
2. Vérifiez le nom de la base de données (format: `username$dbname`)
3. Testez la connexion MySQL:

```bash
mysql -u votre-username -h votre-username.mysql.pythonanywhere-services.com -p
```

### Fichiers statiques non chargés

1. Vérifiez les chemins dans la section Static files
2. Re-exécutez `collectstatic`
3. Rechargez l'application web

### Emails non envoyés

1. Vérifiez les variables d'environnement EMAIL_*
2. Assurez-vous d'utiliser un mot de passe d'application Gmail
3. Vérifiez les logs pour les erreurs SMTP

## 📊 Performance et Limites (Plan Gratuit)

- **CPU**: 100 secondes/jour
- **Stockage**: 512 MB
- **Trafic**: Limité mais suffisant pour tests
- **Temps d'inactivité**: L'app s'endort après 3 mois sans visite

**Recommandation**: Pour production réelle, passez au plan payant ($5/mois).

## 🔒 Sécurité

### Checklist de sécurité:

- ✅ `DEBUG = False` en production
- ✅ `SECRET_KEY` unique et sécurisée
- ✅ HTTPS activé (automatique sur PythonAnywhere)
- ✅ Mot de passe MySQL fort
- ✅ Variables sensibles dans `.env` (non commité)
- ✅ CORS configuré si nécessaire

### Sauvegardes:

```bash
# Backup de la base de données
mysqldump -u votre-username -h votre-username.mysql.pythonanywhere-services.com -p votre-username$gestionpfe > backup_$(date +%Y%m%d).sql

# Backup des fichiers média
tar -czf media_backup_$(date +%Y%m%d).tar.gz media/
```

## 📚 Ressources

- [Documentation PythonAnywhere](https://help.pythonanywhere.com/)
- [Déploiement Django](https://help.pythonanywhere.com/pages/DeployExistingDjangoProject/)
- [Configuration MySQL](https://help.pythonanywhere.com/pages/UsingMySQL/)
- [Variables d'environnement](https://help.pythonanywhere.com/pages/environment-variables-for-web-apps/)

## 🆘 Support

En cas de problème:
1. Consultez les logs
2. Vérifiez la [documentation PythonAnywhere](https://help.pythonanywhere.com/)
3. Forum PythonAnywhere
4. Stack Overflow avec le tag `pythonanywhere`

---

**Dernière mise à jour**: 15 décembre 2025
