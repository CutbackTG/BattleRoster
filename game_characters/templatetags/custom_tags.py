from django import template

register = template.Library()

@register.filter
def get_attr(obj, attr_name):
    """
    Safely get an attribute from a model instance or dictionary.
    Returns 10 as default for numeric attributes (like stats) or '' for strings.
    """
    if obj is None:
        return ''
    numeric_fields = [
        "level", "health", "mana", "strength", "dexterity",
        "constitution", "intelligence", "wisdom", "charisma",
    ]
    if isinstance(obj, dict):
        return obj.get(attr_name, 10 if attr_name in numeric_fields else '')
    return getattr(obj, attr_name, 10 if attr_name in numeric_fields else '')


@register.filter
def getattr_filter(value, arg):
    """Allows {{ object|getattr_filter:'fieldname' }} in templates."""
    return getattr(value, arg, None)
