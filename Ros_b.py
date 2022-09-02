#-*-coding:utf-8-*-
import time

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets

import matplotlib
matplotlib.use("Qt5Agg")  # Declare to use QT5
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt


# Функция Розенброка
def func(x):
    return ((1-x[0])**2) + (100 * ((x[1] - x[0]**2)**2))

# Генетический алгоритм
def genetic_algorithm(popsize, its, bound, mut, crossp):
    # Размер популяции
    # Количество итераций
    # Границы
    # Сила мутации
    # Вероятность мутации
    sc = list()
    # Границы поиска
    bounds = [bound, bound]
    # Измерение
    dimensions = len(bounds)

    # Генерация начальной популяции размера popsize 0 - 1
    pop = np.random.rand(popsize, dimensions)

    # минимальные и максимальные границы
    min_b, max_b = np.asarray(bounds).T

    # Разница между максимальным и минимальным
    diff = np.fabs(min_b - max_b)

    # Получаем популяцию в заданных границах
    pop_denorm = min_b + pop * diff

    # Вычисляется фитнес функция для всех особей популяции
    fitness = np.asarray([func(x) for x in pop_denorm])

    # Получаем индекс минимального потомка
    best_idx = np.argmin(fitness)

    # Получаем потомка с минимальным значением
    best = pop_denorm[best_idx]
    sc.append(pop_denorm.tolist())

    # Движемся пока есть итерации
    for i in range(its):
        # Идем по каждому элементу в популяции
        for j in range(popsize):
            # Получаем индексы потомков всех кроме текущего
            idxs = [idx for idx in range(popsize) if idx != j]

            # Выбираем случайных 3 потомков
            a, b, c = pop[np.random.choice(idxs, 3, replace=False)]

            # Изменение потомков
            # Ограниченичиваем элементы массива от 0 до 1 если мутация вышла за рамки
            mutant = np.clip(a + mut * (b - c), 0, 1)

            # Создаем рандомную мутацию, применив вероятность мутации
            cross_points = np.random.rand(dimensions) < crossp

            # Если мутация не была созданна, то создадим новую, изменив 1 элемент
            if not np.any(cross_points):
                cross_points[np.random.randint(0, dimensions)] = True

            # В гене где нет мутации, заменяем на популяцию TRUE - mutant; False - pop[j](оставляем предыдущую)
            trial = np.where(cross_points, mutant, pop[j])

            # Создание новой мутации
            trial_denorm = min_b + trial * diff

            # Получаем её приспособленность
            f = func(trial_denorm)

            # Если полученная мутация лучше(меньше) текущей особи, то заменяем её в популяции
            if f < fitness[j]:
                fitness[j] = f
                pop_denorm[j] = trial_denorm
                pop[j] = trial

                # Если это лучшее решение в популяции
                if f < fitness[best_idx]:
                    best_idx = j
                    best = trial_denorm
        sc.append(pop_denorm.tolist())
    # Возвращаем лучшие решения на данной итерации
    return best, fitness[best_idx], sc

# Формочка вывода
class Ui_Dialog(object):
    def setupUi(self, Widget):
        Widget.setObjectName("Widget")
        Widget.resize(1314, 692)
        Widget.setAutoFillBackground(False)
        Widget.setStyleSheet("background-color: rgb(64, 65, 66);")
        self.groupBox = QtWidgets.QGroupBox(Widget)
        self.groupBox.setGeometry(QtCore.QRect(20, 40, 851, 631))
        self.groupBox.setObjectName("groupBox")
        self.label = QtWidgets.QLabel(Widget)
        self.label.setGeometry(QtCore.QRect(0, 0, 1301, 41))
        font = QtGui.QFont()
        font.setFamily("Old English Text MT")
        font.setPointSize(16)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setStyleSheet("color: rgb(190, 192, 193);")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.Start = QtWidgets.QPushButton(Widget)
        self.Start.setGeometry(QtCore.QRect(1160, 290, 131, 51))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI Semibold")
        font.setPointSize(12)
        font.setBold(True)
        self.Start.setFont(font)
        self.Start.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.Start.setObjectName("Start")
        self.textEdit = QtWidgets.QTextEdit(Widget)
        self.textEdit.setGeometry(QtCore.QRect(1230, 50, 60, 30))
        self.textEdit.setBaseSize(QtCore.QSize(0, 0))
        self.textEdit.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.textEdit.setObjectName("textEdit")
        self.textEdit_2 = QtWidgets.QTextEdit(Widget)
        self.textEdit_2.setGeometry(QtCore.QRect(1230, 90, 60, 30))
        self.textEdit_2.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.textEdit_2.setObjectName("textEdit_2")
        self.textEdit_3 = QtWidgets.QTextEdit(Widget)
        self.textEdit_3.setGeometry(QtCore.QRect(1230, 130, 60, 30))
        self.textEdit_3.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.textEdit_3.setObjectName("textEdit_3")
        self.label_2 = QtWidgets.QLabel(Widget)
        self.label_2.setGeometry(QtCore.QRect(930, 50, 291, 30))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI Semibold")
        font.setPointSize(16)
        font.setBold(True)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("color: rgb(190, 192, 193);")
        self.label_2.setTextFormat(QtCore.Qt.PlainText)
        self.label_2.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName("label_2")
        self.label_5 = QtWidgets.QLabel(Widget)
        self.label_5.setGeometry(QtCore.QRect(871, 90, 351, 30))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI Semibold")
        font.setPointSize(16)
        font.setBold(True)
        self.label_5.setFont(font)
        self.label_5.setStyleSheet("color: rgb(190, 192, 193);")
        self.label_5.setTextFormat(QtCore.Qt.PlainText)
        self.label_5.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_5.setObjectName("label_5")
        self.textEdit_4 = QtWidgets.QTextEdit(Widget)
        self.textEdit_4.setGeometry(QtCore.QRect(1230, 170, 60, 30))
        self.textEdit_4.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.textEdit_4.setObjectName("textEdit_4")
        self.textEdit_5 = QtWidgets.QTextEdit(Widget)
        self.textEdit_5.setGeometry(QtCore.QRect(1230, 210, 60, 30))
        self.textEdit_5.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.textEdit_5.setObjectName("textEdit_5")
        self.label_6 = QtWidgets.QLabel(Widget)
        self.label_6.setGeometry(QtCore.QRect(1000, 130, 221, 30))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI Semibold")
        font.setPointSize(16)
        font.setBold(True)
        self.label_6.setFont(font)
        self.label_6.setStyleSheet("color: rgb(190, 192, 193);")
        self.label_6.setTextFormat(QtCore.Qt.PlainText)
        self.label_6.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(Widget)
        self.label_7.setGeometry(QtCore.QRect(930, 210, 291, 30))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI Semibold")
        font.setPointSize(16)
        font.setBold(True)
        self.label_7.setFont(font)
        self.label_7.setStyleSheet("color: rgb(190, 192, 193);")
        self.label_7.setTextFormat(QtCore.Qt.PlainText)
        self.label_7.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_7.setObjectName("label_7")
        self.Clear = QtWidgets.QPushButton(Widget)
        self.Clear.setGeometry(QtCore.QRect(1050, 290, 101, 51))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI Semibold")
        font.setPointSize(12)
        font.setBold(True)
        self.Clear.setFont(font)
        self.Clear.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.Clear.setObjectName("Clear")
        self.pushButton_3 = QtWidgets.QPushButton(Widget)
        self.pushButton_3.setGeometry(QtCore.QRect(890, 290, 151, 51))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI Semibold")
        font.setPointSize(12)
        font.setBold(True)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.pushButton_3.setObjectName("pushButton_3")
        self.label_8 = QtWidgets.QLabel(Widget)
        self.label_8.setGeometry(QtCore.QRect(1000, 170, 221, 30))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI Semibold")
        font.setPointSize(16)
        font.setBold(True)
        self.label_8.setFont(font)
        self.label_8.setStyleSheet("color: rgb(190, 192, 193);")
        self.label_8.setTextFormat(QtCore.Qt.PlainText)
        self.label_8.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_8.setObjectName("label_8")
        self.textEdit_6 = QtWidgets.QTextEdit(Widget)
        self.textEdit_6.setGeometry(QtCore.QRect(900, 450, 391, 30))
        self.textEdit_6.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.textEdit_6.setObjectName("textEdit_6")
        self.label_9 = QtWidgets.QLabel(Widget)
        self.label_9.setGeometry(QtCore.QRect(880, 410, 291, 30))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI Semibold")
        font.setPointSize(16)
        font.setBold(True)
        self.label_9.setFont(font)
        self.label_9.setStyleSheet("color: rgb(190, 192, 193);")
        self.label_9.setTextFormat(QtCore.Qt.PlainText)
        self.label_9.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_9.setObjectName("label_9")

        self.retranslateUi(Widget)
        QtCore.QMetaObject.connectSlotsByName(Widget)

    def retranslateUi(self, Widget):
        _translate = QtCore.QCoreApplication.translate
        Widget.setWindowTitle(_translate("Widget", "ГА"))
        self.groupBox.setTitle(_translate("Widget", "GroupBox"))
        self.label.setText(_translate("Widget", "Генетический алгоритм оптимизации функции Розенброка"))
        self.Start.setText(_translate("Widget", "Запустить"))
        self.label_2.setText(_translate("Widget", "Число итераций:"))
        self.label_5.setText(_translate("Widget", "Размер популяции:"))
        self.label_6.setText(_translate("Widget", "Границы:"))
        self.label_7.setText(_translate("Widget", "Вероятность мутации:"))
        self.Clear.setText(_translate("Widget", "Очистить"))
        self.pushButton_3.setText(_translate("Widget", "По умолчанию"))
        self.label_8.setText(_translate("Widget", "Сила мутации:"))
        self.label_9.setText(_translate("Widget", "Найденное решение:"))

# Отрисовка функции
class MyFigure(FigureCanvas):
    def __init__(self,width=5, height=4, dpi=100):
        # Шаг 1. Создание фигуры.
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        # Шаг 2. Активируйте окно рисунка в родительском классе
        super(MyFigure,self).__init__(self.fig) # Это предложение является важным, иначе графика не будет отображаться
        # 3-й шаг: создайте подзаголовок для рисования графики, 111 представляет номер подзаговора, например, подзаголовок Matlab (1,1,1)
        self.axes = self.fig.add_subplot(111, projection='3d')

# Главный класс
class MainDialogImgBW(QDialog,Ui_Dialog):
    def __init__(self):
        super(MainDialogImgBW,self).__init__()
        self.setupUi(self)
        self.setWindowTitle("Генетический алгоритм")
        self.setMinimumSize(0,0)
        self.iter = 0
        self.F = MyFigure(width=3, height=2, dpi=100)

        # Задаем угол обзора
        self.F.axes.view_init(45, 30)

        self.gridlayout = QGridLayout(self.groupBox)
        self.gridlayout.addWidget(self.F)

        self.add_functions()

    def add_functions(self):
        self.pushButton_3.clicked.connect(self.default)
        self.Clear.clicked.connect(self.clear)
        self.Start.clicked.connect(lambda: self.draw(
            self.textEdit.toPlainText(),
            self.textEdit_2.toPlainText(),
            self.textEdit_3.toPlainText(),
            self.textEdit_4.toPlainText(),
            self.textEdit_5.toPlainText()))

    def clear(self):
        self.textEdit.setText("")
        self.textEdit_2.setText("")
        self.textEdit_3.setText("")
        self.textEdit_4.setText("")
        self.textEdit_5.setText("")

    def default(self):
        self.textEdit.setText("10")
        self.textEdit_2.setText("20")
        self.textEdit_3.setText("-10, 10")
        self.textEdit_4.setText("0.8")
        self.textEdit_5.setText("0.7")

    def draw(self,iterat, popsize, bound, mut, cross):
        self.F.axes.clear()

        self.iterat = int(iterat)
        self.popsize = int(popsize)
        self.bound = list(map(int,bound.split(",")))
        self.mut = float(mut)
        self.cross = float(cross)


        # Создаем данные для графика
        X = np.linspace(self.bound[0], self.bound[1], 100)
        Y = np.linspace(self.bound[0], self.bound[1], 100)
        self.X, self.Y = np.meshgrid(X, Y)
        self.Z = func(np.array([self.X, self.Y]))

        # Рисуем поверхность
        self.best, self.fit, self.sc = genetic_algorithm(self.popsize, self.iterat, self.bound, self.mut, self.cross)
        # Выводим лучшее решение
        self.textEdit_6.setText(str(self.best) + "   " + str(self.fit))

        # Отрисовка графиков
        self.tempIter = 0
        self.step = self.iterat / 10
        self.timer = QtCore.QTimer()
        self.timer.setInterval(500)
        self.timer.timeout.connect(self.update)
        self.timer.start()


    def update(self):

        # Очистка графика
        self.F.axes.clear()
        self.F.axes.plot_surface(self.X, self.Y, self.Z, alpha=0.6)

        # Установка заголовка
        title = 'Итерация : ' + str((self.tempIter + 1) * self.step)
        self.F.axes.set_title(title)

        x, y = np.split(self.sc[int(self.tempIter * self.step)], [1], axis=1)

        if self.tempIter == 9:
            self.F.axes.scatter(self.best[0], self.best[1], self.fit, s=120, color="#FF0000", marker=".")
            self.timer.stop()
        else:
            self.F.axes.scatter(x, y, func([x, y]), s=50, color="#000000", marker=".")

        self.tempIter += 1

        self.F.draw()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = MainDialogImgBW()
    main.show()
    #app.installEventFilter(main)
    sys.exit(app.exec_())