# 🎓 Projet de Gestion PFE - ENSPD

## ✅ État d'avancement

Le projet est maintenant **opérationnel** avec la première fonctionnalité complète : **Gestion des utilisateurs et authentification**.

### Fonctionnalités implémentées

#### 1. ✅ Gestion des utilisateurs et authentification (COMPLÈTE)

**Backend (Django):**
- ✅ Modèle User personnalisé avec 4 rôles (étudiant, encadreur, administration, jury)
- ✅ Modèle Profile pour informations complémentaires
- ✅ Formulaires d'inscription et connexion sécurisés
- ✅ Formulaires de mise à jour de profil
- ✅ Vues pour inscription, connexion, déconnexion, profil
- ✅ Tableaux de bord personnalisés par rôle
- ✅ Interface d'administration Django

**Frontend (HTML/CSS/JavaScript):**
- ✅ Template de base responsive avec Bootstrap 5
- ✅ Page d'accueil attractive
- ✅ Pages d'inscription et connexion
- ✅ Tableaux de bord pour chaque rôle (étudiant, encadreur, admin, jury)
- ✅ Page de profil utilisateur
- ✅ Page d'édition de profil
- ✅ Fichiers CSS personnalisés avec animations
- ✅ JavaScript pour fonctionnalités interactives

### Fonctionnalités à implémenter

#### 2. ⏳ Catalogue et affectation des sujets
- Créer les modèles Subject, Candidature, Affectation
- Créer les vues et templates pour proposer des sujets
- Créer les vues et templates pour consulter les sujets
- Système de candidature en ligne
- Système d'affectation automatisé

#### 3. ⏳ Suivi collaboratif des projets
- Créer les modèles Project, Milestone, Deliverable
- Tableau de bord avec indicateurs de progression
- Planification par jalons
- Upload et versioning des livrables

#### 4. ⏳ Communication contextualisée
- Créer les modèles Message, Notification
- Messagerie interne
- Système de notifications
- Commentaires sur documents

#### 5. ⏳ Planification automatisée des soutenances
- Créer les modèles Defense, Jury, Evaluation
- Génération automatique du planning
- Constitution des jurys
- Saisie des notes et procès-verbaux

#### 6. ⏳ Archivage et reporting
- Créer les modèles Archive, Report
- Bibliothèque numérique
- Moteur de recherche
- Génération de statistiques

## 🚀 Comment démarrer le projet

### 1. Activer l'environnement virtuel
```powershell
cd "c:\Users\hp\Documents\Projet gestion PFE"
.\venv\Scripts\Activate.ps1
```

### 2. Lancer le serveur de développement
```powershell
python manage.py runserver
```

Ou directement sans activer l'environnement:
```powershell
.\venv\Scripts\python.exe manage.py runserver
```

### 3. Accéder à l'application
- **Interface principale:** http://127.0.0.1:8000/
- **Interface d'administration:** http://127.0.0.1:8000/admin/

## 🔐 Identifiants de connexion

### Superutilisateur (Administration Django)
- **Username:** admin
- **Email:** admin@enspd.cm
- **Password:** admin123

### Pour créer d'autres utilisateurs
Utilisez la page d'inscription: http://127.0.0.1:8000/users/register/

## 📁 Structure du projet

```
Projet gestion PFE/
├── config/                     # Configuration Django principale
│   ├── settings.py            # Paramètres du projet
│   ├── urls.py                # URLs principales
│   └── wsgi.py                # Configuration WSGI
│
├── users/                     # Application gestion utilisateurs ✅
│   ├── models.py              # Modèles User et Profile
│   ├── forms.py               # Formulaires d'authentification
│   ├── views.py               # Vues pour inscription/connexion/profil
│   ├── urls.py                # URLs de l'application users
│   └── admin.py               # Configuration admin
│
├── subjects/                  # Application gestion des sujets ⏳
├── projects/                  # Application suivi des projets ⏳
├── defenses/                  # Application planification soutenances ⏳
├── communications/            # Application messagerie ⏳
├── archives/                  # Application archivage ⏳
│
├── templates/                 # Templates HTML
│   ├── base.html              # Template de base
│   ├── home.html              # Page d'accueil
│   └── users/                 # Templates users
│       ├── login.html
│       ├── register.html
│       ├── dashboard_student.html
│       ├── dashboard_supervisor.html
│       ├── dashboard_admin.html
│       ├── dashboard_jury.html
│       ├── profile.html
│       └── profile_edit.html
│
├── static/                    # Fichiers statiques
│   ├── css/
│   │   └── style.css          # Styles personnalisés
│   ├── js/
│   │   └── main.js            # JavaScript principal
│   └── images/
│
├── media/                     # Fichiers uploadés
│   ├── avatars/               # Photos de profil
│   └── documents/             # Documents des projets
│
├── venv/                      # Environnement virtuel Python
├── db.sqlite3                 # Base de données SQLite
├── manage.py                  # Script de gestion Django
├── requirements.txt           # Dépendances Python
├── .env                       # Variables d'environnement
└── README.md                  # Documentation

```

## 🛠️ Technologies utilisées

- **Backend:** Django 4.2 (Python)
- **Frontend:** HTML5, CSS3, JavaScript (Vanilla)
- **Framework CSS:** Bootstrap 5.3
- **Icônes:** Font Awesome 6.4
- **Base de données:** SQLite (développement)
- **Authentification:** Django Auth System personnalisé

## 📋 Commandes utiles

### Créer des migrations
```powershell
python manage.py makemigrations
```

### Appliquer les migrations
```powershell
python manage.py migrate
```

### Créer un superutilisateur
```powershell
python manage.py createsuperuser
```

### Collecter les fichiers statiques (production)
```powershell
python manage.py collectstatic
```

### Lancer les tests
```powershell
python manage.py test
```

## 🎯 Prochaines étapes

1. **Implémenter la fonctionnalité "Catalogue et affectation des sujets"**
   - Créer les modèles pour les sujets
   - Créer les vues et templates pour la gestion des sujets
   - Implémenter le système de candidature
   - Tester l'intégration front-end/back-end

2. **Continuer fonctionnalité par fonctionnalité** selon le plan établi

## 📞 Support

Pour toute question ou problème, consultez la documentation Django : https://docs.djangoproject.com/

---

**Projet académique - ENSPD 2025**  
**Développement fonctionnalité par fonctionnalité avec intégration complète front-end/back-end**
