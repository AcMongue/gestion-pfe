# 🚀 Commandes Rapides - Projet Gestion PFE

## Démarrage quotidien

### Lancer le serveur
```powershell
cd "c:\Users\hp\Documents\Projet gestion PFE"
.\venv\Scripts\python.exe manage.py runserver
```

Puis ouvrir: http://127.0.0.1:8000/

### Accéder à l'administration
http://127.0.0.1:8000/admin/
- Username: `admin`
- Password: `admin123`

## Gestion de la base de données

### Créer des migrations après modification des modèles
```powershell
.\venv\Scripts\python.exe manage.py makemigrations
```

### Appliquer les migrations
```powershell
.\venv\Scripts\python.exe manage.py migrate
```

### Réinitialiser la base de données (ATTENTION: supprime toutes les données!)
```powershell
Remove-Item db.sqlite3
.\venv\Scripts\python.exe manage.py migrate
.\venv\Scripts\python.exe set_admin_password.py
```

## Gestion des utilisateurs

### Créer un superutilisateur
```powershell
.\venv\Scripts\python.exe manage.py createsuperuser
```

### Changer le mot de passe d'un utilisateur
```powershell
.\venv\Scripts\python.exe manage.py changepassword <username>
```

## Gestion des fichiers statiques

### Collecter les fichiers statiques (pour production)
```powershell
.\venv\Scripts\python.exe manage.py collectstatic
```

## Tests

### Lancer tous les tests
```powershell
.\venv\Scripts\python.exe manage.py test
```

### Tester une application spécifique
```powershell
.\venv\Scripts\python.exe manage.py test users
```

## Shell Django

### Ouvrir le shell interactif Django
```powershell
.\venv\Scripts\python.exe manage.py shell
```

Exemples de commandes dans le shell:
```python
# Importer le modèle User
from users.models import User

# Lister tous les utilisateurs
User.objects.all()

# Créer un utilisateur
user = User.objects.create_user(
    username='test',
    email='test@example.com',
    password='test123',
    role='student'
)

# Compter les utilisateurs par rôle
User.objects.filter(role='student').count()
```

## Développement

### Créer une nouvelle application Django
```powershell
.\venv\Scripts\python.exe manage.py startapp nom_app
```

### Vérifier le projet pour des problèmes
```powershell
.\venv\Scripts\python.exe manage.py check
```

### Afficher les migrations
```powershell
.\venv\Scripts\python.exe manage.py showmigrations
```

## Dépendances

### Installer les dépendances
```powershell
.\venv\Scripts\python.exe -m pip install -r requirements.txt
```

### Mettre à jour les dépendances
```powershell
.\venv\Scripts\python.exe -m pip install --upgrade -r requirements.txt
```

### Ajouter une nouvelle dépendance
```powershell
.\venv\Scripts\python.exe -m pip install nom_package
.\venv\Scripts\python.exe -m pip freeze > requirements.txt
```

## Nettoyage

### Supprimer les fichiers Python compilés
```powershell
Get-ChildItem -Path . -Filter "*.pyc" -Recurse | Remove-Item
Get-ChildItem -Path . -Filter "__pycache__" -Recurse | Remove-Item -Recurse
```

### Supprimer les fichiers de migration (ATTENTION!)
```powershell
Get-ChildItem -Path . -Filter "0*.py" -Recurse | Where-Object { $_.Directory.Name -eq "migrations" } | Remove-Item
```

## URLs importantes

- **Page d'accueil:** http://127.0.0.1:8000/
- **Inscription:** http://127.0.0.1:8000/users/register/
- **Connexion:** http://127.0.0.1:8000/users/login/
- **Tableau de bord:** http://127.0.0.1:8000/users/dashboard/
- **Profil:** http://127.0.0.1:8000/users/profile/
- **Admin:** http://127.0.0.1:8000/admin/

## Environnement virtuel

### Créer un nouvel environnement virtuel (si nécessaire)
```powershell
python -m venv venv
```

### Activer l'environnement (si la politique d'exécution le permet)
```powershell
.\venv\Scripts\Activate.ps1
```

### Désactiver l'environnement
```powershell
deactivate
```

## Git (si utilisé)

### Initialiser le dépôt
```powershell
git init
git add .
git commit -m "Initial commit - Fonctionnalité 1 complète"
```

### Ajouter un remote et pousser
```powershell
git remote add origin <url-du-depot>
git push -u origin main
```

## Aide

### Voir toutes les commandes Django disponibles
```powershell
.\venv\Scripts\python.exe manage.py help
```

### Aide sur une commande spécifique
```powershell
.\venv\Scripts\python.exe manage.py help <commande>
```

---

**Astuce:** Vous pouvez créer un fichier `run.ps1` avec la commande de démarrage pour lancer rapidement le serveur.

```powershell
# Contenu de run.ps1
cd "c:\Users\hp\Documents\Projet gestion PFE"
.\venv\Scripts\python.exe manage.py runserver
```

Puis exécuter: `.\run.ps1`
