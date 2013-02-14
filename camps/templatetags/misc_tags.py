from django import template
from django.utils.safestring import mark_safe
from django.template.defaultfilters import stringfilter
from django.utils.text import normalize_newlines

register = template.Library()


def remove_newlines(text, replacement=' '):
    """
    Removes all newline characters from a block of text.
    """
    normalized_text = normalize_newlines(text)
    return mark_safe(normalized_text.replace('\n', replacement))

remove_newlines.is_safe = True
remove_newlines = stringfilter(remove_newlines)
register.filter(remove_newlines)


def make_latin1(text):
    """
    Return text as Latin-1.
    """
    text = text.replace(u'\u2022', '-')  # Bullet character
    return mark_safe(text.encode('iso-8859-1', 'replace'))

make_latin1.is_safe = True
make_latin1 = stringfilter(make_latin1)
register.filter(make_latin1)
