import numpy as np
from matplotlib import pyplot

x = np.linspace(-100,100,1000)
y1 = np.sin(x)
y2 = np.cos(x)

toggle = 0

def onpress(event):
    global toggle

    event.canvas.figure.clear()

    event.canvas.figure.gca().plot(x,x**toggle + toggle*x + toggle)

    event.canvas.draw()

    toggle += 1

fig = pyplot.figure()
fig.canvas.mpl_connect('key_press_event', onpress)

pyplot.plot(x,x**toggle + toggle*x + toggle)
pyplot.show()