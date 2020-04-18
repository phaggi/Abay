import pyttsx3
engine = pyttsx3.init()
def talk(words):
    print(words)
    engine.say(words)
    engine.runAndWait()
