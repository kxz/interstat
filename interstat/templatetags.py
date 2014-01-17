from itertools import tee
import re
from zlib import adler32

from django import template
from django.template.defaultfilters import stringfilter
from django.utils.html import urlize
from django.utils.safestring import SafeText


register = template.Library()


FORMATTING_BOUNDARIES = re.compile(r"""
    \x02 |            # Bold
    \x03(             # Color
      [0-9]?[0-9](    # Optional foreground number (from 0 or 00 to 99)
        ,[0-9]?[0-9]  # Optional background number (from 0 or 00 to 99)
      )?
    )? |
    \x0F |            # Normal (revert to default formatting)
    \x16 |            # Reverse video (sometimes rendered as italics)
    \x1F |            # Underline
    ^ | $             # Beginning and end of string, for convenience
                      #   This *must* go at the end, otherwise it'll
                      #   take precedence over a control code at the
                      #   start of a string.
    """, re.VERBOSE)


# In order from 0 to 15.
MIRC_COLORS = ['white', 'black', 'navy', 'green',
               'red', 'maroon', 'purple', 'olive',
               'yellow', 'lime', 'teal', 'cyan',
               'royalblue', 'pink', 'gray', 'lightgray']


### Utility methods.

def pairwise(iterable):
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


def toggle(mapping, key, value):
    if key in mapping:
        del mapping[key]
    else:
        mapping[key] = value


### Template tags.

@register.filter
@stringfilter
def colorhash(s):
    """Return an HTML color "hash" for the string *s*."""
    return '#{:03x}'.format(adler32(s) & 0x777)


@register.filter
@stringfilter
def ircformat(message):
    """Given a *message* containing mIRC formatting codes, return an
    HTML rendering."""
    html = ''
    style = {}
    matches = FORMATTING_BOUNDARIES.finditer(message)
    for first, second in pairwise(matches):
        control_code = first.group(0)[:1]
        if control_code == '\x02':
            toggle(style, 'font-weight', 'bold')
        elif control_code == '\x03':
            if first.group(1):
                style['color'] = MIRC_COLORS[int(first.group(1))]
                if first.group(2):
                    style['background-color'] = MIRC_COLORS[int(first.group(2))]
            else:
                style.pop('color', None)
                style.pop('background-color', None)
        elif control_code == '\x0F':
            style.clear()
        elif control_code == '\x16':
            toggle(style, 'font-style', 'italic')
        elif control_code == '\x1F':
            toggle(style, 'text-decoration', 'underline')

        text = urlize(message[first.end():second.start()], autoescape=True)
        if text:  # Don't output empty <span> tags.
            if style:
                css = '; '.join('{}: {}'.format(*s) for s in style.iteritems())
                html += '<span style="{}">{}</span>'.format(css, text)
            else:
                html += text
    return SafeText(html)


template.add_to_builtins(__name__)
