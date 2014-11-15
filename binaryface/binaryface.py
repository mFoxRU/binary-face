__author__ = 'mFoxRU'

import argparse
from itertools import izip

from templating import load_template
import imaging


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'filename', metavar='FILE', help='File with data')
    parser.add_argument(
        '-t', action='store', metavar='TEMPLATE', default='default',
        dest='template', help='Template name. Default is "default"')
    parser.add_argument(
        '--sep', action='store', metavar='SEPARATOR', default=',',
        dest='separator',
        help='Separator for attributes. Default is ","')
    parser.add_argument(
        '--spl', action='store', metavar='SPLITTER', default='\n',
        dest='splitter',
        help='Separator for attribute sets. Default is \\n')
    parser.add_argument(
        '--fill', action='store', metavar='VALUE', default='0',
        help='Use VALUE for unused attributes. Default is 0')
    parser.add_argument(
        '--class', choices=('first', 'last', 'no'), default='last',
        dest='classplace',
        help='Define which column contains class attribute. Default is "last"'
    )
    parser.epilog = """
    For more information visit https://github.com/mfoxru/binary-face
    """
    return parser.parse_args()


def read_file(filename, separator, splitter, classplace, **kwargs):
    """
    Reads file and returns attributes and classes lists
    :param filename: Data source
    :param separator: Separator for attribute sets
    :param splitter: Separator for attributes
    :param classplace: Defines which attribute is class attribute. Acceptable
    values: 'first', 'last', 'no'
    :return: 2-item tuple of lists containing attributes and corresponding
    classes. If classplace is 'no' then second list will be empty
    """
    attributes, classes = [], []
    with open(filename, mode='rb') as src:
        for line in src.read().split(splitter):
            items = line.strip().split(separator)
            if classplace == 'first':
                attributes.append(items[1:])
                classes.append(items[0])
            elif classplace == 'last':
                attributes.append(items[:-1])
                classes.append(items[-1])
            else:
                attributes.append(items)
    return attributes, classes


def main():
    conf = parse_args()
    load_template(conf.template)
    data, classes = read_file(**conf.__dict__)
    for attribute_set, set_class in izip(data, classes):
        name = '_'.join(('class', set_class, 'values', ''.join(attribute_set)))
        imaging.ImageSet.make_image(attribute_set, conf.fill, name)

if __name__ == '__main__':
    main()