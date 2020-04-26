import yaml
import re
from yandex import Yandex
import pyowm


class Keymaker:
    '''
    return Yandex (yandexkey) and owm (owmkey:) keys from .yml
    '''
    trkey = 'yandexkey'
    owmkey = 'owmkey'

    def __init__(self, _securityfile):
        self.securityfile = _securityfile

    def getkeys(self):
        """
        make global variables by keys from yaml
        :param _securityfile: path to YAML file with structure key:value
        :return: None
        """
        _PATTERN = r'^\s*(.+)\:(.+)$'
        _templates = ''
        _result = False
        try:
            with open(self.securityfile, 'r') as _yaml:
                _templates = yaml.safe_load(_yaml).split()
        except FileNotFoundError:
            print('File ', self.securityfile, 'not found')
            _result = False
        else:
            _keychain = dict()
            for _data in _templates:
                _data = re.findall(_PATTERN, _data)
                _keychain.update({_data[0][0]: _data[0][1]})
            _result = True
        finally:
            _owm = pyowm.OWM(_keychain[self.trkey], language='ru')
            _tr = Yandex(_keychain[self.owmkey])
            return _owm, _tr
