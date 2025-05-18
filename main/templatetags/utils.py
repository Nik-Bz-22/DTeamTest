from django import template

register = template.Library()


@register.filter
def as_list(obj, attr):
    """
    Unified access to a list:
    - obj — object or dictionary
    - attr — name of the attribute or key
    Returns: obj.attr.all() / obj[attr] / []
    """
    if isinstance(obj, dict):
        value = obj.get(attr, [])
    else:
        value = getattr(obj, attr, [])

    if hasattr(value, "all"):
        return value.all()

    return value or []
