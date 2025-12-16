# 🚀 Déploiement Rapide - PythonAnywhere

## ⚡ ÉTAPES RAPIDES (15 minutes)

### 1️⃣ Créer le compte PythonAnywhere
- Allez sur: https://www.pythonanywhere.com/registration/register/beginner/
- Créez un compte gratuit
- Notez votre nom d'utilisateur (ex: `johnsmith`)

---

### 2️⃣ Configurer MySQL (sur PythonAnywhere Dashboard)
1. Allez dans **Databases** → **MySQL**
2. Définissez un mot de passe MySQL
3. Créez une base de données: `VOTRE-USERNAME$gestionpfe`
4. Notez le mot de passe quelque part

---

### 3️⃣ Terminal Bash PythonAnywhere

Ouvrez un terminal Bash et collez ces commandes UNE PAR UNE:

```bash
# ===== VARIABLES À CONFIGURER =====
export USERNAME="VOTRE-USERNAME-ICI"  # Remplacez par votre username PythonAnywhere
export GITHUB_REPO="https://github.com/AcMongue/gestion-pfe.git"

# ===== CLONAGE DU PROJET =====
cd ~
git clone $GITHUB_REPO gestion-pfe
cd gestion-pfe

# ===== ENVIRONNEMENT VIRTUEL =====
mkvirtualenv --python=/usr/bin/python3.10 gestionpfe
workon gestionpfe

# ===== INSTALLATION DES DÉPENDANCES =====
pip install --upgrade pip
pip install -r requirements_production.txt

# ===== CRÉATION DES RÉPERTOIRES =====
mkdir -p logs staticfiles
mkdir -p media/avatars media/documents media/projects
chmod -R 755 media staticfiles logs

# ===== GÉNÉRATION SECRET KEY =====
python -c "from django.core.management.utils import get_random_secret_key; print('SECRET_KEY:', get_random_secret_key())"
# COPIEZ LA CLÉ AFFICHÉE ⬆️
```
31nx8k!$!^2^=^+)k(@dr@ux=k+=3cpvhrhvz+5+7h$3g3$g8m
---

### 4️⃣ Créer le fichier .env

Dans le terminal, créez le fichier de configuration:

```bash
nano .env
```

Collez ce contenu (REMPLACEZ LES VALEURS):

```env
DJANGO_SECRET_KEY='COLLEZ-LA-SECRET-KEY-GENEREE-ETAPE-3'
DB_PASSWORD='VOTRE-MOT-DE-PASSE-MYSQL-ETAPE-2'
EMAIL_HOST_USER='votre-email@gmail.com'
EMAIL_HOST_PASSWORD='mot-de-passe-app-gmail'
```

DJANGO_SECRET_KEY='31nx8k!$!^2^=^+)k(@dr@ux=k+=3cpvhrhvz+5+7h$3g3$g8m'
DB_PASSWORD='mysql2003'
EMAIL_HOST_USER='ac7dev25@gmail.com'
EMAIL_HOST_PASSWORD='hxpk rkai aynu hcck'
**Pour Gmail:**
1. Allez sur https://myaccount.google.com/security
2. Activez la validation en 2 étapes
3. Créez un mot de passe d'application
4. Utilisez ce mot de passe dans EMAIL_HOST_PASSWORD

Sauvegardez: `Ctrl+O` → `Entrée` → `Ctrl+X`

---

### 5️⃣ Mise à jour settings_production.py

```bash
# Remplacez automatiquement votre username partout
sed -i "s/votre-username/$USERNAME/g" config/settings_production.py

# Vérifiez avec plus de contexte
grep -A 3 "ALLOWED_HOSTS" config/settings_production.py
# Devrait afficher:
# ALLOWED_HOSTS = [
#     'ac7.pythonanywhere.com',
#     'www.ac7.pythonanywhere.com',
# ]
```

---

### 6️⃣ Django - Migrations et Collecte Statiques

```bash
# Collecte des fichiers statiques
python manage.py collectstatic --noinput --settings=config.settings_production

# Migrations de la base de données
python manage.py migrate --settings=config.settings_production

# Création du superutilisateur (INTERACTIF)
python manage.py createsuperuser --settings=config.settings_production
```

**Entrez les informations du superutilisateur:**
- Matricule: `admin001`
- Email: `admin@enspd.cm`
- Prénom: `Admin`
- Nom: `Système`
- Rôle: `5` (Admin Général)
- Filière: `1` (GI) ou `2` (GBM)
- Mot de passe: (choisissez un mot de passe fort)

---

### 7️⃣ Configuration Web App PythonAnywhere

1. **Allez dans l'onglet Web** → **Add a new web app**
2. Choisissez **Manual configuration** → **Python 3.10**

#### A. Fichier WSGI

Cliquez sur le lien WSGI (ex: `/var/www/VOTRE-USERNAME_pythonanywhere_com_wsgi.py`)

**Supprimez tout** et collez:

```python
import os
import sys

# REMPLACEZ 'VOTRE-USERNAME' par votre username réel
path = '/home/VOTRE-USERNAME/gestion-pfe'
if path not in sys.path:
    sys.path.insert(0, path)

venv_path = '/home/VOTRE-USERNAME/.virtualenvs/gestionpfe/lib/python3.10/site-packages'
if venv_path not in sys.path:
    sys.path.insert(0, venv_path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings_production'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

Sauvegardez et fermez.

#### B. Environnement Virtuel

Dans la section **Virtualenv**, entrez:
```
/home/VOTRE-USERNAME/.virtualenvs/gestionpfe
```

#### C. Fichiers Statiques

Dans **Static files**, ajoutez 2 entrées:

| URL       | Directory                                          |
|-----------|----------------------------------------------------|
| /static/  | /home/VOTRE-USERNAME/gestion-pfe/staticfiles      |
| /media/   | /home/VOTRE-USERNAME/gestion-pfe/media            |

#### D. Variables d'environnement (optionnel)

Si vous préférez ne pas utiliser `.env`:
1. Allez dans **Environment variables** (bas de page)
2. Ajoutez chaque variable:
   - `DJANGO_SECRET_KEY`
   - `DB_PASSWORD`
   - `EMAIL_HOST_USER`
   - `EMAIL_HOST_PASSWORD`

---

### 8️⃣ Rechargement et Test

1. **Bouton vert** en haut: **Reload VOTRE-USERNAME.pythonanywhere.com**
2. **Visitez**: `https://VOTRE-USERNAME.pythonanywhere.com`

#### ✅ Tests à effectuer:
- [ ] Page d'accueil s'affiche
- [ ] Login fonctionne
- [ ] Admin accessible: `/admin`
- [ ] Images/CSS chargés correctement

---

## 🔥 COMMANDES DE MAINTENANCE

### Mise à jour depuis GitHub
```bash
cd ~/gestion-pfe
git pull origin main
python manage.py migrate --settings=config.settings_production
python manage.py collectstatic --noinput --settings=config.settings_production
# Puis recharger l'app dans Web
```

### Voir les logs d'erreur
```bash
# Logs Django
tail -50 ~/gestion-pfe/logs/django.log

# Logs serveur
tail -50 /var/log/VOTRE-USERNAME.pythonanywhere.com.error.log

# Logs en temps réel
tail -f ~/gestion-pfe/logs/django.log
```

### Créer des données de test
```bash
cd ~/gestion-pfe
workon gestionpfe
python scripts/data/create_test_data.py
```

### Shell Django
```bash
cd ~/gestion-pfe
workon gestionpfe
python manage.py shell --settings=config.settings_production
```

### Backup base de données
```bash
mysqldump -u $USERNAME -h $USERNAME.mysql.pythonanywhere-services.com -p $USERNAME\$gestionpfe > backup_$(date +%Y%m%d).sql
```

---

## ⚠️ DÉPANNAGE RAPIDE

### Erreur "collectstatic command not found"

Problème de chargement des settings. Vérifiez:

```bash
# 1. Fichier .env existe ?
ls -la .env

# 2. Testez le chargement
python -c "import os; os.environ['DJANGO_SETTINGS_MODULE']='config.settings_production'; import django; django.setup(); print('OK')"

# 3. Si erreur d'import, vérifiez les dépendances
pip install python-decouple
pip list | grep -i django

# 4. Vérifiez le contenu du .env
cat .env
```

### Erreur 500
```bash
# Vérifier les logs
tail -50 /var/log/VOTRE-USERNAME.pythonanywhere.com.error.log

# Vérifier la config
python manage.py check --deploy --settings=config.settings_production
```

### CSS/Images ne chargent pas
1. Vérifiez les chemins dans Static files (étape 7C)
2. Re-exécutez `collectstatic`
3. Rechargez l'app

### Base de données inaccessible
```bash
# Tester la connexion MySQL
mysql -u VOTRE-USERNAME -h VOTRE-USERNAME.mysql.pythonanywhere-services.com -p
# Entrez le mot de passe de l'étape 2
```

### Import error
```bash
# Réinstaller les dépendances
workon gestionpfe
pip install -r requirements_production.txt --force-reinstall
```

---

## 📊 STATUT DU DÉPLOIEMENT

- [ ] Compte PythonAnywhere créé
- [ ] MySQL configuré
- [ ] Code cloné depuis GitHub
- [ ] Environnement virtuel créé
- [ ] Dépendances installées
- [ ] Fichier .env créé
- [ ] settings_production.py mis à jour
- [ ] Migrations exécutées
- [ ] Fichiers statiques collectés
- [ ] Superutilisateur créé
- [ ] Web app configurée
- [ ] WSGI configuré
- [ ] Static files mappés
- [ ] Application rechargée
- [ ] Site accessible et fonctionnel

---

## 🎯 VOTRE SITE

Une fois déployé, votre application sera accessible à:

**URL**: https://VOTRE-USERNAME.pythonanywhere.com
**Admin**: https://VOTRE-USERNAME.pythonanywhere.com/admin

---

**Temps estimé**: 15-20 minutes  
**Dernière mise à jour**: 15 décembre 2025
