import random
import math
import time
import sys
import pylab
from PySide6 import QtCore
from PySide6.QtWidgets import QApplication, QWidget, QGridLayout
from forms.Beeswarm import Ui_Widget
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class floatbee:
    """Класс пчел"""
    def __init__(self):
        # Положение пчелы (искомые величины)
        self.position = None

        # Интервалы изменений искомых величин (координат)
        self.minval = None
        self.maxval = None

        # Значение целевой функции
        self.fitness = 0.0

    def calcfitness(self):
        """Расчет целевой функции. Этот метод необходимо перегрузить в производном классе.
        Функция не возвращает значение целевой функции, а только устанавливает член self.fitness
        Эту функцию необходимо вызывать после каждого изменения координат пчелы"""
        pass

    def sort(self, otherbee):
        """Функция для сортировки пчел по их целевой функции (здоровью) в порядке убывания."""
        if self.fitness < otherbee.fitness:
            return -1
        elif self.fitness > otherbee.fitness:
            return 1
        else:
            return 0

    def otherpatch(self, bee_list, range_list):
        """Проверить находится ли пчела на том же участке, что и одна из пчел в bee_list.
        range_list - интервал изменения каждой из координат"""
        # Если пчел нет в лучшем участке
        if len(bee_list) == 0:
            return True

        # Проходим по всем пчелам в участке
        for curr_bee in bee_list:
            position = curr_bee.getposition() # Берем позицию данной лучшей пчелки

            # Проходим по каждой координате
            for i in range(len(self.position)):
                # Если какая то координата не находится на том же участке
                if abs(self.position[i] - position[i]) > range_list[i]:
                    return True

        return False

    # Геттер координат
    def getposition(self):
        return [val for val in self.position]

    def goto(self, otherpos, range_list):
        """Перелет в окрестность места, которое нашла другая пчела. Не в то же самое место! """

        # К каждой из координат добавляем случайное значение
        self.position = [otherpos[n] + random.uniform(-range_list[n], range_list[n]) \
                         for n in range(len(otherpos))]

        # Проверим, чтобы не выйти за заданные пределы
        self.checkposition()

        # Расчитаем и сохраним целевую функцию
        self.calcfitness()

    def gotorandom(self):
        # Заполним координаты случайными значениями
        self.position = [random.uniform(self.minval[n], self.maxval[n]) for n in range(len(self.position))]
        self.checkposition() # Корректировка координат
        self.calcfitness() # Вычисление целевой функции

    def checkposition(self):
        """Скорректировать координаты пчелы, если они выходят за установленные пределы"""
        for n in range(len(self.position)):
            if self.position[n] < self.minval[n]:
                self.position[n] = self.minval[n]

            elif self.position[n] > self.maxval[n]:
                self.position[n] = self.maxval[n]


class hive:
    """Улей. Управляет пчелами"""

    def __init__(self, scoutbeecount, selectedbeecount, bestbeecount, selsitescount, bestsitescount, range_list, beetype):
        """
        scoutbeecount - Количество пчел-разведчиков
        selectedbeecount - количество пчел, посылаемое на остальные выбранные участки
        bestbeecount - Количество пчел, отправляемые на лучшие участки

        selsitescount - количество выбранных участков
        bestsitescount - количество лучших участков среди выбранных
        range_list - список диапазонов координат для одного участка
        beetype - класс пчелы, производный от bee
        """

        self.scoutbeecount = scoutbeecount
        self.selectedbeecount = selectedbeecount
        self.bestbeecount = bestbeecount

        self.selsitescount = selsitescount
        self.bestsitescount = bestsitescount

        self.beetype = beetype

        self.range = range_list

        # Лучшая на данный момент позиция
        self.bestposition = None

        # Лучшее на данный момент здоровье пчелы (чем больше, тем лучше)
        self.bestfitness = -1.0e9

        # Начальное заполнение роя пчелами со случайными координатами
        beecount = scoutbeecount + selectedbeecount * selsitescount + bestbeecount * bestsitescount
        self.swarm = [beetype() for n in range(beecount)]

        # Лучшие и выбранные места
        self.bestsites = []
        self.selsites = []


        self.swarm.sort(key=lambda bee: bee.fitness, reverse=True) # Сортировка
        self.bestposition = self.swarm[0].getposition() # Лучшее решение
        self.bestfitness = self.swarm[0].fitness # Значение лучшего решения

    def sendbees(self, position, index, count):
        """ Послать пчел на позицию.
        Возвращает номер следующей пчелы для вылета """
        for i in range(count):
            # Чтобы не выйти за пределы улея
            if index == len(self.swarm):
                break

            curr_bee = self.swarm[index]

            if curr_bee not in self.bestsites and curr_bee not in self.selsites:
                # Пчела не на лучших или выбранных позициях
                curr_bee.goto(position, self.range)

            index += 1

        return index

    def nextstep(self):
        """Новая итерация"""
        # Выбираем самые лучшие места и сохраняем ссылки на тех, кто их нашел
        self.bestsites = [self.swarm[0]]

        curr_index = 1

        # идем с конца
        for currbee in self.swarm[curr_index: -1]:
            # Если пчела находится в пределах уже отмеченного лучшего участка, то ее положение не считаем
            if currbee.otherpatch(self.bestsites, self.range):
                # Добавляем лучшее место
                self.bestsites.append(currbee)

                # Если нашли максимальное количество лучших участков
                if len(self.bestsites) == self.bestsitescount:
                    break
            # Обновляем счетчик
            curr_index += 1

        # Выбираем остальные места
        self.selsites = []

        for currbee in self.swarm[curr_index: -1]:
            # Если пчела находится в пределах уже отмеченных участках, то ее положение не считаем
            if currbee.otherpatch(self.bestsites, self.range) and currbee.otherpatch(self.selsites, self.range):
                self.selsites.append(currbee)

                if len(self.selsites) == self.selsitescount:
                    break

        # Отправляем пчел на задание :)
        # Отправляем сначала на лучшие места

        # Номер очередной отправляемой пчелы. 0-ую пчелу никуда не отправляем
        bee_index = 1

        for best_bee in self.bestsites:
            bee_index = self.sendbees(best_bee.getposition(), bee_index, self.bestbeecount)

        for sel_bee in self.selsites:
            bee_index = self.sendbees(sel_bee.getposition(), bee_index, self.selectedbeecount)

        # Оставшихся пчел пошлем куда попадет
        for curr_bee in self.swarm[bee_index: -1]:
            curr_bee.gotorandom()

        self.swarm.sort(key=lambda bee: bee.fitness, reverse=True)
        self.bestposition = self.swarm[0].getposition()
        self.bestfitness = self.swarm[0].fitness


# Фитнесс функции ------------------------------------------------------------------------------------------------------

class spherebee(floatbee):
    """Функция - сумма квадратов по каждой координате"""

    # Количество координат
    count = 2

    @staticmethod
    def getstartrange():
        return [150.0] * spherebee.count

    @staticmethod
    def getrangekoeff():
        return [0.98] * spherebee.count

    def __init__(self):
        floatbee.__init__(self)

        self.minval = [-150.0] * spherebee.count
        self.maxval = [150.0] * spherebee.count

        self.position = [random.uniform(self.minval[n], self.maxval[n]) for n in range(spherebee.count)]
        self.calcfitness()

    def calcfitness(self):
        """Расчет целевой функции. Этот метод необходимо перегрузить в производном классе.
        Функция не возвращает значение целевой функции, а только устанавливает член self.fitness
        Эту функцию необходимо вызывать после каждого изменения координат пчелы"""
        self.fitness = 0.0
        for val in self.position:
            self.fitness -= val * val


class dejongbee(floatbee):
    """Функция De Jong"""

    # Количество координат
    count = 2

    @staticmethod
    def getstartrange():
        return [2.048] * dejongbee.count

    @staticmethod
    def getrangekoeff():
        return [0.98] * dejongbee.count

    def __init__(self):
        floatbee.__init__(self)

        self.minval = [-2.048] * dejongbee.count
        self.maxval = [2.048] * dejongbee.count

        self.position = [random.uniform(self.minval[n], self.maxval[n]) for n in range(dejongbee.count)]
        self.calcfitness()

    def calcfitness(self):
        """Расчет целевой функции. Этот метод необходимо перегрузить в производном классе.
        Функция не возвращает значение целевой функции, а только устанавливает член self.fitness
        Эту функцию необходимо вызывать после каждого изменения координат пчелы"""
        x1 = self.position[0]
        x2 = self.position[1]

        self.fitness = 3905.93 - 100.0 * ((x1 * x1 - x2) ** 2) - ((1 - x1) ** 2)


class goldsteinbee(floatbee):
    """Функция Goldstein & Price"""

    # Количество координат
    count = 2

    @staticmethod
    def getstartrange():
        return [2.0] * goldsteinbee.count

    @staticmethod
    def getrangekoeff():
        return [0.98] * goldsteinbee.count

    def __init__(self):
        floatbee.__init__(self)

        self.minval = [-2.0] * goldsteinbee.count
        self.maxval = [2.0] * goldsteinbee.count

        self.position = [random.uniform(self.minval[n], self.maxval[n]) for n in range(goldsteinbee.count)]
        self.calcfitness()

    def calcfitness(self):
        """Расчет целевой функции. Этот метод необходимо перегрузить в производном классе.
        Функция не возвращает значение целевой функции, а только устанавливает член self.fitness
        Эту функцию необходимо вызывать после каждого изменения координат пчелы"""
        x1 = self.position[0]
        x2 = self.position[1]

        self.fitness = -(1.0 + ((x1 + x2 + 1.0) ** 2) * (
                19.0 - 14.0 * x1 + 3.0 * x1 * x1 - 14.0 * x2 + 6.0 * x1 * x2 + 3.0 * x2 * x2)) * \
                       (30.0 + ((2.0 * x1 - 3.0 * x2) ** 2) * (
                               18.0 - 32.0 * x1 + 12.0 * x1 * x1 + 48.0 * x2 - 36.0 * x1 * x2 + 27.0 * x2 * x2))


class rosenbrockbee(floatbee):
    """Функция Rosenbrock"""

    # Количество координат
    count = 2

    @staticmethod
    def getstartrange():
        return [10.0] * rosenbrockbee.count

    @staticmethod
    def getrangekoeff():
        return [0.98] * rosenbrockbee.count

    def __init__(self):
        floatbee.__init__(self)

        self.minval = [-10.0] * rosenbrockbee.count
        self.maxval = [10.0] * rosenbrockbee.count

        self.position = [random.uniform(self.minval[n], self.maxval[n]) for n in range(rosenbrockbee.count)]
        self.calcfitness()

    def calcfitness(self):
        """Расчет целевой функции. Этот метод необходимо перегрузить в производном классе.
        Функция не возвращает значение целевой функции, а только устанавливает член self.fitness
        Эту функцию необходимо вызывать после каждого изменения координат пчелы"""

        self.fitness = 0.0
        for n in range(1):
            xi = self.position[n]
            xi1 = self.position[n + 1]

            self.fitness -= 100.0 * (((xi * xi - xi1) ** 2) + ((1 - xi) ** 2))


class testbee(floatbee):
    count = 4

    @staticmethod
    def getstartrange():
        return [20.0] * testbee.count

    @staticmethod
    def getrangekoeff():
        return [0.98] * testbee.count

    """Функция	из статьи"""

    def __init__(self):
        floatbee.__init__(self)

        self.minval = [-500.0] * testbee.count
        self.maxval = [500.0] * testbee.count

        self.position = [random.uniform(self.minval[n], self.maxval[n]) for n in range(testbee.count)]
        self.calcfitness()

    def calcfitness(self):
        """Расчет целевой функции. Этот метод необходимо перегрузить в производном классе.
        Функция не возвращает значение целевой функции, а только устанавливает член self.fitness
        Эту функцию необходимо вызывать после каждого изменения координат пчелы"""

        self.fitness = 0.0
        for n in range(testbee.count):
            xi = self.position[n]

            self.fitness += -xi * math.sin(math.sqrt(abs(xi)))

        self.fitness *= -1


class funcbee(floatbee):
    """Пчела для поиска коэффициентов степенной функции"""

    # Количество координат
    count = 5

    @staticmethod
    def getstartrange():
        return [5.0] * funcbee.count

    @staticmethod
    def getrangekoeff():
        return [0.995, 0.99, 0.97, 0.95, 0.9]
    def __init__(self):
        floatbee.__init__(self)

        # Количество точек для расчета
        self.xcount = 30

        self.minval = [-15.0] * funcbee.count
        self.maxval = [15.0] * funcbee.count

        # Интервал, в котором могут изменяться значения x (не координаты пчелы)
        xmin = -20.0
        xmax = 20.0

        # Точки для расчета целевой функции. У каждой пчелы задается случайным образом
        self.x1_points = [random.uniform(xmin, xmax) for n in range(self.xcount)]
        self.x2_points = [random.uniform(xmin, xmax) for n in range(self.xcount)]
        self.x3_points = [random.uniform(xmin, xmax) for n in range(self.xcount)]
        self.x4_points = [random.uniform(xmin, xmax) for n in range(self.xcount)]

        # Рассчитаем значения правильной целевой функции
        self.correct_vals = [
            self.correctfunc(self.x1_points[n], self.x2_points[n], self.x3_points[n], self.x4_points[n]) \
            for n in range(self.xcount)]

        self.position = [random.uniform(self.minval[n], self.maxval[n]) for n in range(funcbee.count)]
        self.calcfitness()

    def correctfunc(self, x1, x2, x3, x4):
        """Правильная целевая функция"""
        a4 = 10.01
        a3 = 1.72
        a2 = -5.93
        a1 = 9.94
        a0 = -13.55

        return a4 * (x4 ** 4) + a3 * (x3 ** 3) + a2 * (x2 ** 2) + a1 * x1 + a0

    def unknownfunc(self, x1, x2, x3, x4):
        return self.position[4] * (x4 ** 4) + \
               self.position[3] * (x3 ** 3) + \
               self.position[2] * (x2 ** 2) + \
               self.position[1] * x1 + \
               self.position[0]

    def calcfitness(self):
        """Расчет целевой функции. Этот метод необходимо перегрузить в производном классе.
        Функция не возвращает значение целевой функции, а только устанавливает член self.fitness
        Эту функцию необходимо вызывать после каждого изменения координат пчелы"""

        self.fitness = 0.0
        for n in range(self.xcount):
            self.fitness -= \
                abs(self.unknownfunc(self.x1_points[n], self.x2_points[n], self.x3_points[n], self.x4_points[n]) - \
                    self.correct_vals[n])

        self.fitness /= self.xcount

#-----------------------------------------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------------------------------------

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
            int(self.ui.textEdit.toPlainText()),
            int(self.ui.textEdit_2.toPlainText()),
            int(self.ui.textEdit_3.toPlainText()),
            int(self.ui.textEdit_4.toPlainText()),
            int(self.ui.textEdit_5.toPlainText()),
            int(self.ui.textEdit_7.toPlainText()),
            int(self.ui.textEdit_8.toPlainText())))

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
        self.ui.textEdit.setText("1000")
        self.ui.textEdit_2.setText("300")
        self.ui.textEdit_3.setText("30")
        self.ui.textEdit_4.setText("10")
        self.ui.textEdit_5.setText("5")
        self.ui.textEdit_6.setText("")
        self.ui.textEdit_7.setText("15")
        self.ui.textEdit_8.setText("10")

    def start(self, func, iterations, scoutbeecount, bestbeecount, selectedbeecount, bestsitescount, selsitescount, max_func_counter):
        self.timer.stop()
        self.ui.textEdit_6.setText("") # Очистка решений
        # Параметры алгоритма
        # Класс пчел, который будет использоваться в алгоритме
        self.iter = iterations
        self.max_func_counter = max_func_counter
        beetype = spherebee

        if func == "Функция сферы":
            beetype = spherebee
        elif func == "Функция De Jong":
            beetype = dejongbee
        elif func == "Функция Goldstein & Price":
            beetype = goldsteinbee
        elif func == "Функция Rosenbrock":
            beetype = rosenbrockbee
        elif func == "Функция из статьи":
            beetype = testbee
        elif func == "Степенная функция":
            beetype = funcbee

        self.func = beetype
        # Во столько раз будем уменьшать область поиска
        self.koeff = beetype.getrangekoeff()

        self.currhive = hive(scoutbeecount, selectedbeecount, bestbeecount, selsitescount, bestsitescount,
                        beetype.getstartrange(), beetype)

        x = []
        y = []

        x_best = []
        y_best = []

        x_sel = []
        y_sel = []

        for curr_bee in self.currhive.swarm:
            if curr_bee in self.currhive.bestsites:
                x_best.append(curr_bee.position[0])
                y_best.append(curr_bee.position[1])

            elif curr_bee in self.currhive.selsites:
                x_sel.append(curr_bee.position[0])
                y_sel.append(curr_bee.position[1])

            else:
                x.append(curr_bee.position[0])
                y.append(curr_bee.position[1])

        self.F.axes.clear()
        self.F.axes.scatter(x, y, c='k', s=1, marker='o')

        if len(x_sel) != 0:
            self.F.axes.scatter(x_sel, y_sel, c='y', s=20, marker='o')

        self.F.axes.scatter(x_best, y_best, c='r', s=30, marker='o')

        self.F.draw()

        # Начальное значение целевой функции
        self.best_func = -1.0e9

        # Количество итераций без улучшения целевой функции
        self.func_counter = 0

        # Отрисовка графиков
        self.tempIter = 0

        self.timer.timeout.connect(self.update)
        self.timer.start()

    # Функция обновления
    def update(self):
        self.ui.textEdit_6.setText(
            str([round(self.currhive.bestposition[0], 3), round(self.currhive.bestposition[1], 3)]) + "  " + str(
                round(self.currhive.bestfitness, 3)))

        # Вычисляем следующую итерацию
        self.currhive.nextstep()

        if self.currhive.bestfitness != self.best_func:
            # Найдено место, где целевая функция лучше
            self.best_func = self.currhive.bestfitness
            self.func_counter = 0  # Обновляем счетчик

            x = []
            y = []

            x_best = []
            y_best = []

            x_sel = []
            y_sel = []

            for curr_bee in self.currhive.swarm:
                if curr_bee in self.currhive.bestsites:
                    x_best.append(curr_bee.position[0])
                    y_best.append(curr_bee.position[1])

                elif curr_bee in self.currhive.selsites:
                    x_sel.append(curr_bee.position[0])
                    y_sel.append(curr_bee.position[1])

                else:
                    x.append(curr_bee.position[0])
                    y.append(curr_bee.position[1])

            self.F.axes.clear()
            title = 'Итерация : ' + str((self.tempIter + 1))
            self.F.axes.set_title(title)
            self.F.axes.scatter(x, y, c='k', s=1, marker='o')

            if len(x_sel) != 0:
                self.F.axes.scatter(x_sel, y_sel, c='y', s=20, marker='o')

            self.F.axes.scatter(x_best, y_best, c='r', s=30, marker='o')
        else:
            self.func_counter += 1  # Обновляем счетчик, что не было улучшений
            # Если уже достигнуто максимальное число без итераций
            if self.func_counter == self.max_func_counter:
                # Уменьшим размеры участков
                self.currhive.range = [self.currhive.range[m] * self.koeff[m] for m in range(len(self.currhive.range))]
                # print(self.currhive.range)
                self.func_counter = 0

                x = []
                y = []

                x_best = []
                y_best = []

                x_sel = []
                y_sel = []

                for curr_bee in self.currhive.swarm:
                    if curr_bee in self.currhive.bestsites:
                        x_best.append(curr_bee.position[0])
                        y_best.append(curr_bee.position[1])

                    elif curr_bee in self.currhive.selsites:
                        x_sel.append(curr_bee.position[0])
                        y_sel.append(curr_bee.position[1])

                    else:
                        x.append(curr_bee.position[0])
                        y.append(curr_bee.position[1])

                self.F.axes.clear()
                title = 'Итерация : ' + str((self.tempIter + 1))
                self.F.axes.set_title(title)
                self.F.axes.scatter(x, y, c='k', s=1, marker='o')

                if len(x_sel) != 0:
                    self.F.axes.scatter(x_sel, y_sel, c='y', s=20, marker='o')

                self.F.axes.scatter(x_best, y_best, c='r', s=30, marker='o')

        self.tempIter += 1 # Обновление счетчика

        if (self.tempIter >= self.iter):
            self.timer.stop()

        self.F.draw() # Отрисовка графика


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Widget()
    widget.show()
    sys.exit(app.exec())




