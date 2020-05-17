import pyttsx3
from Danelia.dprint import ui_print

engine = pyttsx3.init()


def talk(_words):
    engine.say(_words)
    ui_print(_words)
    engine.runAndWait()


if __name__ == '__main__':
    talk('Меня зовут Данелия')
