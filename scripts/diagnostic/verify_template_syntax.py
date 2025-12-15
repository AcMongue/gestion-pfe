"""
Vérification rapide de la syntaxe des templates
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.template import Template, Context
from django.template.loader import get_template

def verify_templates():
    """Vérifie que les templates peuvent être chargés sans erreur de syntaxe."""
    print("=" * 80)
    print("VÉRIFICATION DE LA SYNTAXE DES TEMPLATES")
    print("=" * 80)
    
    templates_to_check = [
        'projects/supervisor_students.html',
        'subjects/supervisor_proposals.html',
    ]
    
    for template_path in templates_to_check:
        try:
            template = get_template(template_path)
            print(f"✅ {template_path}: Syntaxe correcte")
        except Exception as e:
            print(f"❌ {template_path}: {str(e)}")
    
    print("\n" + "=" * 80)
    print("✅ Vérification terminée")
    print("=" * 80)

if __name__ == '__main__':
    verify_templates()
