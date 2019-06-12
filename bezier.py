import multiprocessing as mp
import time

import matplotlib.pyplot as plt
import numpy as np
import sys

from constants import PROCESSES, STEP, POINT_COUNT


def binomial(i, n):
    return np.math.factorial(n) / (np.math.factorial(i) * (np.math.factorial(n - i)))


def calculate_coord(points, t):
    x = 0
    y = 0
    for index, point in enumerate(points):
        x = x + (binomial(index, len(points) - 1) * (t ** index) * (1 - t) ** ((len(points) - 1) - index)) * point[0]
        y = y + (binomial(index, len(points) - 1) * (t ** index) * (1 - t) ** ((len(points) - 1) - index)) * point[1]
    return x, y


def divide_chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]


def start():
    # points = [(0, 0), (1, 1), (2, 0), (3, 0.5), (2, 2), (0.5, 5)]
    # генерування рандомних точок
    points = np.random.random(POINT_COUNT)
    points = [(idx, p) for idx, p in enumerate(points)]

    # кількість точок для апроксимації
    degree = 25
    # цикл що змінює кількість процесів
    for pn in PROCESSES:
        # кількість процесів
        process_count = 2 ** pn

        # час початку виконання
        time1 = time.time()

        # масив що містить числа від нуля до одиниці з певним кроком
        steps = np.arange(0, 1, STEP)
        # пул запущених процесів
        pool = mp.Pool(process_count)
        # масив з результатами
        results = []

        # розділення точок на чанки певного розміру
        for chunk in divide_chunks(points, degree):
            # виклик функції calculate_coord у окремому процесі з певним кроком
            # додавання результату до масиву результатів
            results.extend(pool.starmap(calculate_coord, [(chunk, t) for t in steps]))
        # закривання пулу процесів
        pool.close()

        # час закінчення виконання
        time2 = time.time()
        print("%s processes. Time: %s" % (process_count, time2 - time1))

        # створення графіку
        plt.figure()
        # позначення точок на графіку
        for x, y in points:
            plt.scatter(x, y, color='red')
        # видобування координати х з масиву результатів
        result_x = [el[0] for el in results]
        # видобування координати у з масиву результатів
        result_y = [el[1] for el in results]
        # відображення графіку
        plt.plot(result_x, result_y, color='blue')
        plt.grid(True)
        # записування графіку до файлу
        plt.savefig('bezier_result.png')


if __name__ == "__main__":
    start()
