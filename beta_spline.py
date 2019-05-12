from graphics import *
import sys
import numpy as np

def bspline(t, degree, points, knots = [], weights = []):
    n = len(points)
    d = len(points[0])

    if(len(weights) == 0):
        for x in range(n):
            weights.append(1)

    if(len(knots) == 0):
        for x in range(n+degree+1):
            knots.append(x)

    domain = [degree, len(knots)-1 - degree]

    low = knots[domain[0]]
    high = knots[domain[1]]

    t = t * (high - low) + low

    s = domain[0]
    while(s < domain[1]):
        if(knots[s] <= t <= knots[s+1]):
            break
        s = s + 1

    # print(s)

    v = []
    for i in range(n):
        v.append([])
        for j in range(d):
            v[i].append(points[i][j] * weights[i])
        v[i].append(weights[i])

    # print(v)

    for l in range(1, degree+1):
        for i in range(s, s-degree-1+l, -1):
            alpha = (t - knots[i]) / (knots[i+degree+1-l] - knots[i])
            for j in range(0, d+1):
                v[i][j] = (1 - alpha) * v[i-1][j] + alpha * v[i][j]

    result = []
    for i in range(d):
        result.append(v[s][i]/v[s][d])
    return result

points = [
  [-1.0,  0.0],
  [-0.5,  0.5],
  [ 0.5, -0.5],
  [ 1.0,  0.0]
]

degree = 2 # number of points for approximation
# knots = [0, 1, 2, 3, 4, 5, 6]

t = 0
win = GraphWin("My Window", 1000, 900)
win.setBackground(color_rgb(0,0,0))

while(t<1):
    sums = bspline(t, degree, points) # generate x, y coor of point
    pt = Point(sums[0]*100, (300 - sums[1]*100))
    pt.setFill(color_rgb(100, 255, 50))
    pt.draw(win)
    t = t + 0.01

win.getMouse()
win.close()