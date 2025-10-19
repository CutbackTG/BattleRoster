from django import template

register = template.Library()

@register.filter
def get_attr(obj, attr_name):
    """
    Safely get an attribute from a model instance or dictionary.
    Returns 10 as default for numeric attributes (like your stats) or '' for strings.
    """
    if obj is None:
        return ''
    if isinstance(obj, dict):
        return obj.get(attr_name, 10 if attr_name in ["level","health","mana","strength","dexterity","constitution","intelligence","wisdom","charisma"] else '')
    return getattr(obj, attr_name, 10 if attr_name in ["level","health","mana","strength","dexterity","constitution","intelligence","wisdom","charisma"] else '')
