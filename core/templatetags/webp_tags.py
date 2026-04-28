from django import template
import os

register = template.Library()

@register.filter
def to_webp(value):
    # Convert the file extension to .webp
    root, ext = os.path.splitext(value)
    return f"{root}.webp"
