# 🚀 Guide Ultra-Simple : Déployer sur PythonAnywhere

> **Pour présentation de projet** - Temps estimé : 15-20 minutes

---

## 📋 Prérequis

- ✅ Compte PythonAnywhere gratuit : https://www.pythonanywhere.com/registration/
- ✅ Projet Django fonctionnel en local
- ✅ Compte GitHub avec votre repo

---

## 🎯 Vue d'ensemble (3 grandes étapes)

1. **LOCAL** : Pousser votre code sur GitHub
2. **PYTHONANYWHERE** : Cloner et configurer
3. **WEB APP** : Activer l'application web

---

# PARTIE 1️⃣ : Sur votre ordinateur (5 minutes)

## Étape 1.1 : Vérifier les fichiers à pousser

Ouvrez PowerShell/Terminal dans votre projet :

```powershell
# Voir l'état actuel
git status
```

**✅ CE QUI DOIT ÊTRE DANS GIT :**
- `config/settings_production.py`
- `pythonanywhere_wsgi.py`
- `requirements_production.txt`
- Tout votre code Django (models, views, templates, etc.)

**❌ CE QUI NE DOIT JAMAIS ÊTRE POUSSÉ :**
- `.env` (mots de passe)
- `db.sqlite3` (base locale)
- `/media/`, `/staticfiles/`
- `__pycache__/`, `*.pyc`

## Étape 1.2 : Pousser sur GitHub

```powershell
# Ajouter tous les fichiers sûrs
git add .

# Committer
git commit -m "Préparation déploiement PythonAnywhere"

# Pousser
git push origin main
```

✅ **Checkpoint** : Allez sur GitHub et vérifiez que votre code est bien là

---

# PARTIE 2️⃣ : Sur PythonAnywhere - Configuration initiale (10 minutes)

## Étape 2.1 : Créer une Web App

1. Connectez-vous sur https://www.pythonanywhere.com
2. Cliquez sur l'onglet **"Web"**
3. Cliquez sur **"Add a new web app"**
4. Choisissez votre domaine gratuit : `votreusername.pythonanywhere.com`
5. Sélectionnez **"Manual configuration"** (pas Django wizard !)
6. Choisissez **Python 3.10**
7. Cliquez sur **"Next"**

✅ **Checkpoint** : Vous êtes maintenant sur la page de configuration de votre web app

## Étape 2.2 : Ouvrir une console Bash

1. Onglet **"Consoles"** (en haut)
2. Cliquez sur **"Bash"** dans la section "Start a new console"

Vous êtes maintenant dans un terminal Linux sur PythonAnywhere.

## Étape 2.3 : Cloner votre projet

```bash
# Aller dans le répertoire home
cd ~

# Cloner votre repo GitHub (remplacez par votre URL)
git clone https://github.com/VOTRE_USERNAME/gestion-pfe.git

# Entrer dans le projet
cd gestion-pfe

# Vérifier que les fichiers sont là
ls
```

Vous devez voir : `manage.py`, `config/`, `users/`, etc.

## Étape 2.4 : Créer un environnement virtuel

```bash
# Créer le virtualenv avec Python 3.10
mkvirtualenv --python=/usr/bin/python3.10 gestionpfe

# Il est automatiquement activé (vous voyez (gestionpfe) devant le prompt)
```

## Étape 2.5 : Installer les dépendances

```bash
# Mettre à jour pip
pip install --upgrade pip

# Installer toutes les dépendances
pip install -r requirements_production.txt
```

⏳ Cela prend 1-2 minutes. Attendez que tout soit installé.

## Étape 2.6 : Configurer la base de données MySQL

### A) Créer la base de données

1. Allez dans l'onglet **"Databases"**
2. Dans la section **"Create a new database"** :
   - Entrez un nom : `gestionpfe`
   - Cliquez sur **"Create"**
3. Notez le **nom complet** de la base : `votreusername$gestionpfe`
4. Définissez un **mot de passe MySQL** si ce n'est pas déjà fait
5. Notez votre **hostname** : `votreusername.mysql.pythonanywhere-services.com`

### B) Créer le fichier `.env`

Retournez dans la console Bash :

```bash
# Toujours dans ~/gestion-pfe
cd ~/gestion-pfe

# Créer le fichier .env avec nano (éditeur de texte)
nano .env
```

Copiez-collez ce contenu (⚠️ **REMPLACEZ** les valeurs par les vôtres) :

```env
DJANGO_SECRET_KEY='votre-cle-secrete-django-tres-longue-et-aleatoire'
DB_PASSWORD='votre_mot_de_passe_mysql'
EMAIL_HOST_USER='votre_email@gmail.com'
EMAIL_HOST_PASSWORD='votre_app_password_gmail'
```

**Comment obtenir ces valeurs :**

- **DJANGO_SECRET_KEY** : Générez-en une nouvelle :
  ```bash
  python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
  ```

- **DB_PASSWORD** : Le mot de passe MySQL que vous venez de définir

- **EMAIL_HOST_USER** : Votre adresse Gmail

- **EMAIL_HOST_PASSWORD** : Un mot de passe d'application Gmail
  - Allez sur https://myaccount.google.com/apppasswords
  - Créez un nouveau mot de passe d'application
  - Copiez les 16 caractères

**Sauvegarder dans nano :**
- `Ctrl + O` → Entrée (pour sauvegarder)
- `Ctrl + X` (pour quitter)

## Étape 2.7 : Vérifier `settings_production.py`

```bash
# Voir si le fichier charge bien les variables d'environnement
cat config/settings_production.py | grep -A 5 "DATABASES"
```

Vous devez voir une configuration MySQL qui utilise `os.environ.get('DB_PASSWORD')`.

## Étape 2.8 : Préparer la base de données

```bash
# Créer les tables dans MySQL
python manage.py migrate --settings=config.settings_production

# Collecter les fichiers statiques (CSS, JS, images)
python manage.py collectstatic --noinput --settings=config.settings_production
```

✅ **Checkpoint** : Vous devez voir "X migrations applied" et des fichiers copiés vers staticfiles/

## Étape 2.9 : Créer un compte admin

```bash
python manage.py createsuperuser --settings=config.settings_production
```

Remplissez les informations demandées :
- **Matricule** : `admin001` (ou ce que vous voulez)
- **Email** : votre email
- **Prénom** : Admin
- **Nom** : Système
- **Rôle** : `5` (Admin Général)
- **Filière** : `1` (GI) ou `2` (GBM)
- **Mot de passe** : choisissez un mot de passe fort

---

# PARTIE 3️⃣ : Configuration Web App (5 minutes)

## Étape 3.1 : Configurer le fichier WSGI

1. Retournez dans l'onglet **"Web"**
2. Scrollez jusqu'à la section **"Code"**
3. Cliquez sur le lien sous **"WSGI configuration file"**
   - Exemple : `/var/www/votreusername_pythonanywhere_com_wsgi.py`

4. **Effacez tout le contenu** du fichier

5. Copiez-collez ce code (⚠️ **REMPLACEZ `votreusername`** par votre vrai username PythonAnywhere) :

```python
import os
import sys

# Ajouter le chemin de votre projet
path = '/home/votreusername/gestion-pfe'
if path not in sys.path:
    sys.path.insert(0, path)

# Ajouter le virtualenv
venv_path = '/home/votreusername/.virtualenvs/gestionpfe/lib/python3.10/site-packages'
if venv_path not in sys.path:
    sys.path.insert(0, venv_path)

# Définir les settings de production
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings_production'

# Charger l'application Django
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

6. Cliquez sur **"Save"** (en haut à droite)

## Étape 3.2 : Configurer le Virtualenv

1. Retournez en haut de la page **"Web"**
2. Dans la section **"Virtualenv"**, cliquez sur **"Enter path to a virtualenv"**
3. Entrez : `/home/votreusername/.virtualenvs/gestionpfe`
   (⚠️ Remplacez `votreusername`)
4. Cliquez sur le ✓ (checkmark)

## Étape 3.3 : Configurer les fichiers statiques

Scrollez vers **"Static files"** :

**Mapping 1 - CSS/JS/images :**
- URL : `/static/`
- Directory : `/home/votreusername/gestion-pfe/staticfiles`

**Mapping 2 - Fichiers uploadés :**
- URL : `/media/`
- Directory : `/home/votreusername/gestion-pfe/media`

⚠️ N'oubliez pas de **remplacer `votreusername`** !

## Étape 3.4 : Recharger l'application

1. Remontez en haut de la page
2. Cliquez sur le gros bouton vert **"Reload votreusername.pythonanywhere.com"**
3. Attendez 5-10 secondes

---

# 🎉 ÉTAPE FINALE : Tester votre application

## Étape 4.1 : Ouvrir votre site

Cliquez sur le lien en haut de la page Web :
```
https://votreusername.pythonanywhere.com
```

✅ **Vous devriez voir la page d'accueil de votre projet !**

## Étape 4.2 : Tester l'admin Django

Allez sur :
```
https://votreusername.pythonanywhere.com/admin
```

Connectez-vous avec le superuser créé à l'étape 2.9.

✅ **Si vous voyez le panneau d'administration Django, c'est gagné !** 🎉

---

# 🐛 Problèmes courants et solutions

## ❌ Erreur 502 Bad Gateway

**Causes possibles :**
- Le fichier WSGI a une erreur de syntaxe
- Le chemin du virtualenv est incorrect
- Settings de production ne se charge pas

**Solution :**
1. Vérifiez les logs d'erreur :
   - Onglet **"Web"** → Section **"Log files"**
   - Cliquez sur **"Error log"**
2. Corrigez l'erreur indiquée
3. Rechargez l'application

## ❌ Page sans CSS (tout est laid)

**Cause :** Les fichiers statiques ne sont pas mappés correctement

**Solution :**
```bash
# Dans la console Bash
cd ~/gestion-pfe
workon gestionpfe
python manage.py collectstatic --noinput --settings=config.settings_production
```

Puis vérifiez les mappings dans **"Static files"** de l'onglet Web.

## ❌ Erreur "Database connection failed"

**Cause :** Le fichier `.env` n'a pas les bonnes informations

**Solution :**
```bash
# Vérifier le contenu
cat ~/gestion-pfe/.env

# Vérifier que le mot de passe MySQL est correct
# Tester la connexion
cd ~/gestion-pfe
workon gestionpfe
python manage.py check --settings=config.settings_production
```

## ❌ Erreur "ModuleNotFoundError"

**Cause :** Dépendances manquantes

**Solution :**
```bash
cd ~/gestion-pfe
workon gestionpfe
pip install -r requirements_production.txt
```

Puis rechargez l'application.

---

# 🔒 Sécurité - IMPORTANT pour la présentation

## ⚠️ NE JAMAIS :
- ❌ Pousser le fichier `.env` sur GitHub
- ❌ Partager votre SECRET_KEY publiquement
- ❌ Montrer votre mot de passe MySQL dans la présentation
- ❌ Afficher l'écran pendant que vous tapez les mots de passe

## ✅ TOUJOURS :
- ✓ Vérifier que `.env` est dans `.gitignore`
- ✓ Utiliser des mots de passe forts
- ✓ Créer un nouveau SECRET_KEY pour la production
- ✓ Utiliser des App Passwords Gmail (pas votre vrai mot de passe)

## 🔍 Vérification de sécurité avant la présentation

```powershell
# Sur votre machine
git status

# S'assurer que .env n'apparaît PAS dans la liste
```

Si `.env` apparaît :
```powershell
# L'ajouter au .gitignore
echo ".env" >> .gitignore
git add .gitignore
git commit -m "Sécurité: Ignorer .env"
git push
```

---

# 📝 Checklist finale avant la présentation

- [ ] ✅ Application accessible sur `https://votreusername.pythonanywhere.com`
- [ ] ✅ Page d'accueil se charge correctement avec CSS
- [ ] ✅ Login fonctionne (testez avec votre superuser)
- [ ] ✅ Admin accessible sur `/admin`
- [ ] ✅ Pas d'erreur dans les logs (Web → Error log)
- [ ] ✅ Fichier `.env` est local uniquement (pas sur GitHub)
- [ ] ✅ Créer 2-3 utilisateurs de test pour la démo
- [ ] ✅ Créer des données de test (sujets, projets) si besoin

---

# 🚀 Commandes rapides pour la démo

## Ajouter des utilisateurs de test

```bash
cd ~/gestion-pfe
workon gestionpfe
python manage.py shell --settings=config.settings_production
```

```python
from users.models import User

# Créer un étudiant
etudiant = User.objects.create_user(
    matricule='22X0001',
    email='etudiant@enspd.cm',
    first_name='Jean',
    last_name='Dupont',
    role=1,  # Étudiant
    filiere=1  # GI
)
etudiant.set_password('demo2024')
etudiant.save()

# Créer un enseignant
prof = User.objects.create_user(
    matricule='PROF001',
    email='prof@enspd.cm',
    first_name='Marie',
    last_name='Martin',
    role=2,  # Enseignant
    filiere=1
)
prof.set_password('demo2024')
prof.save()

exit()
```

## Mettre à jour après des changements

```bash
# Si vous modifiez du code en local et voulez l'envoyer sur PythonAnywhere
cd ~/gestion-pfe
git pull origin main
workon gestionpfe
python manage.py migrate --settings=config.settings_production
python manage.py collectstatic --noinput --settings=config.settings_production
```

Puis rechargez via le bouton **Reload** dans l'onglet Web.

---

# 💡 Conseils pour la présentation

1. **Préparez une sauvegarde** : Faites des captures d'écran de votre app fonctionnelle
2. **Testez avant** : Ouvrez votre site 1h avant la présentation pour vérifier
3. **Compte démo** : Créez un compte avec identifiants simples pour la démo
4. **Plan B** : Ayez votre version locale prête en cas de problème réseau
5. **URL courte** : Notez votre URL sur un papier : `votreusername.pythonanywhere.com`

---

# 📞 Besoin d'aide ?

- Documentation PythonAnywhere : https://help.pythonanywhere.com/
- Forum PythonAnywhere : https://www.pythonanywhere.com/forums/
- Documentation Django : https://docs.djangoproject.com/

---

# ✨ Félicitations !

Votre projet Django est maintenant en ligne et accessible à tous ! 🎉

**URL de votre projet :** `https://votreusername.pythonanywhere.com`

Bonne présentation ! 👏
