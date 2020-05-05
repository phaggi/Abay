import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets


import daneliadesign as ddesign  # Это наш конвертированный файл д
from time import sleep
from random import randint

from PyQt5.QtCore import QTimer


class DaneliaUI(QtWidgets.QMainWindow, ddesign.Ui_MainWindow):
    power = False

    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле daneliadesign.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.btnBrowse.clicked.connect(self.switcher)  # Выполнить функцию
        self.timer = QTimer()
        self.index = 0

        # при нажатии кнопки

    '''def switcher(self):
        self.power = not self.power
        if self.power:
            _words = 'Вкл'
        else:
            _words = 'Выкл'
        self.talk(_words)
        self.generate_text()
'''
    def switcher(self):
        self.index = 0
        self.power = not self.power
        print(self.power)
        self.timer.timeout.connect(self.generate_text())
        self.timer.start(1000)
        self.talk(str(self.power))
        print('printed')

    def talk(self, _words):
        self.listWidget.addItem(_words)

    def clear(self):
        self.listWidget.clear()

    def in_text(self):
        pass

    def generate_text(self):
        self.clear()
        string = 'цикл ' +  str(self.index)
        print(string)
        self.talk(string)
        self.index += 1
        if self.index == 5:
            self.timer.stop()

def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = DaneliaUI()  # Создаём объект класса DaneliaUI
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение


if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()
