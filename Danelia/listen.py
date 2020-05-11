import speech_recognition as sr
from Danelia.speak import talk


def commands():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print('Говорите: ')
        r.pause_threshold = 1
        r.dynamic_energy_threshold = True

        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)
        print(audio)
    try:
        exersize = r.recognize_google(audio, language="ru-Ru").lower()
        print('Вы сказали: ' + exersize)
    except sr.UnknownValueError:
        talk('Я вас не поняла. Повторите пожалуйста.')
        exersize = commands()

    return exersize


if __name__ == '__main__':
    commands()
