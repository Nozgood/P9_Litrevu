from django import template
from litrevu_management.models import Review

# register create an instance of Library to register my filter
register = template.Library()


# register_filter decorator allow me to declare a function as filter
@register.filter(name="hasattr")
def hasattr_filter(value, arg):
    return hasattr(value, arg)


@register.filter(name="has_review")
def has_review(ticket):
    return Review.objects.filter(ticket=ticket).exists()
