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
    points = np.random.random(POINT_COUNT)
    points = [(idx, p) for idx, p in enumerate(points)]

    degree = 25  # number of points for approximation
    for pn in PROCESSES:
        process_count = 2 ** pn

        time1 = time.time()

        steps = np.arange(0, 1, STEP)
        pool = mp.Pool(process_count)
        results = []
        for chunk in divide_chunks(points, degree):
            results.extend(pool.starmap(calculate_coord, [(chunk, t) for t in steps]))
        pool.close()

        time2 = time.time()
        print("%s processes. Time: %s" % (process_count, time2 - time1))

        plt.figure()
        for x, y in points:
            plt.scatter(x, y, color='red')
        result_x = [el[0] for el in results]
        result_y = [el[1] for el in results]
        plt.plot(result_x, result_y, color='blue')
        plt.grid(True)
        plt.savefig('bezier_result.png')


if __name__ == "__main__":
    start()
