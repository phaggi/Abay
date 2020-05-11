import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets, QtCore
import Danelia.danelia

#  import Danelia.daneliadesign as ddesign  # Это наш конвертированный файл д
from time import sleep
from random import randint

from Danelia.listen import commands
test = False

class Dany:
    def __init__(self):
        pass


class DaneliaThread(QtCore.QThread):
    mysignal = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.runned = False

    # noinspection PyAttributeOutsideInit
    def run(self) -> None:
        self.counter = 0
        while self.runned:
            self.sleep(1)
            self.counter += 1
            if test: print('cycle ', self.counter)
            # noinspection PyAttributeOutsideInit
            self.out_text = str(randint(1, self.counter))
            self.mysignal.emit('out text = ' + self.out_text)


class DaneliaUI(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.setup()

    # noinspection PyAttributeOutsideInit
    def setup(self, *args):
        if len(args) == 0:
            args = ['Данелия - голосовой помощник', 'Говорить']
        self._label_name, self._button_start_name = args
        self.label = QtWidgets.QLabel(self._label_name)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.listWidget = QtWidgets.QListWidget()

        self.h_box = QtWidgets.QHBoxLayout()
        self.button_start = QtWidgets.QPushButton(self._button_start_name)
        self.h_box.addWidget(self.button_start)
        self.v_box = QtWidgets.QVBoxLayout()
        self.v_box.addWidget(self.label)
        self.v_box.addWidget(self.listWidget)
        self.v_box.addLayout(self.h_box)
        self.setLayout(self.v_box)

        self.mythread = DaneliaThread()  # creating instance
        self.button_start.clicked.connect(self.on_clicked)
        self.mythread.started.connect(self.on_started)
        self.mythread.finished.connect(self.on_finished)
        self.mythread.mysignal.connect(self.on_change, QtCore.Qt.QueuedConnection)

    def on_clicked(self):
        if test: print('clicked button')
        # self.button_start.setDisabled(True)
        self.switcher()
        self.mythread.start()

    def on_started(self):
        if test: print('started')
        self.listWidget.clear()
        self.talk('Начали')

        # self.label.setText('called method on_started')

    def on_finished(self):
        if test: print('finished')
        # self.label.setText('called method on_finished')
        self.talk('Кончили')
        # self.button_start.clicked.connect(self.on_clicked)
        # self.button_start.setDisabled(False)

    def on_change(self, _words):
        self.talk(_words)

    def switcher(self):
        self.mythread.runned = not self.mythread.runned
        if test: print('Runned is ', self.mythread.runned)

    def talk(self, _words):
        self.listWidget.addItem(_words)


def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = DaneliaUI()  # Создаём объект класса DaneliaUI
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение


if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    test = True
    main()  # то запускаем функцию main()
