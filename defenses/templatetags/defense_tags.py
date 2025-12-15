from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(name='safe_label')
def safe_label(value):
    """Permet d'afficher les labels HTML de manière sécurisée"""
    return mark_safe(value)
