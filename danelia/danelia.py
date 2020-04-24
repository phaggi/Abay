import datetime
import random
import sys
import webbrowser
import pyowm
import pyttsx3
import speech_recognition as sr
from yandex import Yandex
import yaml
import re
import sqlite3
from urllib.parse import quote

engine = pyttsx3.init()
db = sqlite3.connect('database.db')
c = db.cursor()

anecdote_base = sqlite3.connect('../anekdot/anecdote.db')
a = anecdote_base.cursor()


def keymaker(_securityfile):
    """
    make global variables by keys from yaml
    :param _securityfile: path to YAML file with structure key:value
    :return: None
    """
    _PATTERN = r'^\s*(.+)\:(.+)$'
    _templates = ''
    _result = False
    try:
        with open(_securityfile, 'r') as _yaml:
            _templates = yaml.safe_load(_yaml).split()
    except FileNotFoundError:
        print('File ', _securityfile, 'not found')
        _result = False
    else:
        _keychain = dict()
        for _data in _templates:
            _data = re.findall(_PATTERN, _data)
            _keychain.update({_data[0][0]: _data[0][1]})
        _keynames = _keychain.keys()
        for _name in _keynames:
            globals().update({_name: _keychain[_name]})
        _result = True
    finally:
        return _result


def talk(_words, _engine=engine):
    if test: print('talk: ', _words)
    _engine.say(_words)
    _engine.runAndWait()


def notunderstand():
    _answer = getanswer(sense='notunderstand')[0]
    print(_answer)
    talk(_answer)


def findquestion(_db, _question):
    """
    return sense by question
    :param _question: question
    :return: sense
    """
    _sqlsense = 'select sense from senses where id in (select sense_id from questions where question = "' + _question + '")'
    return _db.execute(_sqlsense)


def getlanguage():
    TODO: get language from SQL
    _lanquagedetected = False
    while not _lanquagedetected:
        try:
            _language = recognize()
            print('Вы сказали: ' + _language)
            _lang = getanswer(sense='translate2', language=_language)[0]
            _lanquagedetected = True
        except:
            notunderstand()
    if test: print(_language, _lang)
    return _language, _lang


def getcommand(_db):
    try:
        _exercise = recognize()
        print(getanswer(sense='yousayd')[0] + _exercise)
    except sr.UnknownValueError:
        notunderstand()
        _exercise = getcommand(_db)
    _result = findquestion(_db, _exercise).fetchone()[0]
    return _result


def openurl(url):
    webbrowser.open(url, new=0, autoraise=True)


def gettownweather():
    _citydetected = False
    while not _citydetected:
        _nameofcity = recognize()
        try:
            _observation = owm.weather_at_place(_nameofcity)
            _citydetected = True
        except pyowm.exceptions.api_response_error.NotFoundError:
            notunderstand()
    _weather = _observation.get_weather()
    _temp = int(_weather.get_temperature('celsius')["temp"])
    _detail = _weather.get_detailed_status()
    return _nameofcity, _temp, _detail


def recognize():
    _recognizer = sr.Recognizer()
    with sr.Microphone() as _source:
        audio3 = _recognizer.listen(_source)
        try:
            _result = _recognizer.recognize_google(audio3, language="ru-Ru").lower()
        except sr.UnknownValueError:
            _result = ''
    if test: print(_result)
    return _result


def translate():
    _db = db
    _language, _lang = getlanguage()
    talk('Какое слово вы хотите перевести?')
    try:
        _name_of_search = recognize()
        print('Вы сказали : ' + _name_of_search)
    except sr.UnknownValueError:
        if test: print('Error in translate')
        notunderstand()
        _name_of_search = getcommand(_db)
        return _name_of_search
    talk(tr.translate(_name_of_search, _lang))

def getanecdotenumber(_db):
    _sqlsense = 'SELECT max(anecs.RowNum) FROM (SELECT ROW_NUMBER () ' \
                'OVER (ORDER BY ROWID) RowNum FROM anekdots) as anecs'
    _lenanecdb = int(_db.execute(_sqlsense).fetchone()[0])
    _anecnumber = random.randint(1, _lenanecdb)
    return _anecnumber


def generatesqlstring(**kwargs):
    if test: print('generatestring kwargs: ', kwargs)
    if 'sense' in kwargs.keys():
        _sense = kwargs['sense']
    if 'language' in kwargs.keys():
        _language = kwargs['language']
        if test: print('generatestring lang :', _language)
    if test: print('generatesqlstring sense: ', _sense)
    if _sense not in ['stupid2', 'translate2']:
        _db = db
        _sqlstring = 'SELECT answer, todo FROM answers WHERE sense_id ' \
                     'in (SELECT id FROM senses WHERE sense = "' + _sense + '")'
    elif _sense is 'stupid2':
        _db = anecdote_base
        _number = getanecdotenumber(_db)
        if test: print(_number)
        _sqlstring = 'SELECT anecs.anekdot, anecs.todo FROM  (SELECT ROW_NUMBER () OVER ' \
                     '(ORDER BY ROWID) RowNum, anekdot, todo FROM anekdots) ' \
                     'as anecs WHERE anecs.rownum = ' + str(_number)
    if _sense is 'translate2':
        _db = db
        _sqlstring = 'SELECT lang FROM languages WHERE word = "' + _language + '"'
    if test: print('generated sqlstring: ', _sqlstring)
    return _db, _sqlstring


def getanswer(**kwargs):
    #TODO: разобраться с костылями!!!
    if test: print('getanswer kwargs: ', kwargs)
    if 'sense' in kwargs.keys():
        _sense = kwargs['sense']
    if 'language' in kwargs.keys():
        _language = kwargs['language']
        if test: print('getanswer lang :', _language)
        _db, _sqlstring = generatesqlstring(sense=_sense, language=_language)
    else:
        _db, _sqlstring = generatesqlstring(sense=_sense)
    if test: print('getanswer string:', _sqlstring)
    try:
        _sqlreturn = _db.execute(str(_sqlstring)).fetchone()
        if test: print('getanswer sqlreturn: ', _sqlreturn)
    except:
        if test: print('Error in getanswer')
    return _sqlreturn


def maketodo(_sense):
    if _sense == 'opengoogle':
        _url = 'https://www.google.com/'
        openurl(_url)
    elif _sense == 'stop':
        sys.exit()
    elif _sense == 'ctime':
        now = datetime.datetime.now()
        talk(str(now.hour) + ':' + str(now.minute))
    elif _sense == 'weather':
        nameofcity, temp, detail = gettownweather()
        talk(' В городе ' + str(nameofcity).capitalize() + ' сейчас ' + str(detail))
        talk('Температура в районе ' + str(temp) + ' градусов')
    elif _sense == 'stupid1':
        talk(getanswer(sense='stupid2')[0])
    elif _sense == 'find':
        _nameofsearch = quote(recognize())
        _url = 'https://yandex.ru/search/?text=' + _nameofsearch + '&lang=ru'
        if test: print(_url)
        openurl(_url)
    elif _sense == 'translate':
        translate()
    else:
        pass


def makesomeanother(_sense):
    # _answer, _todo = findanswer(_db, _sense)
    _answer, _todo = getanswer(sense=_sense)

    talk(_answer)
    if _todo:
        if test: print('тут система должна сделать ', _sense)
        maketodo(_sense)


if __name__ == '__main__':

    '''
    ниже лучше добавлять переменные для ключей из YAML файла security/danelia.yml
    для явной видимости переменных и чтоб не ругался линтер, что переменная не задана
    '''
    owmkey = ''
    yandexkey = ''
    '''
    переменные досюда
    '''

    securityfile = '../security/danelia.yml'
    result = keymaker(securityfile)
    if not result:
        print('!!! Что-то с файлом ключей !!!')
        quit()

    owm = pyowm.OWM(owmkey, language='ru')
    tr = Yandex(yandexkey)

# cmds = {
# "ctime": ('текущее время','сейчас времени', 'который час'),
# "radio": ('включи музыку', 'воспроизведи радио', 'включи радио'),
# "stupid1": ('расскажи анекдот', 'рассмещи меня', 'ты знаешь анекдот')
# }
# chromepath = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe'
# webbrowser.register('Chrome', None, webbrowser.BackgroundBrowser(chromepath))
'''
engine = pyttsx3.init()
db = sqlite3.connect('database.db')
c = db.cursor()
'''
# talk('Здравствуйте, попросите что-нибудь:')

test = True
if not test:
    while True:
        makeSomeThing(getcommand(db))
else:
    comms = ['name', 'ability', 'ctime', 'stupid1', 'weather', 'find', 'opengoogle', 'stop']
    #comms = ['translate']
    for comm in comms:
        print(comm)
        makesomeanother(comm)