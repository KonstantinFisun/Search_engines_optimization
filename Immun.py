import random
import math
import time
import sys
import pylab
from PySide6 import QtCore
from PySide6.QtWidgets import QApplication, QWidget, QGridLayout
from forms.Immun import Ui_Widget
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import random

# Функция сферы
def sphere(x, y):
    return (x ** 2 + y ** 2)

# Функция Розенброка (целевая)
def rosenbrock(x, y):
    return (1 - x) ** 2 + 100 * (y - x ** 2) ** 2

# расстояние между точками
def affin(x, y):
    return (x[0] - y[0]) ** 2 + (x[1] - y[1]) ** 2


# генерация начальной популяции
def generate_population(border, count):
    population = []
    for i in range(count):
        population.append([random.uniform(border[0], border[1]), random.uniform(border[0], border[1])])
    return population


# сжатие популяции
# value - коэффициент клонального сжатия
def compress(population, value,func):
    flag = True
    while flag:
        flag = False
        # для каждого элемента
        for i in range(len(population)):
            for j in range(i + 1, len(population)):
                if population[i] != [] and population[j] != []:
                    if affin(population[i], population[j]) < value:
                        flag = True
                        if func(population[i][0], population[i][1]) < func(population[j][0],
                                                                               population[j][1]):
                            population[j] = []
                        else:
                            population[i] = []
    # Убираем удаленных антитела
    population = list(filter(lambda a: a != [], population))
    return population


# клонирование и мутация антител !!!!!!!!!
def clone_and_mutate(antibodies, number_clones_cloned_antibody, mutation_coefficient,
                     count_clones_left, gen, threshold_coefficient_death, clonal_compression_ratio,func):
    clones = []  # Клоны
    # Идем по каждому антигену
    for body in antibodies:
        # Идем по числу оставляемых клонов
        for c in range(number_clones_cloned_antibody):
            # Добавляем клона
            # к значению каждой координаты прибавляется случайное число в интервале
            # [-0.5*mutation_coefficient, 0.5*mutation_coefficient]
            clones.append([body[0] + mutation_coefficient * random.uniform(-0.5, 0.5),
                           body[1] + mutation_coefficient * random.uniform(-0.5, 0.5)])

    # Сортировка по убыванию аффинности полученных клонов
    clones.sort(key=lambda a: affin(a, gen), reverse=False)

    # Оставляем лучших до числа клонов клонируемого антитела(входной параметр)
    Sm = clones[:count_clones_left]

    # Идем по оставшимся клонам
    for i in range(count_clones_left):
        # Из полученной популяции удаляются все клоны, евклидово расстояние от которых до антигена меньше параметра смерти
        if affin(Sm[i], gen) < threshold_coefficient_death:
            Sm = Sm[:i]
            break

    # сжатие популяции
    Sm = compress(Sm, clonal_compression_ratio,func)
    return Sm


# получаем лучшие антитела
def get_best_antibodies(antibodies, antigen, count_antitel_for_mutation):
    # Сортировка по убыванию аффинности
    antibodies.sort(key=lambda x: affin(x, antigen), reverse=False)

    # Выбираем лучшие антитела для мутации
    return antibodies[:count_antitel_for_mutation]


# создание популяции клеток памяти
def create_Sm(antibodies, antigens, count_antitel_for_mutation,
              number_clones_cloned_antibody, mutation_coefficient, count_clones_left,
              threshold_coefficient_death, clonal_compression_ratio, func):

    # Идем по всем антигенам
    for gen in antigens:
        # Получаем лучшие антитела для мутации
        antibodies = get_best_antibodies(antibodies, gen, count_antitel_for_mutation)

        # клонирование и мутация полученных антител
        Sm = clone_and_mutate(antibodies, number_clones_cloned_antibody, mutation_coefficient,
                              count_clones_left, gen, threshold_coefficient_death, clonal_compression_ratio, func)

        antibodies += Sm
        antibodies = compress(antibodies, clonal_compression_ratio, func)

    return antibodies


'''
Параметры:
1. Минимальные и максимальное значения координат
2. Размер начальной популяции антител
3. Размер начальной популяции антигенов
4. Число антител для мутации
5. Число оставляемых клонов
6. Число клонов клонируемого антитела
7. Коэффициент мутации
8. количество итераций
9. Пороговый коэффициент гибели
10. Коэффициент клонального сжатия
'''


# Отрисовка функции
class MyFigure(FigureCanvas):
    def __init__(self, width=5, height=4, dpi=100):
        # Шаг 1. Создание фигуры.
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        # Шаг 2. Активируйте окно рисунка в родительском классе
        super(MyFigure, self).__init__(self.fig)  # Это предложение является важным, иначе графика не будет отображаться
        # 3-й шаг: создайте подзаголовок для рисования графики, 111 представляет номер подзаговора, например, подзаголовок Matlab (1,1,1)
        self.axes = self.fig.add_subplot(111)

# Форма
class Widget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Widget()
        self.ui.setupUi(self)
        self.F = MyFigure(width=3, height=2, dpi=100)

        self.gridlayout = QGridLayout(self.ui.groupBox)  # (self.ui.groupBox)
        self.gridlayout.addWidget(self.F)

        self.timer = QtCore.QTimer() # Таймер для функций

        self.add_functions()

    def add_functions(self):
        self.ui.pushButton_3.clicked.connect(self.default)

        self.ui.Clear.clicked.connect(self.clear)

        self.ui.Start.clicked.connect(lambda: self.start(
            self.ui.comboBox.currentText(),
            list(map(int, self.ui.textEdit.toPlainText().split(","))),
            int(self.ui.textEdit_2.toPlainText()),
            int(self.ui.textEdit_3.toPlainText()),
            int(self.ui.textEdit_4.toPlainText()),
            int(self.ui.textEdit_5.toPlainText()),
            int(self.ui.textEdit_7.toPlainText()),
            float(self.ui.textEdit_8.toPlainText()),
            int(self.ui.textEdit_9.toPlainText()),
            float(self.ui.textEdit_10.toPlainText()),
            float(self.ui.textEdit_11.toPlainText())))

    def clear(self):
        self.ui.comboBox.setCurrentIndex(0)
        self.ui.textEdit.setText("")
        self.ui.textEdit_2.setText("")
        self.ui.textEdit_3.setText("")
        self.ui.textEdit_4.setText("")
        self.ui.textEdit_5.setText("")
        self.ui.textEdit_6.setText("")
        self.ui.textEdit_7.setText("")
        self.ui.textEdit_8.setText("")
        self.ui.textEdit_9.setText("")
        self.ui.textEdit_10.setText("")
        self.ui.textEdit_11.setText("")

    def default(self):
        self.ui.textEdit.setText("-6,6")
        self.ui.textEdit_2.setText("100")
        self.ui.textEdit_3.setText("50")
        self.ui.textEdit_4.setText("10")
        self.ui.textEdit_5.setText("5")
        self.ui.textEdit_6.setText("")
        self.ui.textEdit_7.setText("7")
        self.ui.textEdit_8.setText("0.3")
        self.ui.textEdit_9.setText("100")
        self.ui.textEdit_10.setText("0.4")
        self.ui.textEdit_11.setText("0.4")

    def start(self, func, border, size_antibodies, size_antigens,
                        count_antitel_for_mutation, count_clones_left,
                        number_clones_cloned_antibody, mutation_coefficient, iterations,
                        threshold_coefficient_death,
                        clonal_compression_ratio):
        self.ui.textEdit_6.setText("")  # Очистка решений

        if func == "Функция сферы":
            self.func = sphere
        elif func == "Функция Rosenbrock":
            self.func = rosenbrock

        self.border = border
        self.count_antitel_for_mutation = count_antitel_for_mutation
        self.count_clones_left = count_clones_left
        self.number_clones_cloned_antibody = number_clones_cloned_antibody
        self.mutation_coefficient = mutation_coefficient
        self.threshold_coefficient_death = threshold_coefficient_death
        self.clonal_compression_ratio = clonal_compression_ratio

        # Генерация начальных популяций антител и антигенов
        self.antibodies = generate_population(border, size_antibodies)  # Генерация антител
        self.antigens = generate_population(border, size_antigens)  # # Генерация антигенов

        # Отрисовка графиков
        self.tempIter = 0
        self.iterations = iterations
        self.timer.timeout.connect(self.update)
        self.timer.start()


    # Функция обновления
    def update(self):
        self.antibodies = create_Sm(self.antibodies, self.antigens, self.count_antitel_for_mutation, self.number_clones_cloned_antibody,
                               self.mutation_coefficient, self.count_clones_left, self.threshold_coefficient_death,
                               self.clonal_compression_ratio, self.func)

        x = []
        y = []
        for anti in self.antibodies:
            x.append(anti[0])
            y.append(anti[1])

        self.F.axes.clear()
        title = 'Итерация : ' + str((self.tempIter + 1))
        self.F.axes.set_title(title)
        self.F.axes.scatter(x, y, c='k', s=5, marker='o')

        mn = self.func(self.antibodies[0][0], self.antibodies[0][1])

        index = 0
        for i in range(1, len(self.antibodies)):
            if self.func(self.antibodies[i][0], self.antibodies[i][1]) < mn:
                index = i
                mn = self.func(self.antibodies[i][0], self.antibodies[i][1])

        self.ui.textEdit_6.setText(
            str([round(self.antibodies[index][0],3),round(self.antibodies[index][1],3)]) + "  " + str(round(mn, 3)))

        self.tempIter += 1 # Обновление счетчика

        if (self.tempIter >= self.iterations):
            self.timer.stop()


        self.F.draw() # Отрисовка графика

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Widget()
    widget.show()
    sys.exit(app.exec())