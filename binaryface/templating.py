__author__ = 'mFoxRU'

import os

from configobj import ConfigObj

from imaging import ImageSet


def load_template(template_name='default'):
    """
    Loads template
    :param template_name: Template name. It's the same as template folder name
    in ./templates folder. Template folder must contain config.ini file in it
    If no name is provided the default template will be used
    """
    template_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                'templates', template_name)
    config_filename = os.path.join(template_dir, 'config.ini')
    try:
        template = ConfigObj(config_filename, file_error=True)
    except Exception as e:
        exit('Could not read config file "{0}". {1}'.format(config_filename,
                                                            e))
    else:
        #ToDo: Add validation
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