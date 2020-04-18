import speech_recognition as sr
def commands():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print('Говорите : ')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)
    try:
        exersize = r.recognize_google(audio, language="ru-Ru").lower()
        print('Вы сказали : ' + exersize)
    except sr.UnknownValueError:
        talk('Я вас не поняла , повторите пожалуйста ')
        exersize = commands()

    return exersize
