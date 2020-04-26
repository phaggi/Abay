import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets

import daneliadesign as ddesign  # Это наш конвертированный файл дизайна

class DaneliaUI(QtWidgets.QMainWindow, ddesign.Ui_MainWindow):
    power = False
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле daneliadesign.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.btnBrowse.clicked.connect(self.switcher)  # Выполнить функцию browse_folder
        # при нажатии кнопки

    def switcher(self):
        self.power = not self.power
        if self.power:
            _words = 'Вкл'
        else:
            _words = 'Выкл'
        self.talk(_words)


    def talk(self, _words):
        self.listWidget.addItem(_words)


def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = DaneliaUI()  # Создаём объект класса DaneliaUI
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение

if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()