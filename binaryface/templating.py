__author__ = 'mFoxRU'

import os

from configobj import ConfigObj


def _read_template_config(template_name):
    template_filename = os.path.join(
        os.curdir,
        'templates',
        template_name,
        'config.ini'
    )
    try:
        config = ConfigObj(template_filename, file_error=True)
    except Exception as e:
        exit(e)
    else:
        #ToDo: Add validation
        return config


def load_template(template_name=None):
    if template_name is None:
        template_name = 'default'
    template = _read_template_config(template_name)

