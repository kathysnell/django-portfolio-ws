import re
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def protect_email(value):
    email_pattern = r'mailto:([\w\.-]+)@([\w\.-]+)'
    # Use single quotes (') for the internal strings
    safe_link = r"javascript:window.location.href='mailto:\1' + '@' + '\2'"
    return mark_safe(re.sub(email_pattern, safe_link, value))
