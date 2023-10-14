from django import template

# register create an instance of Library to register my filter
register = template.Library()


# register_filter decorator allow me to declare a function as filter
@register.filter(name="hasattr")
def hasattr_filter(value, arg):
    return hasattr(value, arg)
