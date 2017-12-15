from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter(name='shorten')
@stringfilter
def shorten(string, max_length):
    if len(string) > max_length:
        return string[:max_length] + " ..."
    return string
