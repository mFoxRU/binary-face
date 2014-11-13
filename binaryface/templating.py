__author__ = 'mFoxRU'

import os

from configobj import ConfigObj
from validate import Validator

from imaging import ImageSet


def load_template(template_name='default'):
    """
    Loads template
    :param template_name: Template name. It's the same as template folder name
    in ./templates folder. Template folder must contain config.ini file in it
    If no name is provided the default template will be used
    """
    appdir = os.path.dirname(os.path.realpath(__file__))
    templates_dir = 'templates'
    template_config = os.path.join(appdir, templates_dir, 'tempconf.ini')
    template_dir = os.path.join(appdir, templates_dir, template_name)
    config_filename = os.path.join(template_dir, 'config.ini')
    try:
        template = ConfigObj(config_filename, configspec=template_config,
                             file_error=True)
    except Exception as e:
        exit('Could not read config "{0}". {1}'.format(config_filename, e))
    else:
        validator = Validator()
        is_valid = template.validate(validator)
        if not is_valid:
            exit('Config file validation failed!')
        for set_name in template.sections:
            imagesets, params = {}, {}
            for k, v in template[set_name].items():
                if isinstance(v, dict):
                    imagesets[k] = v
                    imagesets[k]['image'] = os.path.join(template_dir,
                                                         imagesets[k]['image'])
                else:
                    params[k] = v
            ImageSet(set_name, imagesets, **params)