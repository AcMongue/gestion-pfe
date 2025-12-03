from django import template

register = template.Library()

@register.filter(name='split')
def split(value, arg):
    """Sépare une chaîne avec le séparateur spécifié."""
    if value:
        return value.split(arg)
    return []
