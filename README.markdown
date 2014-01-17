# Interstat

A simple HTML formatter for IRC log files.
Right now, it only supports the format used by [Omnipresence][omni], but
it should be easy enough to extend to other formats.

[omni]: https://bitbucket.org/kxz/omnipresence

Yes, it requires Django.
Sorry, I'm lazy.

Install it with:

    $ python setup.py install

Then run:

    $ interstat LOGFILE HTMLFILE

If you want to change the generated HTML or CSS, copy the files in the
`interstat/templates` directory that you want to override, make your
changes, and run:

    $ interstat --template-dir my-templates/ LOGFILE HTMLFILE

For more options, try:

    $ interstat --help

Interstat also provides a Python API, in case that's more your thing:

    import interstat
    # To convert an entire log file to an HTML string:
    foo = interstat.as_html(open('irc.log'), 'omnipresence')
    # To convert text with mIRC formatting codes to HTML:
    bar = interstat.ircformat('\x02Bold\x02 and \x1Funderlined\x1F, oh my!')
