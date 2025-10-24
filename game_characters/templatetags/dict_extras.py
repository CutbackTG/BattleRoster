from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """
    Retrieve an item from a dictionary safely in Django templates.
    Usage: {{ mydict|get_item:mykey }}
    """
    if isinstance(dictionary, dict):
        return dictionary.get(key)
    return None
