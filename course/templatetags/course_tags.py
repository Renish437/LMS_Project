from django import template

register = template.Library()

@register.filter
def discount_calculation(price, discount):
    """Calculate discounted price"""
    try:
        return price - (price * discount / 100)
    except:
        return price


@register.filter
def half_length(value):
    return len(value) // 2 + len(value) % 2