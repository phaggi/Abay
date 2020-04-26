# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'danelia/ddesign.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(410, 318)
        MainWindow.setStyleSheet("background-color: rgb(0, 0, 0);\n"
"")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setFocusPolicy(QtCore.Qt.NoFocus)
        self.listWidget.setStyleSheet("color: rgb(255, 0, 0);\n"
"font: 24pt \"Myriad CAD\";")
        self.listWidget.setObjectName("listWidget")
        self.verticalLayout.addWidget(self.listWidget)
        self.btnBrowse = QtWidgets.QPushButton(self.centralwidget)
        self.btnBrowse.setMinimumSize(QtCore.QSize(0, 50))
        font = QtGui.QFont()
        font.setFamily("Myriad CAD")
        font.setPointSize(24)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(3)
        self.btnBrowse.setFont(font)
        self.btnBrowse.setMouseTracking(False)
        self.btnBrowse.setStyleSheet("QPushButton{\n"
"    font: 25 24pt \"Myriad CAD\";\n"
"    border: none;\n"
"    color: rgb(255, 0, 0);\n"
"    background-color: rgb(0, 0, 0);\n"
"}\n"
"QPushButton:hover{\n"
"    \n"
"    color: rgb(0, 0, 255);\n"
"}\n"
"QPushButton:pressed{\n"
"    color: rgb(255, 255, 0);\n"
"}\n"
"")
        self.btnBrowse.setObjectName("btnBrowse")
        self.verticalLayout.addWidget(self.btnBrowse)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Dialog"))
        self.btnBrowse.setText(_translate("MainWindow", "ПОГОВОРИТЬ"))

