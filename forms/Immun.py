# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.3.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QGroupBox, QLabel,
    QPushButton, QSizePolicy, QTextEdit, QWidget)

class Ui_Widget(object):
    def setupUi(self, Widget):
        if not Widget.objectName():
            Widget.setObjectName(u"Widget")
        Widget.resize(1422, 694)
        font = QFont()
        font.setPointSize(1)
        Widget.setFont(font)
        Widget.setAutoFillBackground(False)
        Widget.setStyleSheet(u"background-color: rgb(64, 65, 66);")
        self.groupBox = QGroupBox(Widget)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(20, 50, 831, 631))
        self.label = QLabel(Widget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(10, 0, 1401, 41))
        font1 = QFont()
        font1.setFamilies([u"Old English Text MT"])
        font1.setPointSize(16)
        font1.setBold(True)
        self.label.setFont(font1)
        self.label.setStyleSheet(u"color: rgb(190, 192, 193);")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setMargin(50)
        self.Start = QPushButton(Widget)
        self.Start.setObjectName(u"Start")
        self.Start.setGeometry(QRect(1280, 550, 131, 51))
        font2 = QFont()
        font2.setFamilies([u"Yu Gothic UI Semibold"])
        font2.setPointSize(12)
        font2.setBold(True)
        self.Start.setFont(font2)
        self.Start.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.textEdit = QTextEdit(Widget)
        self.textEdit.setObjectName(u"textEdit")
        self.textEdit.setGeometry(QRect(1309, 150, 101, 30))
        self.textEdit.setBaseSize(QSize(0, 0))
        font3 = QFont()
        font3.setFamilies([u"Yu Gothic UI"])
        font3.setPointSize(16)
        self.textEdit.setFont(font3)
        self.textEdit.setAcceptDrops(True)
        self.textEdit.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"")
        self.textEdit.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.label_2 = QLabel(Widget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(900, 150, 401, 30))
        font4 = QFont()
        font4.setFamilies([u"Yu Gothic UI Semibold"])
        font4.setPointSize(14)
        font4.setBold(True)
        self.label_2.setFont(font4)
        self.label_2.setStyleSheet(u"color: rgb(190, 192, 193);")
        self.label_2.setTextFormat(Qt.PlainText)
        self.label_2.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.label_5 = QLabel(Widget)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(871, 190, 431, 30))
        self.label_5.setFont(font4)
        self.label_5.setStyleSheet(u"color: rgb(190, 192, 193);")
        self.label_5.setTextFormat(Qt.PlainText)
        self.label_5.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.label_6 = QLabel(Widget)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(870, 230, 431, 30))
        self.label_6.setFont(font4)
        self.label_6.setStyleSheet(u"color: rgb(190, 192, 193);")
        self.label_6.setTextFormat(Qt.PlainText)
        self.label_6.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.label_7 = QLabel(Widget)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setGeometry(QRect(870, 310, 431, 30))
        self.label_7.setFont(font4)
        self.label_7.setStyleSheet(u"color: rgb(190, 192, 193);")
        self.label_7.setTextFormat(Qt.PlainText)
        self.label_7.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.Clear = QPushButton(Widget)
        self.Clear.setObjectName(u"Clear")
        self.Clear.setGeometry(QRect(1170, 550, 101, 51))
        self.Clear.setFont(font2)
        self.Clear.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.pushButton_3 = QPushButton(Widget)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setGeometry(QRect(1010, 550, 151, 51))
        self.pushButton_3.setFont(font2)
        self.pushButton_3.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.label_8 = QLabel(Widget)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setGeometry(QRect(900, 270, 401, 31))
        self.label_8.setFont(font4)
        self.label_8.setStyleSheet(u"color: rgb(190, 192, 193);")
        self.label_8.setTextFormat(Qt.PlainText)
        self.label_8.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.textEdit_6 = QTextEdit(Widget)
        self.textEdit_6.setObjectName(u"textEdit_6")
        self.textEdit_6.setGeometry(QRect(1010, 650, 401, 30))
        font5 = QFont()
        font5.setFamilies([u"Yu Gothic UI Semibold"])
        font5.setPointSize(16)
        font5.setBold(True)
        self.textEdit_6.setFont(font5)
        self.textEdit_6.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.textEdit_6.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.label_9 = QLabel(Widget)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setGeometry(QRect(1000, 610, 381, 30))
        self.label_9.setFont(font5)
        self.label_9.setStyleSheet(u"color: rgb(190, 192, 193);")
        self.label_9.setTextFormat(Qt.PlainText)
        self.label_9.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.label_10 = QLabel(Widget)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setGeometry(QRect(870, 350, 431, 30))
        self.label_10.setFont(font4)
        self.label_10.setStyleSheet(u"color: rgb(190, 192, 193);")
        self.label_10.setTextFormat(Qt.PlainText)
        self.label_10.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.label_11 = QLabel(Widget)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setGeometry(QRect(1000, 390, 301, 31))
        self.label_11.setFont(font4)
        self.label_11.setStyleSheet(u"color: rgb(190, 192, 193);")
        self.label_11.setTextFormat(Qt.PlainText)
        self.label_11.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.label_3 = QLabel(Widget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(1000, 50, 251, 30))
        self.label_3.setFont(font5)
        self.label_3.setStyleSheet(u"color: rgb(190, 192, 193);")
        self.label_3.setTextFormat(Qt.PlainText)
        self.label_3.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.comboBox = QComboBox(Widget)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setGeometry(QRect(1010, 90, 401, 41))
        self.comboBox.setFont(font4)
        self.comboBox.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"")
        self.textEdit_2 = QTextEdit(Widget)
        self.textEdit_2.setObjectName(u"textEdit_2")
        self.textEdit_2.setGeometry(QRect(1310, 190, 101, 30))
        self.textEdit_2.setBaseSize(QSize(0, 0))
        self.textEdit_2.setFont(font3)
        self.textEdit_2.setAcceptDrops(True)
        self.textEdit_2.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"")
        self.textEdit_2.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.textEdit_3 = QTextEdit(Widget)
        self.textEdit_3.setObjectName(u"textEdit_3")
        self.textEdit_3.setGeometry(QRect(1310, 230, 101, 30))
        self.textEdit_3.setBaseSize(QSize(0, 0))
        self.textEdit_3.setFont(font3)
        self.textEdit_3.setAcceptDrops(True)
        self.textEdit_3.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"")
        self.textEdit_3.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.textEdit_4 = QTextEdit(Widget)
        self.textEdit_4.setObjectName(u"textEdit_4")
        self.textEdit_4.setGeometry(QRect(1310, 270, 101, 30))
        self.textEdit_4.setBaseSize(QSize(0, 0))
        self.textEdit_4.setFont(font3)
        self.textEdit_4.setAcceptDrops(True)
        self.textEdit_4.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"")
        self.textEdit_4.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.textEdit_5 = QTextEdit(Widget)
        self.textEdit_5.setObjectName(u"textEdit_5")
        self.textEdit_5.setGeometry(QRect(1310, 310, 101, 30))
        self.textEdit_5.setBaseSize(QSize(0, 0))
        self.textEdit_5.setFont(font3)
        self.textEdit_5.setAcceptDrops(True)
        self.textEdit_5.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"")
        self.textEdit_5.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.textEdit_7 = QTextEdit(Widget)
        self.textEdit_7.setObjectName(u"textEdit_7")
        self.textEdit_7.setGeometry(QRect(1310, 350, 101, 30))
        self.textEdit_7.setBaseSize(QSize(0, 0))
        self.textEdit_7.setFont(font3)
        self.textEdit_7.setAcceptDrops(True)
        self.textEdit_7.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"")
        self.textEdit_7.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.textEdit_8 = QTextEdit(Widget)
        self.textEdit_8.setObjectName(u"textEdit_8")
        self.textEdit_8.setGeometry(QRect(1310, 390, 101, 30))
        self.textEdit_8.setBaseSize(QSize(0, 0))
        self.textEdit_8.setFont(font3)
        self.textEdit_8.setAcceptDrops(True)
        self.textEdit_8.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"")
        self.textEdit_8.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.label_12 = QLabel(Widget)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setGeometry(QRect(1000, 430, 301, 31))
        self.label_12.setFont(font4)
        self.label_12.setStyleSheet(u"color: rgb(190, 192, 193);")
        self.label_12.setTextFormat(Qt.PlainText)
        self.label_12.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.textEdit_9 = QTextEdit(Widget)
        self.textEdit_9.setObjectName(u"textEdit_9")
        self.textEdit_9.setGeometry(QRect(1310, 430, 101, 30))
        self.textEdit_9.setBaseSize(QSize(0, 0))
        self.textEdit_9.setFont(font3)
        self.textEdit_9.setAcceptDrops(True)
        self.textEdit_9.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"")
        self.textEdit_9.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.label_13 = QLabel(Widget)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setGeometry(QRect(1000, 470, 301, 31))
        self.label_13.setFont(font4)
        self.label_13.setStyleSheet(u"color: rgb(190, 192, 193);")
        self.label_13.setTextFormat(Qt.PlainText)
        self.label_13.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.textEdit_10 = QTextEdit(Widget)
        self.textEdit_10.setObjectName(u"textEdit_10")
        self.textEdit_10.setGeometry(QRect(1310, 470, 101, 30))
        self.textEdit_10.setBaseSize(QSize(0, 0))
        self.textEdit_10.setFont(font3)
        self.textEdit_10.setAcceptDrops(True)
        self.textEdit_10.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"")
        self.textEdit_10.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.label_14 = QLabel(Widget)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setGeometry(QRect(910, 510, 391, 31))
        self.label_14.setFont(font4)
        self.label_14.setStyleSheet(u"color: rgb(190, 192, 193);")
        self.label_14.setTextFormat(Qt.PlainText)
        self.label_14.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.textEdit_11 = QTextEdit(Widget)
        self.textEdit_11.setObjectName(u"textEdit_11")
        self.textEdit_11.setGeometry(QRect(1310, 510, 101, 30))
        self.textEdit_11.setBaseSize(QSize(0, 0))
        self.textEdit_11.setFont(font3)
        self.textEdit_11.setAcceptDrops(True)
        self.textEdit_11.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"")
        self.textEdit_11.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.retranslateUi(Widget)

        QMetaObject.connectSlotsByName(Widget)
    # setupUi

    def retranslateUi(self, Widget):
        Widget.setWindowTitle("Иммунная сеть")
        self.groupBox.setTitle(QCoreApplication.translate("Widget", u"GroupBox", None))
        self.label.setText(QCoreApplication.translate("Widget", u"\u0410\u043b\u0433\u043e\u0440\u0438\u0442\u043c \u0438\u0441\u0441\u043a\u0443\u0441\u0442\u0432\u0435\u043d\u043d\u043e\u0439 \u0438\u043c\u043c\u0443\u043d\u043d\u043e\u0439 \u0441\u0435\u0442\u0438", None))
        self.Start.setText(QCoreApplication.translate("Widget", u"\u0417\u0430\u043f\u0443\u0441\u0442\u0438\u0442\u044c", None))
        self.label_2.setText(QCoreApplication.translate("Widget", u"\u0413\u0440\u0430\u043d\u0438\u0446\u044b:", None))
        self.label_5.setText(QCoreApplication.translate("Widget", u"\u0420\u0430\u0437\u043c\u0435\u0440 \u043d\u0430\u0447\u0430\u043b\u044c\u043d\u043e\u0439 \u043f\u043e\u043f\u0443\u043b\u044f\u0446\u0438\u0438 \u0430\u043d\u0442\u0438\u0442\u0435\u043b:", None))
        self.label_6.setText(QCoreApplication.translate("Widget", u"\u0420\u0430\u0437\u043c\u0435\u0440 \u043d\u0430\u0447\u0430\u043b\u044c\u043d\u043e\u0439 \u043f\u043e\u043f\u0443\u043b\u044f\u0446\u0438\u0438 \u0430\u043d\u0442\u0438\u0433\u0435\u043d\u043e\u0432:", None))
        self.label_7.setText(QCoreApplication.translate("Widget", u"\u0427\u0438\u0441\u043b\u043e \u043e\u0441\u0442\u0430\u0432\u043b\u044f\u0435\u043c\u044b\u0445 \u043a\u043b\u043e\u043d\u043e\u0432:", None))
        self.Clear.setText(QCoreApplication.translate("Widget", u"\u041e\u0447\u0438\u0441\u0442\u0438\u0442\u044c", None))
        self.pushButton_3.setText(QCoreApplication.translate("Widget", u"\u041f\u043e \u0443\u043c\u043e\u043b\u0447\u0430\u043d\u0438\u044e", None))
        self.label_8.setText(QCoreApplication.translate("Widget", u"\u0427\u0438\u0441\u043b\u043e \u0430\u043d\u0442\u0438\u0442\u0435\u043b \u0434\u043b\u044f \u043c\u0443\u0442\u0430\u0446\u0438\u0438:", None))
        self.label_9.setText(QCoreApplication.translate("Widget", u"\u041d\u0430\u0439\u0434\u0435\u043d\u043d\u043e\u0435 \u043b\u0443\u0447\u0448\u0435\u0435 \u0440\u0435\u0448\u0435\u043d\u0438\u0435:", None))
        self.label_10.setText(QCoreApplication.translate("Widget", u"\u0427\u0438\u0441\u043b\u043e \u043a\u043b\u043e\u043d\u043e\u0432 \u043a\u043b\u043e\u043d\u0438\u0440\u0443\u0435\u043c\u043e\u0433\u043e \u0430\u043d\u0442\u0438\u0442\u0435\u043b\u0430:", None))
        self.label_11.setText(QCoreApplication.translate("Widget", u"\u041a\u043e\u044d\u0444\u0444\u0438\u0446\u0438\u0435\u043d\u0442 \u043c\u0443\u0442\u0430\u0446\u0438\u0438:", None))
        self.label_3.setText(QCoreApplication.translate("Widget", u"\u0426\u0435\u043b\u0435\u0432\u0430\u044f \u0444\u0443\u043d\u043a\u0446\u0438\u044f:", None))
        self.comboBox.setItemText(0, QCoreApplication.translate("Widget", u"\u0424\u0443\u043d\u043a\u0446\u0438\u044f \u0441\u0444\u0435\u0440\u044b", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("Widget", u"\u0424\u0443\u043d\u043a\u0446\u0438\u044f Rosenbrock", None))

        self.label_12.setText(QCoreApplication.translate("Widget", u"\u041a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e \u0438\u0442\u0435\u0440\u0430\u0446\u0438\u0439:", None))
        self.label_13.setText(QCoreApplication.translate("Widget", u"\u041f\u043e\u0440\u043e\u0433\u043e\u0432\u044b\u0439 \u043a\u043e\u044d\u0444\u0444\u0438\u0446\u0438\u0435\u043d\u0442 \u0433\u0438\u0431\u0435\u043b\u0438:", None))
        self.label_14.setText(QCoreApplication.translate("Widget", u"\u041a\u043e\u044d\u0444\u0444\u0438\u0446\u0438\u0435\u043d\u0442 \u043a\u043b\u043e\u043d\u0430\u043b\u044c\u043d\u043e\u0433\u043e \u0441\u0436\u0430\u0442\u0438\u044f:", None))
    # retranslateUi
