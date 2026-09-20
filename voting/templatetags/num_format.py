from django import template

register = template.Library()


@register.filter
def thou(value):
    """Format a number with thousands separators, e.g. 1350 -> 1,350."""
    try:
        return f"{int(float(value)):,}"
    except (TypeError, ValueError):
        return value


@register.filter
def initials(value):
    """Build up to two-letter initials from a person's name."""
    parts = [p for p in str(value).split() if p]
    if not parts:
        return "?"
    return "".join(p[0] for p in parts[:2]).upper()


@register.filter
def minus(value, arg):
    try:
        return round(float(value) - float(arg), 1)
    except (TypeError, ValueError):
        return 0