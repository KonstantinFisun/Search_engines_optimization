import math
import numdifftools as nd
import numpy as np
import sys
import matplotlib
matplotlib.use("Qt5Agg")  # Объявить об использовании QT5
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from PyQt5 import QtCore, QtGui, QtWidgets

# Создание класса рисования графики matplotlib
class MyFigure(FigureCanvas):
    def __init__(self,width=5, height=4, dpi=100):
        #Step 1: Create a Create Figure
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        #Step 2: Activate the Figure window in the parent class
        super(MyFigure,self).__init__(self.fig) #This sentence is essential, otherwise graphics cannot be displayed
        #Step 3: Create a subplot for drawing graphics, 111 indicates the subplot number, such as matplot(1,1,1)
        self.axes = self.fig.add_subplot(111)


class Ui_Widget(object):
    def setupUi(self, Widget):
        Widget.setObjectName("Widget")
        Widget.resize(1094, 586)
        Widget.setAutoFillBackground(False)
        Widget.setStyleSheet("background-color: rgb(64, 65, 66);")
        self.groupBox = QtWidgets.QGroupBox(Widget)
        self.groupBox.setGeometry(QtCore.QRect(20, 40, 651, 531))
        self.groupBox.setObjectName("groupBox")
        self.label = QtWidgets.QLabel(Widget)
        self.label.setGeometry(QtCore.QRect(140, 0, 801, 41))
        font = QtGui.QFont()
        font.setFamily("Old English Text MT")
        font.setPointSize(16)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setStyleSheet("color: rgb(190, 192, 193);")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(Widget)
        self.pushButton.setGeometry(QtCore.QRect(950, 290, 131, 51))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI Semibold")
        font.setPointSize(12)
        font.setBold(True)
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.pushButton.setObjectName("pushButton")
        self.textEdit = QtWidgets.QTextEdit(Widget)
        self.textEdit.setGeometry(QtCore.QRect(1020, 50, 60, 30))
        self.textEdit.setBaseSize(QtCore.QSize(0, 0))
        self.textEdit.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.textEdit.setObjectName("textEdit")
        self.textEdit_2 = QtWidgets.QTextEdit(Widget)
        self.textEdit_2.setGeometry(QtCore.QRect(1020, 90, 60, 30))
        self.textEdit_2.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.textEdit_2.setObjectName("textEdit_2")
        self.textEdit_3 = QtWidgets.QTextEdit(Widget)
        self.textEdit_3.setGeometry(QtCore.QRect(1020, 130, 60, 30))
        self.textEdit_3.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.textEdit_3.setObjectName("textEdit_3")
        self.label_2 = QtWidgets.QLabel(Widget)
        self.label_2.setGeometry(QtCore.QRect(720, 50, 291, 30))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI Semibold")
        font.setPointSize(16)
        font.setBold(True)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("color: rgb(190, 192, 193);")
        self.label_2.setTextFormat(QtCore.Qt.PlainText)
        self.label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName("label_2")
        self.label_5 = QtWidgets.QLabel(Widget)
        self.label_5.setGeometry(QtCore.QRect(721, 90, 291, 30))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI Semibold")
        font.setPointSize(16)
        font.setBold(True)
        self.label_5.setFont(font)
        self.label_5.setStyleSheet("color: rgb(190, 192, 193);")
        self.label_5.setTextFormat(QtCore.Qt.PlainText)
        self.label_5.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_5.setObjectName("label_5")
        self.label_3 = QtWidgets.QLabel(Widget)
        self.label_3.setGeometry(QtCore.QRect(721, 130, 291, 30))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI Semibold")
        font.setPointSize(16)
        font.setBold(True)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("color: rgb(190, 192, 193);")
        self.label_3.setTextFormat(QtCore.Qt.PlainText)
        self.label_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(Widget)
        self.label_4.setGeometry(QtCore.QRect(721, 170, 291, 30))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI Semibold")
        font.setPointSize(16)
        font.setBold(True)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color: rgb(190, 192, 193);")
        self.label_4.setTextFormat(QtCore.Qt.PlainText)
        self.label_4.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName("label_4")
        self.textEdit_4 = QtWidgets.QTextEdit(Widget)
        self.textEdit_4.setGeometry(QtCore.QRect(1020, 170, 60, 30))
        self.textEdit_4.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.textEdit_4.setObjectName("textEdit_4")
        self.textEdit_5 = QtWidgets.QTextEdit(Widget)
        self.textEdit_5.setGeometry(QtCore.QRect(1020, 210, 60, 30))
        self.textEdit_5.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.textEdit_5.setObjectName("textEdit_5")
        self.label_6 = QtWidgets.QLabel(Widget)
        self.label_6.setGeometry(QtCore.QRect(721, 210, 291, 30))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI Semibold")
        font.setPointSize(16)
        font.setBold(True)
        self.label_6.setFont(font)
        self.label_6.setStyleSheet("color: rgb(190, 192, 193);")
        self.label_6.setTextFormat(QtCore.Qt.PlainText)
        self.label_6.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(Widget)
        self.label_7.setGeometry(QtCore.QRect(721, 250, 291, 30))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI Semibold")
        font.setPointSize(16)
        font.setBold(True)
        self.label_7.setFont(font)
        self.label_7.setStyleSheet("color: rgb(190, 192, 193);")
        self.label_7.setTextFormat(QtCore.Qt.PlainText)
        self.label_7.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_7.setObjectName("label_7")
        self.textEdit_6 = QtWidgets.QTextEdit(Widget)
        self.textEdit_6.setGeometry(QtCore.QRect(1020, 250, 60, 30))
        self.textEdit_6.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.textEdit_6.setObjectName("textEdit_6")
        self.pushButton_2 = QtWidgets.QPushButton(Widget)
        self.pushButton_2.setGeometry(QtCore.QRect(840, 290, 101, 51))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI Semibold")
        font.setPointSize(12)
        font.setBold(True)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(Widget)
        self.pushButton_3.setGeometry(QtCore.QRect(680, 290, 151, 51))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI Semibold")
        font.setPointSize(12)
        font.setBold(True)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.pushButton_3.setObjectName("pushButton_3")

        self.retranslateUi(Widget)
        QtCore.QMetaObject.connectSlotsByName(Widget)
        # Пятый шаг: определение экземпляра класса MyFigure
        # self.F = MyFigure(width=3, height=2, dpi=100)
        # self.F.plotsin()
        # self.plotcos()
        # Шаг 6. Создайте макет в groupBox графического интерфейса пользователя, который используется для добавления экземпляра класса MyFigure (то есть фигуры) в другие части.
        #self.gridlayout = QtWidgets.QGridLayout(self.groupBox)  # Наследовать контейнер groupBox

        self.add_functions()

    def retranslateUi(self, Widget):
        _translate = QtCore.QCoreApplication.translate
        Widget.setWindowTitle(_translate("Widget", "Widget"))
        self.groupBox.setTitle(_translate("Widget", "GroupBox"))
        self.label.setText(_translate("Widget", "Метод градиентного спуска с постоянным шагом"))
        self.pushButton.setText(_translate("Widget", "Запустить"))
        self.label_2.setText(_translate("Widget", "Число итераций:"))
        self.label_5.setText(_translate("Widget", "Epsilon:"))
        self.label_3.setText(_translate("Widget", "Epsilon_1:"))
        self.label_4.setText(_translate("Widget", "Epsilon_2:"))
        self.label_6.setText(_translate("Widget", "Начальная точка:"))
        self.label_7.setText(_translate("Widget", "Шаг:"))
        self.pushButton_2.setText(_translate("Widget", "Очистить"))
        self.pushButton_3.setText(_translate("Widget", "По умолчанию"))



    def add_functions(self):
        self.pushButton_3.clicked.connect(self.default)

        self.pushButton_2.clicked.connect(self.clear)

        self.pushButton.clicked.connect(lambda: self.gradient(
            self.textEdit.toPlainText(),
            self.textEdit_2.toPlainText(),
            self.textEdit_3.toPlainText(),
            self.textEdit_4.toPlainText(),
            self.textEdit_5.toPlainText(),
            self.textEdit_6.toPlainText()))

    def clear(self):
        self.textEdit.setText("")
        self.textEdit_2.setText("")
        self.textEdit_3.setText("")
        self.textEdit_4.setText("")
        self.textEdit_5.setText("")
        self.textEdit_6.setText("")

    def default(self):
        self.textEdit.setText("10")
        self.textEdit_2.setText("0.1")
        self.textEdit_3.setText("0.1")
        self.textEdit_4.setText("0.15")
        self.textEdit_5.setText("0.5 , 1")
        self.textEdit_6.setText("0.24")

    def gradient(self,M,eps,eps1,eps2,x,step):
        self.F.axes.clear()
        # Шаг 1 Задать х , 0 < ε < 1, ε 1 > 0, ε 2 > 0,  М – предельное число итераций
        self.eps_first = float(eps1)
        self.eps_second = float(eps2)
        self.M = int(M)
        self.start_point = list(map(float,x.split(",")))


        # Шаг 2 Положить k = 0
        k = 0
        arr = [[], [], []]
        self.tk = float(step)
        print(3)
        res = self.gradient_method(self.start_point, self.eps_first, self.eps_second, self.M, k, self.tk, arr)

        print("Результат : " + str(res))

        x_p = np.linspace(-2, 2, 100)
        y_p = np.linspace(-2, 2, 100)

        # x_plot, y_plot = np.meshgrid(x_p, y_p)
        # fun_plot = self.func([x_plot, y_plot])
        # self.gridlayout.addWidget(self.F)
        # print(1)
        # self.F.axes.scatter(arr[0], arr[1], arr[2], color='black', linewidths=2)
        # self.F.axes.scatter(res[0], res[1], self.func([res[0], res[1]]), color='red', linewidths=4)
        # self.F.axes.plot_surface(x_plot, y_plot, fun_plot, rstride=5, cstride=5, alpha=0.7)

        self.F = MyFigure(width=3, height=2, dpi=100)
        self.plotcos()
        self.gridlayout = QtWidgets.QGridLayout(self.groupBox)  # Inherit container groupBox
        self.gridlayout.addWidget(self.F, 0, 1)

        # self.gridlayout.addWidget(self.F, 0, 1)

    def plotcos(self):
        t = np.arange(0.0, 5.0, 0.01)
        s = np.cos(2 * np.pi * t)
        self.F.axes.plot(t, s)
        self.F.fig.suptitle("cos")

    # Функция f(x)
    def func(self,x):
        return 2 * x[0] ** 2 + x[0] * x[1] + x[1] ** 2


    # Функция ||x||
    def norma(self,x):
        res = 0
        length = len(x)
        for i in range(length):
            res += abs(x[i]) ** length
        return math.sqrt(res)

    def gradient_method(self, x, eps_first, eps_second, M, k, tk, arr):
        while (True):
            arr[0].append(x[0])
            arr[1].append(x[1])
            arr[2].append(self.func([x[0],x[1]]))

            # Вычисляем ▼f(x^k)
            grad = nd.Gradient(self.func)(x)

            # Шаг 4. Проверить выполнение критерия окончания  ||▼f(x^k)||<e_1
            if self.norma(grad) < eps_first:
                x_res = x  # если критерий выполнен, то x0 = xk;
                return x_res
            else:
                # Шаг 5. Проверить выполнение неравенства k ≥ M:
                if k >= M:
                    x_0 = x  # если неравенство выполнено, то x0 = xk;
                    return x_0
                else:
                    # Шаг 6. Задать величину шага tk
                    # Шаг 7. Вычислить  xk+1 = xk - tk ▼f(xk)

                    x_next = x - (tk * grad)
                    # Шаг 8. Проверить выполнение условия
                    # f(xk+1) - f(xk) < 0    (или |f(xk+1) - f(xk) |<  ε || f(xk)||2);
                    if ((self.func(x_next) - self.func(x)) < 0 or math.fabs(self.func(x_next)- self.func(x)) < eps*(self.norma(grad)**2)):
                        # Шаг 9. Проверить выполнение условий
                        # ||xk+1 - xk|| < ε 2,  ||f(xk+1) - f(xk)|| < ε 2:
                        if (self.norma(x_next - x) < eps_second and math.fabs(self.func(x_next) - self.func(x)) < eps_second):
                            x_res = x_next
                            return x_res
                        else:
                            # если хотя бы одно из условий не выполнено, положить k = k +1 и перейти к шагу 3.
                            k += 1
                            x = list(x_next)
                            print(x)
                            continue
                    else:
                        # если условие не выполнено, положить tk = tk/2   и перейти к шагу 7.
                        tk /= 2
                        continue

def main():
    app = QtWidgets.QApplication(sys.argv)
    Widget = QtWidgets.QWidget()
    ui = Ui_Widget()
    ui.setupUi(Widget)
    Widget.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()