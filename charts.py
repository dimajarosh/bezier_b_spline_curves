import matplotlib.pyplot as plt
import numpy as np

from beta_spline import bspline
from bezier import divide_chunks, calculate_coord
from constants import POINT_COUNT, STEP

COLORS = ['green', 'blue', 'orange', 'purple']

if __name__ == "__main__":
    np.random.seed(234)
    points = np.random.random(POINT_COUNT)
    points = [(idx, p) for idx, p in enumerate(points)]

    steps = np.arange(0, 1, STEP)

    for color_index, degree in enumerate([2, 3, 4, len(points)]):
        results_bezier = list()
        for chunk in divide_chunks(points, degree):
            for t in steps:
                results_bezier.append(calculate_coord(chunk, t))

        # len -1 for beta splines
        if degree == len(points):
            degree = len(points) - 1
        knots = list()
        for i in range(len(points) + degree + 1):
            if i <= degree:
                knots.append(0)
            elif degree < i < len(points):
                knots.append(i - degree + 1)
            elif i >= len(points):
                knots.append(len(points) - degree + 2)
        results_spline = list()
        for t in steps:
            results_spline.append(bspline(t, degree, points, knots=knots))

        result_x1 = [el[0] for el in results_bezier]
        result_y1 = [el[1] for el in results_bezier]

        result_x2 = [el[0] for el in results_spline]
        result_y2 = [el[1] for el in results_spline]

        # plt.plot(result_x2, result_y2, color=COLORS[color_index])

        plt.figure()
        plt.grid(True)
        for x, y in points:
            plt.scatter(x, y, color='red')
        plt.plot(result_x1, result_y1, color='blue')
        plt.savefig('bezier_result_%s.png' % degree)

        plt.figure()
        plt.grid(True)
        for x, y in points:
            plt.scatter(x, y, color='red')
        plt.plot(result_x2, result_y2, color='green')
        plt.savefig('beta_spline_result_%s.png' % degree)

        plt.figure()
        plt.grid(True)
        for x, y in points:
            plt.scatter(x, y, color='red')
        plt.plot(result_x1, result_y1, color='blue')
        plt.plot(result_x2, result_y2, color='green')
        plt.savefig('together_%s.png' % degree)

        # plt.savefig('beta_spline_result_all.png')
