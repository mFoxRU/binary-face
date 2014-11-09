__author__ = 'mFoxRU'

import argparse

from templating import load_template


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'f', metavar='FILE', help='File with data')
    parser.add_argument(
        '-t', action='store', metavar='TEMPLATE', default='default',
        dest='template', help='Template name. Default is "default"')
    parser.add_argument(
        '--sep', action='store', metavar='SEPARATOR', default=',',
        help='Separator for attributes. Default is ","')
    parser.add_argument(
        '--spl', action='store', metavar='SPLITTER', default='\n',
        help='Separator for attribute sets. Default is \\n')
    parser.add_argument(
        '--fill', action='store', metavar='VALUE', default=0,
        help='Use VALUE for unused attributes. Default is 0')
    parser.add_argument(
        '--class', choices=('first', 'last', 'no'), default='last',
        help='Define which column contains class attribute. Default is "last"'
    )
    parser.epilog = """
    For more information visit https://github.com/mfoxru/binary-face
    """
    return parser.parse_args()


def main():
    conf = parse_args()
    load_template(conf.template)

if __name__ == '__main__':
    main()