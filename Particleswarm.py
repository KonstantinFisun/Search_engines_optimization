import numpy
import sys
from matplotlib import cm

from PySide6 import QtCore
from PySide6.QtWidgets import QApplication, QWidget, QGridLayout
from forms.Particleswarm import Ui_Widget
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
            int(self.ui.textEdit.toPlainText()),
            int(self.ui.textEdit_2.toPlainText()),
            int(self.ui.textEdit_3.toPlainText()),
            list(map(int, self.ui.textEdit_4.toPlainText().split(","))),
            float(self.ui.textEdit_5.toPlainText()),
            float(self.ui.textEdit_7.toPlainText()),
            float(self.ui.textEdit_8.toPlainText())))

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

    def default(self):
        self.ui.comboBox.setCurrentIndex(0)
        self.ui.textEdit.setText("30")
        self.ui.textEdit_2.setText("20")
        self.ui.textEdit_3.setText("2")
        self.ui.textEdit_4.setText("-10, 10")
        self.ui.textEdit_5.setText("0.1")
        self.ui.textEdit_6.setText("")
        self.ui.textEdit_7.setText("1.0")
        self.ui.textEdit_8.setText("5.0")

    def start(self, func, iterations, swarmsize, dimension, bound, k, p, g):
        self.ui.textEdit_6.setText("") # Очистка решений
        self.dimension = dimension # Делаем размерность полем класса

        self.iter = iterations # Количество итераций
        # Создаем данные для графика
        self.X = numpy.linspace(bound[0], bound[1], 100)
        self.Y = numpy.linspace(bound[0], bound[1], 100)
        self.X, self.Y = numpy.meshgrid(self.X, self.Y)

        global swarm
        minvalues = numpy.array(
            [bound[0]] * dimension)  # список, задающий минимальные значения для каждой координаты частицы
        maxvalues = numpy.array(
            [bound[1]] * dimension)  # список, задающий максимальные значения для каждой координаты частицы

        currentVelocityRatio = k  # общий масштабирующий коэффициент для скорости
        localVelocityRatio = p  # коэффициент, задающий влияние лучшей точки, найденной каждой частицей, на будущую скорость
        globalVelocityRatio = g  # коэффициент, задающий влияние лучшей точки, найденной всеми частицами, на будущую скорость

        self.F.axes.clear()  # Очистка графика

        # Создание класса роя
        if func == "Функция сферы":
            self.swarm = Swarm(swarmsize, dimension, minvalues, maxvalues, currentVelocityRatio, localVelocityRatio,
                               globalVelocityRatio, sphereFunction)
            self.Z = sphereFunction(numpy.array([self.X, self.Y]), self.dimension)
            for i in range(len(self.swarm.swarm)):
                self.F.axes.scatter(self.swarm.swarm[i].currentPosition[0], self.swarm.swarm[i].currentPosition[1],
                                    sphereFunction(self.swarm.swarm[i].currentPosition),
                                    s=50, color="#000000", marker=".")
            self.func = sphereFunction # Определяем функцию

        elif func == "функция Растригина":
            self.swarm = Swarm(swarmsize, dimension, minvalues, maxvalues, currentVelocityRatio, localVelocityRatio,
                          globalVelocityRatio, rastriginFunction)
            self.Z = rastriginFunction(numpy.array([self.X, self.Y]), self.dimension)


            for i in range(len(self.swarm.swarm)):
                self.F.axes.scatter(self.swarm.swarm[i].currentPosition[0], self.swarm.swarm[i].currentPosition[1],
                                    rastriginFunction(self.swarm.swarm[i].currentPosition, self.dimension),
                                    s=50, color="#000000", marker=".")

            self.func = rastriginFunction # Определяем функцию
        elif func == "Функция Швефеля":
            self.swarm = Swarm(swarmsize, dimension, minvalues, maxvalues, currentVelocityRatio, localVelocityRatio,
                          globalVelocityRatio, schwefelFunction)
            self.Z = schwefelFunction(numpy.array([self.X, self.Y]), self.dimension)
            self.func = schwefelFunction # Определяем функцию

        self.F.axes.plot_surface(self.X, self.Y, self.Z, alpha=0.6, cmap=cm.coolwarm)
        self.F.draw()

        # Отрисовка графиков
        self.tempIter = 0
        self.step = self.iter / 10

        self.timer.timeout.connect(self.update)
        self.timer.start()

    # Функция обновления
    def update(self):
        self.swarm.nextIteration() # Обработка следующей итерации

        if self.tempIter == self.iter - 1:
            self.F.axes.clear()
            title = 'Итерация : ' + str((self.tempIter + 1))
            self.F.axes.set_title(title)
            self.F.axes.plot_surface(self.X, self.Y, self.Z, alpha=0.6,cmap=cm.coolwarm)
            for i in range(len(self.swarm.swarm)):
                self.F.axes.scatter(self.swarm.swarm[i].currentPosition[0], self.swarm.swarm[i].currentPosition[1],
                                    self.func(self.swarm.swarm[i].currentPosition, self.dimension),
                                    s=50, color="#FF0000", marker=".")
            self.ui.textEdit_6.setText(str(numpy.round(self.swarm.globalBestPosition, 6)) + "  " + str(round(self.swarm.globalBestFinalFunc, 6)))
            self.timer.stop()
        elif self.tempIter % self.step == 0:
            self.F.axes.clear()
            title = 'Итерация : ' + str((self.tempIter + 1))
            self.F.axes.set_title(title)
            self.F.axes.plot_surface(self.X, self.Y, self.Z, alpha=0.6)
            for i in range(len(self.swarm.swarm)):
                self.F.axes.scatter(self.swarm.swarm[i].currentPosition[0], self.swarm.swarm[i].currentPosition[1],
                                    self.func(self.swarm.swarm[i].currentPosition, self.dimension),
                                    s=50, color="#000000", marker=".")

        self.tempIter += 1 # Переходим к следующей итерации

        self.F.draw() # Отрисовка графика



# Функции
def sphereFunction(pos, dimension=2):
    return sum(pos * pos)


def schwefelFunction(pos, dimension=2):
    return sum(-pos * numpy.sin(numpy.sqrt(numpy.abs(pos))))


def rastriginFunction(pos, dimension):
    return 10.0 * dimension + sum(pos * pos - 10.0 * numpy.cos(2 * numpy.pi * pos))


# Класс Роя
class Swarm:
    def __init__(self, _swarmsize, _dimension, _minvalues, _maxvalues, _currentVelocityRatio, _localVelocityRatio,
                 _globalVelocityRatio, func):
        self.swarmsize = _swarmsize  # размер роя (количество частиц)

        self.func = func

        # Выполним проверки
        assert len(_minvalues) == len(_maxvalues)
        assert (_localVelocityRatio + _globalVelocityRatio) > 4

        self.minvalues = numpy.array(
            _minvalues[:])  # список, задающий минимальные значения для каждой координаты частицы
        self.maxvalues = numpy.array(
            _maxvalues[:])  # список, задающий максимальные значения для каждой координаты частицы

        self.currentVelocityRatio = _currentVelocityRatio  # общий масштабирующий коэффициент для скорости
        self.localVelocityRatio = _localVelocityRatio  # коэффициент, задающий влияние лучшей точки, найденной каждой частицей, на будущую скорость
        self.globalVelocityRatio = _globalVelocityRatio  # коэффициент, задающий влияние лучшей точки, найденной всеми частицами, на будущую скорость

        self.globalBestFinalFunc = None
        self.globalBestPosition = None

        self.dimension = _dimension  # Размерность функции

        self.swarm = self.createSwarm()

    # Создает рой из частиц со случайными координатами и скоростями
    def createSwarm(self):
        return [Particle(self) for _ in range(self.swarmsize)]

    # Выполнить следующую итерацию алгоритма
    def nextIteration(self):
        for particle in self.swarm:
            particle.nextIteration(self)

    # Целевая фунция
    def finalFunc(self, position):
        penalty = self.getPenalty(position, 10000.0)
        finalfunc = self.func(position, self.dimension)

        return finalfunc + penalty

    # Расчет штрафной функции
    def getPenalty(self, position, ratio):
        # position - координаты, для которых рассчитывается штраф
        # ratio - вес штрафа
        penalty1 = sum([ratio * abs(coord - minval)
                        for coord, minval in zip(position, self.minvalues)
                        if coord < minval])

        penalty2 = sum([ratio * abs(coord - maxval)
                        for coord, maxval in zip(position, self.maxvalues)
                        if coord > maxval])

        return penalty1 + penalty2

    # Расчет целевой функции
    def getFinalFunc(self, position):
        assert len(position) == len(self.minvalues)  # Проверим, что размеры совпадают

        finalFunc = self.finalFunc(position)

        if self.globalBestFinalFunc is None or finalFunc < self.globalBestFinalFunc:
            self.globalBestFinalFunc = finalFunc
            self.globalBestPosition = position[:]

        return finalFunc


# Класс частицы
class Particle(object):
    def __init__(self, swarm):
        # swarm - экземпляр класса Swarm, хранящий параметры алгоритма, список частиц и лучшее значение роя в целом
        # position - начальное положение частицы (список)

        # Текущее положение частицы
        self.currentPosition = self.getInitPosition(swarm)

        # Лучшее положение частицы
        self.localBestPosition = self.currentPosition[:]

        # Лучшее значение целевой функции
        self.localBestFinalFunc = swarm.getFinalFunc(self.currentPosition)

        self.velocity = self.getInitVelocity(swarm)

    # Возвращает список со случайными координатами для заданного интервала изменений
    def getInitPosition(self, swarm):
        return numpy.random.rand(swarm.dimension) * (swarm.maxvalues - swarm.minvalues) + swarm.minvalues

    # Генерирует начальную случайную скорость
    def getInitVelocity(self, swarm):
        assert len(swarm.minvalues) == len(self.currentPosition)
        assert len(swarm.maxvalues) == len(self.currentPosition)

        minval = -(swarm.maxvalues - swarm.minvalues)
        maxval = (swarm.maxvalues - swarm.minvalues)

        return numpy.random.rand(swarm.dimension) * (maxval - minval) + minval

    def nextIteration(self, swarm):
        # Случайный вектор для коррекции скорости с учетом лучшей позиции данной частицы
        rnd_currentBestPosition = numpy.random.rand(swarm.dimension)

        # Случайный вектор для коррекции скорости с учетом лучшей глобальной позиции всех частиц
        rnd_globalBestPosition = numpy.random.rand(swarm.dimension)

        veloRatio = swarm.localVelocityRatio + swarm.globalVelocityRatio

        commonRatio = (2.0 * swarm.currentVelocityRatio /
                       (numpy.abs(2.0 - veloRatio - numpy.sqrt(veloRatio ** 2 - 4.0 * veloRatio))))

        # Подсчитываем новую скорость
        newVelocity_part1 = commonRatio * self.velocity

        newVelocity_part2 = (commonRatio *
                             swarm.localVelocityRatio *
                             rnd_currentBestPosition *
                             (self.localBestPosition - self.currentPosition))

        newVelocity_part3 = (commonRatio *
                             swarm.globalVelocityRatio *
                             rnd_globalBestPosition *
                             (swarm.globalBestPosition - self.currentPosition))

        self.velocity = newVelocity_part1 + newVelocity_part2 + newVelocity_part3

        # Обновить позицию частицы
        self.currentPosition += self.velocity

        finalFunc = swarm.getFinalFunc(self.currentPosition)

        if finalFunc < self.localBestFinalFunc:
            self.localBestPosition = self.currentPosition[:]
            self.localBestFinalFunc = finalFunc


# Точка входа в программу
if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Widget()
    widget.show()
    sys.exit(app.exec())
