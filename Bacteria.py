import random
import math
import time
import sys
import numpy
from matplotlib import cm
from PySide6 import QtCore
from PySide6.QtWidgets import QApplication, QWidget, QGridLayout
from forms.Bacteria import Ui_Widget
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

# Отрисовка функции
class MyFigure(FigureCanvas):
    def __init__(self, width=5, height=4, dpi=100):
        # Шаг 1. Создание фигуры.
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        # Шаг 2. Активируйте окно рисунка в родительском классе
        super(MyFigure, self).__init__(self.fig)  # Это предложение является важным, иначе графика не будет отображаться
        # 3-й шаг: создайте подзаголовок для рисования графики, 111 представляет номер подзаговора, например, подзаголовок Matlab (1,1,1)
        self.axes = self.fig.add_subplot(111, projection='3d')

# Функция сферы
def sphere(x, y):
    return (x ** 2 + y ** 2)

# Функция Розенброка (целевая)
def rosenbrock(x, y):
    return (1 - x) ** 2 + 100 * (y - x ** 2) ** 2

# Длина вектора
def mod(x):
    return math.sqrt(x[0] ** 2 + x[1] ** 2)

# Генерация популяции
def generate(border, size_population, func):

    population = [] # Популяция

    # Идем по размеру популяции
    for i in range(size_population):
        bacteria = [[random.uniform(border[0], border[1]), random.uniform(border[0], border[1])]] # Координаты в данных границах
        bacteria.append([random.uniform(-1, 1), random.uniform(-1, 1)]) # Скорость
        bacteria.append(func(bacteria[0][0], bacteria[0][1])) # Целевая функция
        population.append(bacteria)

    return population

# Xемотаксис бактерии
def chemotaxis(bacteria, lmbd, func):
    # Выбираем из двух
    operation = random.randint(0, 1)

    if operation == 0:
        # Продолжаем движение
        bacteria[0][0] = bacteria[0][0] + lmbd * bacteria[1][0] / (mod(bacteria[1])) # Новая координата x
        bacteria[0][0] = bacteria[0][1] + lmbd * bacteria[1][1] / (mod(bacteria[1])) # Новая координата y
    else:
        # Делаем кувырок
        v = [random.uniform(-1, 1), random.uniform(-1, 1)] # Новый вектор скорости
        bacteria[0][0] = bacteria[0][0] + lmbd * v[0] / mod(v) # Новая координата x
        bacteria[0][1] = bacteria[0][1] + lmbd * v[1] / mod(v) # Новая координата y
        bacteria[1] = v
    bacteria[2] += func(bacteria[0][0], bacteria[0][1]) # Добавляем к здоровью бактерии
    return bacteria

# Репродукция
def reproduction(bacteries):
    count = len(bacteries) # Размер популяции

    # Сортировка по фитнесс функции
    bacteries.sort(key=lambda a: a[2], reverse=False)

    bacteries = bacteries[:int(count / 2)]
    bacteries += bacteries # Дублируем
    return bacteries

# ликвидация
def elimination(bacteries, n, border, func):
    # Идем по параметру количество особей, уничтожаемых в ходе ликвидации
    for i in range(n):
        # Выбираем случайную бактерию
        x = random.randint(0, (len(bacteries) - 1))
        # Ликвидируем её
        del bacteries[x]
        # Создаем новую
        new_bacteria = generate(border, 1, func)
        # Добавляем
        bacteries += new_bacteria
    return bacteries

# Получаем лучшее значение в популяции
def get_best_solution(bacteries):
    best_solution = [bacteries[0][0],bacteries[0][2]] # Принимаем за лучшее первую бактерию

    for bac in bacteries:
        if bac[2] < best_solution[1]:
            best_solution = [bac[0], bac[2]]
    return best_solution

class Widget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Widget()
        self.ui.setupUi(self)
        self.F = MyFigure(width=3, height=2, dpi=100)

        self.gridlayout = QGridLayout(self.ui.groupBox)  # (self.ui.groupBox)
        self.gridlayout.addWidget(self.F)

        self.timer = QtCore.QTimer() # Таймер для функций

        self.add_functions() # Вещаем слушателей

    def add_functions(self):
        self.ui.pushButton_3.clicked.connect(self.default)

        self.ui.Clear.clicked.connect(self.clear)

        self.ui.Start.clicked.connect(lambda: self.start(
            self.ui.comboBox.currentText(),
            list(map(int, self.ui.textEdit.toPlainText().split(","))),
            int(self.ui.textEdit_2.toPlainText()),
            int(self.ui.textEdit_3.toPlainText()),
            float(self.ui.textEdit_4.toPlainText()),
            int(self.ui.textEdit_5.toPlainText()),
            float(self.ui.textEdit_7.toPlainText())))

    def clear(self):
        self.ui.comboBox.setCurrentIndex(0)
        self.ui.textEdit.setText("")
        self.ui.textEdit_2.setText("")
        self.ui.textEdit_3.setText("")
        self.ui.textEdit_4.setText("")
        self.ui.textEdit_5.setText("")
        self.ui.textEdit_6.setText("")
        self.ui.textEdit_7.setText("")


    def default(self):
        self.ui.textEdit.setText("-10,10")
        self.ui.textEdit_2.setText("100")
        self.ui.textEdit_3.setText("500")
        self.ui.textEdit_4.setText("0.1")
        self.ui.textEdit_5.setText("5")
        self.ui.textEdit_6.setText("")
        self.ui.textEdit_7.setText("0.1")

    '''
    Параметры:
    1 - Минимальные и максимальное значения координат
    2 - Размер популяции
    3 - количество итераций изменения популяции (суммарное число шагов)
    4 - размер шага (скорость)
    5 - количесво особей, уничтожаемых в ходе ликвидации n
    6 - вероятность ликвидации  ep
    '''

    # Бактериальный алгоритм
    def start(self, func, border, size_population, iterations, lmbd, n, ep):
        if func == "Функция сферы":
            self.func = sphere
        elif func == "Функция Rosenbrock":
            self.func = rosenbrock

        self.border = border
        self.size_population = size_population
        self.lmbd = lmbd
        self.n = n
        self.ep = ep

        # Генерируется популяция указанной численности
        # Каждая бактрерия представляет собой вектор из 3 объектов
        self.population = generate(border, size_population, self.func)

        # Запоминаем лучшее решение
        self.current_best = get_best_solution(self.population)

        # Лучшее глобальное решение
        self.global_best = self.current_best

        # Лучшее решение на данной итерации
        self.bst = self.current_best

        # Создаем данные для графика
        self.X = numpy.linspace(self.border[0], self.border[1], 100)
        self.Y = numpy.linspace(self.border[0], self.border[1], 100)
        self.X, self.Y = numpy.meshgrid(self.X, self.Y)

        self.Z = self.func(self.X, self.Y)
        self.F.axes.plot_surface(self.X, self.Y, self.Z, alpha=0.6, cmap=cm.coolwarm)

        # Отрисовка
        for bac in self.population:
            self.F.axes.scatter(bac[0][0], bac[0][1], bac[2], c='black', s=5, marker='o')

        title = 'Итерация : 0'
        self.F.axes.set_title(title)

        self.F.draw()
        # Отрисовка графиков
        self.tempIter = 0
        self.iterations = iterations
        self.timer.timeout.connect(self.update)
        self.timer.start()


    # Функция обновления
    def update(self):

        # Если есть лучшее решение - делаем хемотаксис
        if self.bst[1] < self.current_best[1]:
            # Лучшее решение
            self.current_best = self.bst

            # Делаем хемотаксис бактерии
            for i in range(len(self.population)):
                #
                self.population[i] = chemotaxis(self.population[i], self.lmbd, self.func)

            # Получаем лучшее решение
            self.bst = get_best_solution(self.population)
        # Иначе репликация или ликвидация
        else:
            # Выбираем случайное число
            i = random.uniform(0, 1)

            # Если, это число больше вероятности ликвидации
            if i > self.ep:
                # Делаем репродукцию
                self.population = reproduction(self.population)
            else:
                # Иначе делаем ликвидацию
                self.population = elimination(self.population, self.n, self.border, self.func)

            self.bst = get_best_solution(self.population)
            self.current_best = self.bst

        if(self.tempIter % 100 == 0):
            self.F.axes.clear()

            title = 'Итерация : ' + str((self.tempIter + 1))
            self.F.axes.set_title(title)

            # Отрисовка
            for bac in self.population:
                self.F.axes.scatter(bac[0][0], bac[0][1], bac[2], c='r', s=5, marker='o')

            # Вывод лучшего решения
            if self.global_best[1] > self.current_best[1]:
                self.global_best = self.current_best
                self.ui.textEdit_6.setText(
                    str([round(self.global_best[0][0], 3), round(self.global_best[0][1], 3)]) + "  " + str(
                        round(self.global_best[1], 3)))

            # Рисуем график
            self.F.axes.plot_surface(self.X, self.Y, self.Z, alpha=0.6, cmap=cm.coolwarm)

            self.F.draw()  # Отрисовка графика


        self.tempIter += 1 # Обновление счетчика

        if self.tempIter >= self.iterations:
            self.timer.stop()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Widget()
    widget.show()
    sys.exit(app.exec())