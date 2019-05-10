from graphics import *
import numpy

points = [[0,0],[1,1],[2,0], [3,0.5], [2, 2], [0.5, 5]]

def binominal(i, n):
	return numpy.math.factorial(n)/(numpy.math.factorial(i)*(numpy.math.factorial(n-i)))

win = GraphWin("My Window", 1000, 500)
win.setBackground(color_rgb(0,0,0))

for point in points:
	pt = Point(point[0]*100, (500 - point[1]*100))
	pt.setFill(color_rgb(255, 0, 0))
	pt.draw(win)

t=0
while(t<=1.0):
	x = 0
	y = 0
	# z = 0
	for index, point in enumerate(points):
		x = x + (binominal(index, len(points)-1) * (t**index)*(1-t)**((len(points)-1)-index))*point[0]
		y = y + (binominal(index, len(points)-1) * (t**index)*(1-t)**((len(points)-1)-index))*point[1]
		# z = z + (binominal(index, len(points)-1) * (t**index)*(1-t)**((len(points)-1)-index))*point[2]
	pt = Point(x*100, (500 - y*100))
	pt.setFill(color_rgb(100, 255, 50))
	pt.draw(win)
	# print(x, y)
	t = t + 0.0005 # точність

win.getMouse()
win.close()


