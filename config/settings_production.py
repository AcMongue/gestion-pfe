"""
Configuration Django pour déploiement sur PythonAnywhere
"""
from .settings import *
import os

# Charger les variables d'environnement depuis .env
from pathlib import Path
env_file = Path(__file__).resolve().parent.parent / '.env'
if env_file.exists():
    with open(env_file) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ.setdefault(key.strip(), value.strip().strip("'\""))

# SÉCURITÉ
DEBUG = False

# Remplacez par votre domaine PythonAnywhere
ALLOWED_HOSTS = [
    'ac7.pythonanywhere.com',
    'www.ac7.pythonanywhere.com',
]

# SECRET KEY - À générer et configurer via variable d'environnement
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', SECRET_KEY)

# Base de données MySQL sur PythonAnywhere
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ac7$gestionpfe',  # Remplacez votre-username
        'USER': 'ac7',  # Remplacez votre-username
        'PASSWORD': os.environ.get('DB_PASSWORD', ''),  # À configurer
        'HOST': 'ac7.mysql.pythonanywhere-services.com',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
        },
    }
}

# Fichiers statiques
STATIC_ROOT = '/home/ac7/gestion-pfe/staticfiles'  # Remplacez votre-username
STATIC_URL = '/static/'

# Fichiers média
MEDIA_ROOT = '/home/ac7/gestion-pfe/media'  # Remplacez votre-username
MEDIA_URL = '/media/'

# Email - Configuration Gmail pour production
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
SERVER_EMAIL = EMAIL_HOST_USER

# Sécurité HTTPS
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# HSTS (HTTP Strict Transport Security)
SECURE_HSTS_SECONDS = 31536000  # 1 an
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': '/home/votre-username/gestion-pfe/logs/django.log',
            'formatter': 'verbose',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# Cache avec Redis (optionnel, nécessite compte payant sur PythonAnywhere)
# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.redis.RedisCache',
#         'LOCATION': 'redis://127.0.0.1:6379/1',
#     }
# }
