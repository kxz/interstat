from ..templatetags import ircformat


IRC_AS_HTML = [
    ('regular', 'regular'),
    ('\x02bold', '<span style="font-weight: bold">bold</span>'),
    ('\x02bold\x0F', '<span style="font-weight: bold">bold</span>'),
    ('\x02bold\x02reg', '<span style="font-weight: bold">bold</span>reg'),
    ('\x031colorized', '<span style="color: black">colorized</span>'),
    ('\x031,1colorized',
     '<span style="background-color: black; color: black">colorized</span>'),
    ('\x031,1colorized\x02plus bold',
     '<span style="background-color: black; color: black">colorized</span>'
     '<span style="background-color: black; color: black; '
     'font-weight: bold">plus bold</span>'),
]


def check_html(irc, html):
    assert ircformat(irc) == html

def test_ircformat():
    for irc, html in IRC_AS_HTML:
        yield check_html, irc, html
