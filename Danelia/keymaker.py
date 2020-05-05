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

    def __init__(self, _securityfile: str):
        """
        :param _securityfile: path to YAML file with structure key:value
        """
        self.securityfile = _securityfile

    def getkeys(self):
        """
        :return: (owmkey, yandexkey)
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
            _owmkey = _keychain['owmkey']
            _yandexkey = _keychain['yandexkey']
            return _owmkey, _yandexkey

    def getowmkey(self):
        return self.getkeys()[0]

    def getyandexkey(self):
        return self.getkeys()[1]

    def getowminstance(self):
        return pyowm.OWM(self.getowmkey(), language='ru')

    def getyandexinstance(self):
        return Yandex(self.getyandexkey())


if __name__ == '__main__':
    file = 'danelia_template.yml'
    keyobject = Keymaker(file)
    owmkey, yandexkey = keyobject.getkeys()
    print(owmkey == '97867564' == keyobject.getowmkey())
    print(yandexkey == '13243546' == keyobject.getyandexkey())
    file = '../security/danelia.yml'
    keyobject = Keymaker(file)
    owm = keyobject.getowminstance()
    yandex = keyobject.getyandexinstance()
    print(owm.is_API_online())
    print(yandex.translate('самолет', 'fr', 'ru', 'plain') == 'l\'avion')
