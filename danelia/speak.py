import pyttsx3
from daneliaprint import dprint
engine = pyttsx3.init()
def talk(words):
    engine.say(words)
    engine.runAndWait()
