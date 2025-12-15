"""
WSGI config for PythonAnywhere deployment

Instructions:
1. Copiez ce fichier dans /var/www/votre-username_pythonanywhere_com_wsgi.py
2. Remplacez 'votre-username' par votre nom d'utilisateur PythonAnywhere
3. Activez ce fichier dans l'onglet Web de PythonAnywhere
"""

import os
import sys

# Ajoutez le chemin de votre projet
path = '/home/votre-username/gestion-pfe'  # REMPLACEZ votre-username
if path not in sys.path:
    sys.path.insert(0, path)

# Ajoutez le chemin de votre environnement virtuel
venv_path = '/home/votre-username/.virtualenvs/gestionpfe/lib/python3.10/site-packages'
if venv_path not in sys.path:
    sys.path.insert(0, venv_path)

# Configuration Django
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings_production'

# Importation WSGI
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
