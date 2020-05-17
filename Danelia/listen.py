import speech_recognition as sr
from Danelia.speak import talk

test = False


def commands():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print('Говорите: ')
        r.pause_threshold = 1
        r.dynamic_energy_threshold = True

        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)
        if test:
            assert isinstance(audio, sr.AudioData)
            print(audio)
        try:
            exercise = r.recognize_google(audio, language="ru-Ru").lower()
            print('Вы сказали: ' + exercise)
        except sr.UnknownValueError:
            talk('Я вас не поняла. Повторите пожалуйста.')
            exercise = commands()

    return exercise


if __name__ == '__main__':
    test = True
    commands()
