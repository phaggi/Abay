import pyttsx3
engine = pyttsx3.init()
def talk(words):
    engine.say(words)
    engine.runAndWait()
