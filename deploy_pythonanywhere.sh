#!/bin/bash
# Script de déploiement pour PythonAnywhere
# À exécuter depuis le terminal Bash de PythonAnywhere

set -e  # Arrêter en cas d'erreur

echo "=== Déploiement Gestion PFE sur PythonAnywhere ==="

# Variables - REMPLACEZ AVEC VOS VALEURS
USERNAME="votre-username"
PROJECT_DIR="/home/$USERNAME/gestion-pfe"
VENV_DIR="/home/$USERNAME/.virtualenvs/gestionpfe"

echo "1. Création du répertoire projet..."
mkdir -p $PROJECT_DIR
cd $PROJECT_DIR

echo "2. Clone du repository GitHub..."
if [ ! -d ".git" ]; then
    git clone https://github.com/votre-compte/votre-repo.git .
else
    git pull origin main
fi

echo "3. Création de l'environnement virtuel..."
if [ ! -d "$VENV_DIR" ]; then
    python3.10 -m venv $VENV_DIR
fi

echo "4. Activation de l'environnement virtuel..."
source $VENV_DIR/bin/activate

echo "5. Installation des dépendances..."
pip install --upgrade pip
pip install -r requirements_production.txt

echo "6. Création des répertoires nécessaires..."
mkdir -p logs
mkdir -p staticfiles
mkdir -p media/avatars
mkdir -p media/documents
mkdir -p media/projects

echo "7. Configuration des variables d'environnement..."
cat > .env << EOL
DJANGO_SECRET_KEY='votre-secret-key-ici'
DB_PASSWORD='votre-mot-de-passe-mysql'
EMAIL_HOST_USER='votre-email@gmail.com'
EMAIL_HOST_PASSWORD='votre-mot-de-passe-app-gmail'
EOL

echo "8. Collecte des fichiers statiques..."
python manage.py collectstatic --noinput --settings=config.settings_production

echo "9. Migrations de la base de données..."
python manage.py migrate --settings=config.settings_production

echo "10. Création du superutilisateur..."
echo "Exécutez manuellement: python manage.py createsuperuser --settings=config.settings_production"

echo ""
echo "=== Déploiement terminé avec succès! ==="
echo ""
echo "Prochaines étapes:"
echo "1. Configurez le fichier WSGI dans l'onglet Web de PythonAnywhere"
echo "2. Configurez les chemins statiques et média"
echo "3. Créez le superutilisateur"
echo "4. Rechargez l'application web"
echo ""
