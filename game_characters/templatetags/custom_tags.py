from django import template

register = template.Library()

@register.filter
def get_attr(obj, attr):
    """Safely get an attribute from a model instance or dictionary."""
    if isinstance(obj, dict):
        return obj.get(attr, '')
    return getattr(obj, attr, '')
