import configparser
from distutils.util import strtobool

import util

configuration = None

def get_property(section: str, option: str, default = None):
    global configuration

    if configuration is None:
        configuration = configparser.ConfigParser()
        _load_properties()

    if not configuration.has_section(section):
        return default
    
    if not (option in configuration[section]):
        return default

    value = configuration.get(section, option)
    if value in ['yes', 'no']:
        return bool(strtobool(value))

    return value
    
def _load_properties():
    configuration.read(util.get_project_root().joinpath('conf.ini'))
