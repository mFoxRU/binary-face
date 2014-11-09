__author__ = 'mFoxRU'

import os

from configobj import ConfigObj

from imaging import ImageSet


def load_template(template_name=None):
    if template_name is None:
        template_name = 'default'
    template_dir = os.path.join(os.curdir, 'templates', template_name)
    config_filename = os.path.join(template_dir, 'config.ini')
    try:
        template = ConfigObj(config_filename, file_error=True)
    except Exception as e:
        exit(e)
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