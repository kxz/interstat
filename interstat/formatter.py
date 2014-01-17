from datetime import datetime
import re

from django.conf import settings
from django.template.loader import render_to_string
from pkg_resources import resource_filename

# I'm mildly disgusted that the __name__ import works, but we need it
# later, so let's not look a gift horse in the mouth.
from . import __name__ as package_name, templatetags
from .formats import formats


MESSAGE_TYPES = ['privmsg', 'action', 'notice', 'nick', 'join',
                 'part', 'quit', 'kick', 'topic', 'mode']



class UnknownFormatError(Exception):
    """Raised when an unknown log format is requested."""
    pass


DEFAULT_TEMPLATE_DIR = resource_filename(package_name, 'templates')


def as_html(log_file, format, **kwargs):
    """Return an HTML rendering of an IRC log file, parsed according to
    the given log format."""
    try:
        rules = formats[format]
    except KeyError:
        raise UnknownFormatError(format)
    messages = []
    for i, line in enumerate(log_file):
        match = rules['line'].match(line)
        if match is None:
            # Just don't bother with lines we can't get a timestamp for.
            continue
        message = {}
        message['id'] = 'L{}'.format(i + 1)
        message['timestamp'] = datetime.strptime(
            match.group('timestamp'), rules['timestamp'])
        line = match.group('line')
        for message_type in MESSAGE_TYPES:
            match = rules[message_type].match(line)
            if match is not None:
                message['type'] = message_type
                message.update(match.groupdict())
                break
        else:
            message['type'] = 'misc'
            message['content'] = line
        message['template'] = 'message/{}.html'.format(message['type'])
        messages.append(message)
    kwargs['messages'] = messages
    # Let Django know where our stuff is.
    template_dirs = [DEFAULT_TEMPLATE_DIR]
    if kwargs.get('template_dir'):
        template_dirs.insert(0, kwargs.pop('template_dir'))
    settings.configure(TEMPLATE_DEBUG=True,
                       TEMPLATE_DIRS=template_dirs)
    return render_to_string('log.html', kwargs)
