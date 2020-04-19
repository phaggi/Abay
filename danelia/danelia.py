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

engine = pyttsx3.init()
db = sqlite3.connect('database.db')
c = db.cursor()


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

def findanswer(_db, _sense):
    """
    return answer by sense
    :param _db: database with answers and senses
    :param _sense: sense
    :return: answer
    """
    _sqlsense = 'SELECT answer, todo FROM answers WHERE sense_id in (SELECT id FROM senses WHERE sense = "' + _sense + '")'
    _numofanswer = 1
    _sqlreturn = _db.execute(_sqlsense).fetchone()
    if _sqlreturn is None:
        _sense = 'notunderstand'
        _sqlreturn = findanswer(_db, _sense)
    _answer, _todo = _sqlreturn
    if test: print(_sqlreturn)
    return _answer, _todo


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
    elif 'анекдот' in exersize or 'расскажи анекдот' in exersize or 'расскажи шутку' in exersize or 'шутка' in exersize:
        a = random.randint(1, 3)
        if a == 1:
            talk('''Страшные времена. Людям приходится мыть руки, готовить дома
            еду и общаться со своими детьми. Так может дойти и до чтения книг.
            ХА ХА''')
        elif a == 2:
            talk('''Сотрудница отдела продаж, специалист по сервису и их
            начальник идут обедать и находят старую масляную лампу.
            Они трут лампу, и Джин появляется в облаке дыма.
            Джин говорит: — Обычно я выполняю три желания,
            поэтому каждый из Вас может загадать по одному.
            — Чур, я первая!, — говорит сотрудница отдела продаж.
            Я хочу быть сейчас на Багамах, мчаться без забот на скутере
            по волнам. Пуфф! И она растворяется в воздухе.
            — Я следующий!, — говорит спец по сервису. Я хочу на Гавайи,
            расслабляться на пляже с личной массажисткой
            и бесконечным запасом Пина-Колады. Пуфф! Исчезает.
            — OK, твоя очередь!, — говорит Джин менеджеру.
            Тогда менеджер говорит: — Я хочу, чтобы эти двое были в офисе
            после обеда.
            Мораль: Всегда дай начальнику высказаться первым. ха-ха''')

        elif a == 3:
            talk('''Стоит мужик у Кремля с плакатом "Воров на нары".
            Его задерживает полиция за оскорбление власти.
            Мужик: — Да я даже про власть ничего не сказал!
            Полицейские: — А то мы не знаем, кто тут воры...''')

    elif 'найди' in exersize or 'узнай' in exersize:
        talk('Что вас интересует?')
        r = sr.Recognizer()
        with sr.Microphone() as source2:
            audio2 = r.listen(source2)
            nameOFsearch = r.recognize_google(audio2, language="ru-Ru").lower()
        webbrowser.open_new_tab('https://yandex.ru/search/?text=' + nameOFsearch)
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
    #comms = ['name', 'ability', 'ctime', 'weather', 'opengoogle', 'stop']
    comms = ['weather']
    for comm in comms:
        makesomeanother(db, comm)
