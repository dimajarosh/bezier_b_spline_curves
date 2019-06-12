import multiprocessing as mp

import matplotlib.pyplot as plt
import numpy as np

from constants import POINT_COUNT, PROCESSES, STEP
from graphics import *


def bspline(t, degree, points, knots=list(), weights=list()):
    n = len(points)
    d = len(points[0])

    if len(weights) == 0:
        for x in range(n):
            weights.append(1)

    if len(knots) == 0:
        for x in range(n + degree + 1):
            knots.append(x)

    domain = [degree, len(knots) - 1 - degree]

    low = knots[domain[0]]
    high = knots[domain[1]]

    t = t * (high - low) + low

    s = domain[0]
    while s < domain[1]:
        if knots[s] <= t <= knots[s + 1]:
            break
        s = s + 1

    v = []
    for i in range(n):
        v.append([])
        for j in range(d):
            v[i].append(points[i][j] * weights[i])
        v[i].append(weights[i])

    for l in range(1, degree + 1):
        for i in range(s, s - degree - 1 + l, -1):
            alpha = (t - knots[i]) / (knots[i + degree + 1 - l] - knots[i])
            for j in range(0, d + 1):
                v[i][j] = (1 - alpha) * v[i - 1][j] + alpha * v[i][j]

    result = []
    for i in range(d):
        result.append(v[s][i] / v[s][d])
    return result


def start():
    # points = [
    #     (-1.0, 0.0),
    #     (-0.5, 0.5),
    #     (0.5, -0.5),
    #     (1.0, 0.0)
    # ]

    # генерування рандомних точок
    points = np.random.random(POINT_COUNT)
    points = [(idx, p) for idx, p in enumerate(points)]

    # кількість точок для апроксимації
    degree = 25
    # knots = [0, 1, 2, 3, 4, 5, 6]
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
        # виклик функції бетасплайну в окремому процесі з певним кроком
        results = pool.starmap(bspline, [(t, degree, points) for t in steps])
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
        plt.savefig('beta_spline_result.png')


if __name__ == "__main__":
    start()
