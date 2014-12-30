"""Unit tests for basic IRC message formatting."""
# pylint: disable=missing-docstring


import unittest

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


class TemplateTagsTestCase(unittest.TestCase):
    def test_ircformat(self):
        for irc, html in IRC_AS_HTML:
            self.assertEqual(ircformat(irc), html)
