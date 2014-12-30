"""Command line entry points."""


import argparse
import os.path
import sys

from . import as_html
from .formats import formats


def main():
    """Default command line entry point."""
    parser = argparse.ArgumentParser(
        description='Format IRC log files as HTML.')
    parser.add_argument(
        '-f', dest='format', metavar='FORMAT',
        choices=formats, default='omnipresence',
        help='log format (default: omnipresence)')
    parser.add_argument(
        '-l', dest='list_formats', action='store_true',
        help='list known formats and exit')
    parser.add_argument(
        '--stylesheet', metavar='URI',
        help='use stylesheet URI instead of inlining default styles')
    parser.add_argument(
        '--template-dir', metavar='DIR',
        help='override the default templates with those in DIR')
    parser.add_argument(
        '--title',
        help='HTML page <title> (default: log file basename)')
    parser.add_argument(
        'log_file', metavar='LOGFILE',
        nargs='?', type=argparse.FileType('r'), default=sys.stdin,
        help='log file to format (default: stdin)')
    parser.add_argument(
        'html_file', metavar='HTMLFILE',
        nargs='?', type=argparse.FileType('w'), default=sys.stdout,
        help='output HTML file (default: stdout)')
    args = parser.parse_args()
    if args.list_formats:
        print ', '.join(formats)
        return
    title = (args.title or
             os.path.splitext(os.path.basename(args.log_file.name))[0])
    html = as_html(args.log_file, args.format,
                   stylesheet=args.stylesheet,
                   template_dir=args.template_dir,
                   title=title)
    args.html_file.write(html.encode('utf-8'))


if __name__ == '__main__':
    main()
