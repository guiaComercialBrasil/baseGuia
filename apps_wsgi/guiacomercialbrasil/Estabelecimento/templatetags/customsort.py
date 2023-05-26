from django import template
from django.template.defaultfilters import _property_resolver
from unidecode import unidecode

register = template.Library()

@register.filter
def customsort(value, arg):
    ''' Sort a list of dictionaries based on property'''
    return value.order_by(unidecode(arg))
