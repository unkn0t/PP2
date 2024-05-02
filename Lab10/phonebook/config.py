from configparser import ConfigParser
from typing import Dict

def load(filename) -> Dict:
    parser = ConfigParser()
    parser.read(filename)

    config = {}
    if parser.has_section('postgresql'):
        params = parser.items('postgresql')
        for param in params:
            config[param[0]] = param[1]
    else:
        raise Exception(f'Section postgresql not found in the {filename} file')

    return config
