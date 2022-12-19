import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from mpl_toolkits.mplot3d import Axes3D
import PySimpleGUI as gui
import time
import random
import math


class immuneNetwork:
    """Класс иммунной сети"""

    def __init__(self, minValue, maxValue, size_Sb, nb, intensiveParam, iterations):
        self.minValue = minValue
        self.maxValue = maxValue
        self.size_Sb = size_Sb
        self.nb = nb
        self.intensiveParam = intensiveParam
        self.iterations = iterations

    def fitness_function(self, x, y):
        pass

    def generate_population(self, minValue, maxValue, num):
        """Генерация начальной популяции"""
        population = []
        for i in range(num):
            population.append([random.uniform(minValue, maxValue), random.uniform(minValue, maxValue)])
        return population

    def get_best_antibodies(self, antibodies, nb):
        """Получаем лучшие антитела"""
        sub_antibodies = antibodies.copy()
        sub_antibodies.sort(key=lambda x: self.fitness_function(x[0], x[1]), reverse=False)
        sub_antibodies = sub_antibodies[:nb]
        return sub_antibodies

    def cloning_and_mutation(self, antibodies, intensiveParam):
        """Клонирование и мутация лучших антител"""
        clones = []
        for body in antibodies:
            alpha = math.exp(-intensiveParam * self.fitness_function(body[0], body[1]))
            clones.append([body[0] + alpha * random.uniform(-0.5, 0.5), body[1] + alpha * random.uniform(-0.5, 0.5)])
        return clones

    def generate_new_population(self, Sm, clones, nb, minValue, maxValue):
        """Создание новой популяции антител"""
        newPopulation = []
        for i in range(len(Sm)):
            if (self.fitness_function(clones[i][0], clones[i][1]) < self.fitness_function(Sm[i][0], Sm[i][1])):
                newPopulation.append(clones[i])
            else:
                newPopulation.append(Sm[i])

        newPopulation += self.generate_population(minValue, maxValue, nb)
        return newPopulation


class rosenbrock(immuneNetwork):
    """Класс функции Розенброка"""

    def __init__(self, minValue, maxValue, size_Sb, nb, intensiveParam, iterations):
        super().__init__(minValue, maxValue, size_Sb, nb, intensiveParam, iterations)

    def fitness_function(self, x, y):
        return (1 - x) ** 2 + 100 * (y - x ** 2) ** 2


class himmelblau(immuneNetwork):
    """Класс функции Химмельблау"""

    def __init__(self, minValue, maxValue, size_Sb, nb, intensiveParam, iterations):
        super().__init__(minValue, maxValue, size_Sb, nb, intensiveParam, iterations)

    def fitness_function(self, x, y):
        return ((x ** 2 + y - 11) ** 2) + (x + y ** 2 - 7) ** 2


class rastrigin(immuneNetwork):
    """Класс функции Растригина"""

    def __init__(self, minValue, maxValue, size_Sb, nb, intensiveParam, iterations):
        super().__init__(minValue, maxValue, size_Sb, nb, intensiveParam, iterations)

    def fitness_function(self, x, y):
        return 20.0 + ((x * x - 10.0 * np.cos(2 * np.pi * x) +
                        (y * y - 10.0 * np.cos(2 * np.pi * y))))


# Функция Розенброка
def rosenbrock_F(x):
    return ((1 - x[0]) ** 2) + (100 * ((x[1] - x[0] ** 2) ** 2))


# Генетический алгоритм
def genetic_algorithm(popsize, its, bound, mut, crossp, func, time_list):
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

    sc.append(fitness[best_idx])
    # sc.append(pop_denorm.tolist())

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
                    # if(abs(f-fitness[best_idx]) < 0.0001):
                    #     best_idx = j
                    #     best = trial_denorm
                    #     return best, fitness[best_idx]
                    best_idx = j
                    best = trial_denorm
        # Точки времени
        time_list.append(time.time() - time1)
        sc.append(fitness[best_idx])

        # sc.append(pop_denorm.tolist())
    # Возвращаем лучшие решения на данной итерации
    return best, fitness[best_idx], sc


if __name__ == "__main__":
    gui.theme_background_color('White')
    gui.theme_text_element_background_color('White')
    gui.theme_button_color('Green')
    gui.theme_text_color('Black')
    gui.theme_element_background_color("White")

    layout = [
        [gui.Text("Алгоритм иммунной сети", justification='center', size=(50, 1), font=('ComicSans', 16))],
        [gui.T("   ")],
        [gui.Text("Минимальное значение:", font=('ComicSans', 12), size=(31, 1)),
         gui.InputText(-6, font=('ComicSans', 12), size=(10, 1))],
        [gui.Text("Максимальное значение:", font=('ComicSans', 12), size=(31, 1)),
         gui.InputText(6, font=('ComicSans', 12), size=(10, 1))],
        [gui.Text("Размер начальной популяции антител:", font=('ComicSans', 12), size=(31, 1)),
         gui.InputText(100, font=('ComicSans', 12), size=(10, 1))],
        [gui.Text("Число антител для клонирования:", font=('ComicSans', 12), size=(31, 1)),
         gui.InputText(40, font=('ComicSans', 12), size=(10, 1))],
        [gui.Text("Параметр интенсивности:", font=('ComicSans', 12), size=(31, 1)),
         gui.InputText(0.3, font=('ComicSans', 12), size=(10, 1))],
        [gui.Text("Количество итераций:", font=('ComicSans', 12), size=(31, 1)),
         gui.InputText(100, font=('ComicSans', 12), size=(10, 1))],
        [gui.Text("Сила мутации:", font=('ComicSans', 12), size=(31, 1)),
         gui.InputText(0.8, font=('ComicSans', 12), size=(10, 1))],
        [gui.Text("Вероятность мутации:", font=('ComicSans', 12), size=(31, 1)),
         gui.InputText(0.7, font=('ComicSans', 12), size=(10, 1))],
        [gui.Radio("Функция Розенброка", "Radio1", default=True, key="Rosenbrock", font=('ComicSans', 12)),
         gui.Radio("Функция Химмельблау", "Radio1", default=False, key="Himmelblau", font=('ComicSans', 12)),
         gui.Radio("Функция Растригина", "Radio1", default=False, key="Rastrigin", font=('ComicSans', 12))],
        [gui.T("   ")],
        [gui.Text(key='result', font=('ComicSans', 12))],
        [gui.Button('Вычислить', font=('ComicSans', 12))]]

    window = gui.Window('Алгоритм иммунной сети', layout)

    while True:
        event, values = window.read()
        if event == gui.WIN_CLOSED:
            break

        if event == 'Вычислить':
            # Минимальное значение
            minValue = int(values[0])
            # Максимальное значение
            maxValue = int(values[1])
            # Размер начальной популяции антител
            size_Sb = int(values[2])
            # Число антител для мутации
            nb = int(values[3])
            # Параметр интенсивности
            intensiveParam = float(values[4])
            # Количество итераций
            iterations = int(values[5])
            # Сила мутации
            mut = float(values[6])
            # Вероятность мутации
            crossp = float(values[7])

            if values["Rosenbrock"] == True:
                network = rosenbrock(minValue, maxValue, size_Sb, nb, intensiveParam, iterations)
            elif values["Himmelblau"]:
                network = himmelblau(minValue, maxValue, size_Sb, nb, intensiveParam, iterations)
            else:
                network = rastrigin(minValue, maxValue, size_Sb, nb, intensiveParam, iterations)

            # -----------------------ГЕНЕТИКА-------------------------------------------------
            time1 = time.time()
            time_list3 = []

            lol, lol1, solution3 = genetic_algorithm(size_Sb, iterations, [minValue, maxValue], mut, crossp, rosenbrock_F, time_list3)

            # Точки времени
            time_list3.append(time.time() - time1)

            # ------------------------------------------------ИММУНКА-----------------------

            time1 = time.time()
            time_list1 = []
            solution1 = []

            # Генерация случайной популяции
            Sb = network.generate_population(minValue, maxValue, size_Sb)
            for i in range(iterations):
                # Получение лучших антител
                Sm = network.get_best_antibodies(Sb, nb)
                # Получение мутантных клонов
                clones = network.cloning_and_mutation(Sm, intensiveParam)
                # Создание новой популяции с учетом клонов
                Sb = network.generate_new_population(Sm, clones, nb, minValue, maxValue)

                # Нахождение лучшего решения в популяции
                best_solution = network.fitness_function(Sb[0][0], Sb[0][1])
                best_index = 0
                for i in range(1, len(Sb)):
                    if network.fitness_function(Sb[i][0], Sb[i][1]) < best_solution:
                        best_index = i
                        best_solution = network.fitness_function(Sb[i][0], Sb[i][1])
                result = [Sb[best_index], best_solution]

                # Точки времени
                time_list1.append(time.time() - time1)
                # Точки решений
                solution1.append(result[1])
            # -------------------------------Гибрид---------------------------------------------

            time1 = time.time()
            time_list2 = []
            solution2 = []

            # Генерация случайной популяции
            Sb = network.generate_population(minValue, maxValue, size_Sb)
            for i in range(iterations):

                # Получение лучших антител
                Sm = network.get_best_antibodies(Sb, nb)

                Sm = np.array(Sm)

                # Генетика
                for j in range(len(Sm)):
                    # Получаем индексы потомков всех кроме текущего
                    idxs = [idx for idx in range(len(Sm)) if idx != j]

                    # Выбираем случайных 3 потомков
                    a, b, c = Sm[np.random.choice(idxs, 3, replace=False)]

                    # Изменение потомков
                    # Ограниченичиваем элементы массива от 0 до 1 если мутация вышла за рамки
                    mutant = np.clip(a + mut * (b - c), minValue, maxValue)

                    # Создаем рандомную мутацию, применив вероятность мутации
                    cross_points = np.random.rand(2) < crossp

                    # Если мутация не была созданна, то создадим новую, изменив 1 элемент
                    if not np.any(cross_points):
                        cross_points[np.random.randint(0, 2)] = True

                    # В гене где нет мутации, заменяем на популяцию TRUE - mutant; False - pop[j](оставляем предыдущую)
                    trial = np.where(cross_points, mutant, Sm[j])

                    # Получаем её приспособленность
                    f = network.fitness_function(trial[0], trial[1])

                    # Если полученная мутация лучше(меньше) текущей особи, то заменяем её в популяции
                    if f < network.fitness_function(Sm[j][0], Sm[j][1]):
                        Sm[j] = trial

                # Получение мутантных клонов
                clones = network.cloning_and_mutation(Sm, intensiveParam)

                # Создание новой популяции с учетом клонов
                Sb = network.generate_new_population(Sm, clones, nb, minValue, maxValue)

                # Нахождение лучшего решения в популяции
                best_solution = network.fitness_function(Sb[0][0], Sb[0][1])
                best_index = 0

                for i in range(1, len(Sb)):
                    if network.fitness_function(Sb[i][0], Sb[i][1]) < best_solution:
                        best_index = i
                        best_solution = network.fitness_function(Sb[i][0], Sb[i][1])

                result = [Sb[best_index], best_solution]

                # Точки времени
                time_list2.append(time.time() - time1)
                # Точки решений
                solution2.append(result[1])

            # Вывод результата
            window['result'].update(f"Результат: {result}")

            # Построение графика эффективности
            fig, ax = plt.subplots()
            ax.plot(time_list1, solution1, color="red")
            ax.plot(time_list2, solution2, color='blue')
            ax.plot(time_list3, solution3, color='green')
            plt.show()

            # Построение 3D графика
            x = np.arange(float(values[0]), float(values[1]), 0.1)
            y = np.arange(float(values[0]), float(values[1]), 0.1)
            x_plot, y_plot = np.meshgrid(x, y)
            fun_plot = network.fitness_function(x_plot, y_plot)

            # 3D График
            ax = plt.figure().add_subplot(111, projection='3d')
            ax.plot_surface(x_plot, y_plot, fun_plot, rstride=5, cstride=5, alpha=0.7)

            # Отображение точки минимума
            ax.scatter(result[0][0], result[0][1], result[1], color='red')
            plt.show()

    window.close()