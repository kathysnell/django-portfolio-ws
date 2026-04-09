from django import template
from core import constants

register = template.Library()

@register.simple_tag
def get_const(name):
    return getattr(constants, name, "")
