#!/usr/bin/env python
"""Script pour mettre à jour le statut des sujets existants."""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from subjects.models import Subject

# Mettre à jour tous les sujets en brouillon vers publié
updated = Subject.objects.filter(status='draft').update(status='published')
total_published = Subject.objects.filter(status='published').count()

print(f"✅ {updated} sujet(s) mis à jour de 'brouillon' vers 'publié'")
print(f"📊 Total de sujets publiés: {total_published}")
