# Projet de Gestion PFE

Application web de gestion des Projets de Fin d'Études (PFE) et mémoires pour l'ENSPD.

## Technologies

- **Backend**: Django 4.2 (Python)
- **Frontend**: HTML, CSS, JavaScript (vanilla)
- **Base de données**: SQLite (développement)
- **Architecture**: Monolithique 2-tiers

## Fonctionnalités

1. **Gestion des utilisateurs et authentification**
   - Inscription et connexion sécurisées
   - Profils personnalisés par rôle (étudiant, encadreur, administration, jury)
   - Gestion fine des droits d'accès

2. **Catalogue et affectation des sujets**
   - Proposition de sujets par les encadreurs
   - Consultation dynamique avec filtres avancés
   - Candidature en ligne et affectation automatisée

3. **Suivi collaboratif des projets**
   - Tableau de bord personnalisé
   - Planification par jalons
   - Dépôt et versioning des livrables

4. **Communication contextualisée**
   - Messagerie interne dédiée
   - Notifications intelligentes
   - Commentaires sur documents

5. **Planification automatisée des soutenances**
   - Génération automatique du planning
   - Constitution des jurys
   - Saisie des notes et procès-verbaux

6. **Archivage et reporting**
   - Bibliothèque numérique
   - Tableaux de bord statistiques
   - Exports de données

## Installation

### Prérequis

- Python 3.10 ou supérieur
- pip (gestionnaire de packages Python)

### Configuration

1. Cloner le dépôt ou créer le projet

2. Créer un environnement virtuel:
```bash
python -m venv venv
```

3. Activer l'environnement virtuel:
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

4. Installer les dépendances:
4. Installer les dépendances:
```bash
pip install -r requirements.txt
```

5. Configurer les variables d'environnement:
   - Copier `.env.example` vers `.env`
   - La base de données SQLite sera créée automatiquement

6. Appliquer les migrations:
python manage.py migrate
```

7. Créer un superutilisateur:
```bash
python manage.py createsuperuser
```

8. Lancer le serveur de développement:
```bash
python manage.py runserver
```

9. Accéder à l'application:
   - Interface principale: http://localhost:8000
   - Interface d'administration: http://localhost:8000/admin

## Structure du projet

```
gestion_pfe/
├── config/                 # Configuration Django principale
├── users/                  # Application gestion utilisateurs
├── subjects/              # Application gestion des sujets
├── projects/              # Application suivi des projets
├── defenses/              # Application planification soutenances
├── communications/        # Application messagerie
├── archives/              # Application archivage
├── static/                # Fichiers statiques (CSS, JS, images)
├── templates/             # Templates HTML globaux
└── media/                 # Fichiers uploadés
```

## 📊 État d'avancement

### ✅ Fonctionnalité 1: Gestion des utilisateurs (COMPLÈTE)
- Authentification et inscription
- Profils personnalisés par rôle
- Tableaux de bord différenciés
- Gestion des profils

### ⏳ Prochaines fonctionnalités
2. Catalogue et affectation des sujets
3. Suivi collaboratif des projets
4. Communication contextualisée
5. Planification automatisée des soutenances
6. Archivage et reporting

## 📚 Documentation

- **PROJET_STATUS.md** - État détaillé du projet
- **FONCTIONNALITE_1_COMPLETE.md** - Documentation de la fonctionnalité 1
- **COMMANDES_RAPIDES.md** - Liste des commandes utiles
- **README.md** - Ce fichier

## 🛠️ Commandes utiles

Voir le fichier **COMMANDES_RAPIDES.md** pour la liste complète.

### Commandes principales
```powershell
# Lancer le serveur
.\run.ps1

# Créer des migrations
.\venv\Scripts\python.exe manage.py makemigrations

# Appliquer les migrations
.\venv\Scripts\python.exe manage.py migrate

# Accéder au shell Django
.\venv\Scripts\python.exe manage.py shell
```

## 🎯 Approche de développement

Le développement se fait **fonctionnalité par fonctionnalité** avec une intégration complète front-end/back-end avant de passer à la suivante. Cela garantit que chaque fonctionnalité est complète, testée et opérationnelle.

## 👥 Rôles utilisateurs

- **Étudiant** - Consulter sujets, gérer son projet, communiquer avec encadreur
- **Encadreur** - Proposer sujets, suivre étudiants, évaluer travaux
- **Administration** - Gérer utilisateurs, valider affectations, planifier soutenances
- **Jury** - Évaluer mémoires, participer aux soutenances

## 🤝 Contribution

Projet académique développé dans le cadre de la formation à l'ENSPD.

## 📝 Licence

Projet académique - ENSPD 2025

---

**Développé avec:** Django 4.2, Bootstrap 5, Font Awesome  
**Architecture:** Monolithique 2-tiers  
**Base de données:** SQLite (développement)
