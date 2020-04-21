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


def talk(words, _engine=engine):
    print(words)
    _engine.say(words)
    _engine.runAndWait()


def findquestion(_db, _question):
    """
    return sense by question
    :param _question: question
    :return: sense
    """
    _sqlsense = 'select sense from senses where id in (select sense_id from questions where question = "' + _question + '")'
    return _db.execute(_sqlsense)


def commands(_db):
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print('Говорите : ')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)
    try:
        _exersize = r.recognize_google(audio, language="ru-Ru").lower()
        print('Вы сказали : ' + _exersize)
    except sr.UnknownValueError:
        talk('Я вас не поняла, повторите пожалуйста')
        _exersize = commands(_db)

    _result = findquestion(_db, _exersize).fetchone()[0]
    return _result


def openurl(url):
    webbrowser.open(url, new=0, autoraise=True)

def gettownweather():
    r = sr.Recognizer()
    with sr.Microphone() as source1:
        audio1 = r.listen(source1)
        nameofcity = r.recognize_google(audio1, language="ru-Ru").lower()
        observation = owm.weather_at_place(nameofcity)
        w = observation.get_weather()
        temp = int(w.get_temperature('celsius')["temp"])
        detail = w.get_detailed_status()
    return nameofcity, temp, detail

def findanswer(_db, _sense, _number = 0):
    """
    return answer by sense
    :param _db: database with answers and senses
    :param _sense: sense
    :return: answer
    """
    if _number == 0:
        _sqlsense = 'SELECT answer, todo FROM answers WHERE sense_id ' \
                    'in (SELECT id FROM senses WHERE sense = "' + _sense + '")'
    else:
        _sqlsense = 'SELECT anecs.anekdot, anecs.todo FROM  (SELECT ROW_NUMBER () OVER ' \
                    '(ORDER BY ROWID) RowNum, anekdot, todo FROM anekdots) ' \
                    'as anecs WHERE anecs.rownum = ' + str(_number)
    _numofanswer = 1
    _sqlreturn = _db.execute(_sqlsense).fetchone()
    if _sqlreturn is None:
        _sense = 'notunderstand'
        _sqlreturn = findanswer(_db, _sense)
    _answer, _todo = _sqlreturn
    if test: print(_sqlreturn)
    return _answer, _todo


def anecdote(_db, _sense):
    _sqlsense = 'SELECT max(anecs.RowNum) FROM (SELECT ROW_NUMBER () ' \
                'OVER (ORDER BY ROWID) RowNum FROM anekdots) as anecs'
    _lenanecdb = int(_db.execute(_sqlsense).fetchone()[0])
    _anecnumber = random.randint(1, _lenanecdb)
    _anec = str(findanswer(_db, _sense, _anecnumber)[0]) + '. Хаха!'
    return _anec



def maketodo(_sense):
    if _sense == 'opengoogle':
        url = 'https://www.google.com/'
        openurl(url)
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
        talk(anecdote(anecdote_base, _sense))
    elif _sense == 'find':
        r = sr.Recognizer()
        with sr.Microphone() as source2:
            audio2 = r.listen(source2)
            nameOFsearch = r.recognize_google(audio2, language="ru-Ru").lower()
        nameOFsearch = quote(nameOFsearch)
        url = 'https://yandex.ru/search/?text=' + nameOFsearch + '&lang=ru'
        if test: print(url)
        webbrowser.open_new_tab(url)
    else:
        pass


def makesomeanother(_db, _sense):
    _answer, _todo = findanswer(_db, _sense)
    talk(_answer)
    if _todo:
        if test: print('тут система должна сделать ', _sense)
        maketodo(_sense)



def makeSomeThing(exersize, _db=db):
    if 'открой гугл' in exersize:
        talk('Сию минуту')
        url = 'https://www.google.com/'
        openurl(url)
    elif 'переведи' in exersize or 'перевод' in exersize or 'переводчик' in exersize:
        talk('На какой язык вы хотите перевести слово?')
        r = sr.Recognizer()
        with sr.Microphone() as source3:
            audio3 = r.listen(source3)
            language = r.recognize_google(audio3, language="ru-Ru").lower()
            if 'французкий' in language or 'французкий' in language:
                nameOFlanguage = 'fr'
            elif 'русский' in language or 'руский' in language:
                nameOFlanguage = 'ru'
            elif 'арабский' in language:
                nameOFlanguage = 'ar'
            elif 'испанский' in language:
                nameOFlanguage = 'es'
            elif 'индонезиский' in language or 'индонезийский' in language:
                nameOFlanguage = 'id'
            elif 'португальский' in language:
                nameOFlanguage = 'pt'
            elif 'бенгальский' in language:
                nameOFlanguage = 'bn'
            elif 'хинди' in language or 'синди' in language or 'бенди' in language:
                nameOFlanguage = 'hi'
            elif 'английский' in language:
                nameOFlanguage = 'en'
            elif 'китайский' in language:
                nameOFlanguage = 'zh'
            elif 'японский' in language:
                nameOFlanguage = 'ja'
            elif 'турецкий' in language:
                nameOFlanguage = 'tr'
            elif 'немецкий' in language:
                nameOFlanguage = 'de'
        try:
            language = r.recognize_google(audio3, language="ru-Ru").lower()
            print('Вы сказали : ' + language)
        except sr.UnknownValueError:
            talk('Я вас не поняла , повторите пожалуйста ')
            language = commands(_db)
            return language
        talk('Какое слово вы хотите перевести ?')
        r = sr.Recognizer()
        with sr.Microphone() as source4:
            audio4 = r.listen(source4)
            nameOFsearch = r.recognize_google(audio4, language="ru-Ru").lower()
        try:
            nameOFsearch = r.recognize_google(audio4, language="ru-Ru").lower()
            print('Вы сказали : ' + nameOFsearch)
        except sr.UnknownValueError:
            talk('Я вас не поняла , повторите пожалуйста ')
            nameOFsearch = commands(_db)
            return nameOFsearch
        talk(tr.translate(nameOFsearch, nameOFlanguage))


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
#talk('Здравствуйте, попросите что-нибудь:')

test = True
if not test:
    while True:
        makeSomeThing(commands(db))
else:
    #comms = ['name', 'ability', 'ctime', 'stupid1', 'weather', 'opengoogle', 'stop']
    comms = ['find']
    for comm in comms:
        makesomeanother(db, comm)
