from random import randint
import random
import urllib.request


class Dprinttest:
    def __init__(self):
        self.text = ''

    def generate_text(self):
        word_url = "http://svnweb.freebsd.org/csrg/share/dict/words?view=co&content-type=text/plain"
        response = urllib.request.urlopen(word_url)
        long_txt = response.read().decode()
        words = long_txt.splitlines()
        upper_words = [Word for Word in words if Word[0].isupper()]
        name_words = [Word for Word in upper_words if not Word.isupper()]
        self.text = ' '.join([name_words[random.randint(0, len(name_words))] for i in range(2)])
        return self.text


if __name__ == '__main__':
    dpr = Dprinttest()
    print(dpr.generate_text(), dpr.generate_text())