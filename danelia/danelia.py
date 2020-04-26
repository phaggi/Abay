import datetime
import random
import sys
import webbrowser
import speech_recognition as sr
import sqlite3
from urllib.parse import quote
from daneliauiclass import DaneliaUI
import sys  # sys нужен для передачи argv в QApplication
from keymaker import Keymaker
from PyQt5 import QtWidgets
from speak import talk

db = sqlite3.connect('database.db')
c = db.cursor()

anecdote_base = sqlite3.connect('../anekdot/anecdote.db')
a = anecdote_base.cursor()
test = False





def notunderstand():
    _answer = getanswer(sense='notunderstand')[0]
    print(_answer)
    talk(_answer)
    return _answer


def findquestion(_db, _question):
    """
    return sense by question
    :param _question: question
    :return: sense
    """
    _sqlsense = 'select sense from senses where id in ' \
                '(select sense_id from questions where question = "' + _question + '")'
    try:
        _result = _db.execute(_sqlsense)
    except TypeError:
        notunderstand()
        _result = 13
    return _result


def getlanguage():
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
    try:
        _result = findquestion(_db, _exercise).fetchone()[0]
    except TypeError:
        notunderstand()
        _result = 'notunderstand'
    return _result


def openurl(url):
    webbrowser.open(url, new=0, autoraise=True)


def gettownweather():
    _citydetected = False
    while not _citydetected:
        _nameofcity = recognize()
        try:
            _observation = owmengine.weather_at_place(_nameofcity)
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
    talk(translateengine.translate(_name_of_search, _lang))


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
    # TODO: разобраться с костылями!!!
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


def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = DaneliaUI()  # Создаём объект класса DaneliaUI
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение


if __name__ == '__main__':
    securityfile = '../security/danelia.yml'
    km = Keymaker(securityfile)
    owmengine, translateengine = km.getkeys()
    answer = getanswer(sense='talksomething')[0]
    print(answer)
    talk(answer)
    # main()
    test = True
    if not test:
        while True:
            makesomeanother(getcommand(db))
    else:
        while False:
            makesomeanother(getcommand(db))
        # comms = ['name', 'ability', 'ctime', 'stupid1', 'weather', 'find', 'opengoogle', 'stop']
        comms = ['name']
        for comm in comms:
            print(comm)
            makesomeanother(comm)
