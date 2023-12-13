from tkinter import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import numpy as np

def plot():
    fig = Figure(figsize=(5,5),dpi=100)

    y = [i**2 for i in range(101)]

    ax = fig.add_subplot(111)
    ax.plot(y)

    canvas = FigureCanvasTkAgg(fig,master=window)
    canvas.draw()
    canvas.get_tk_widget().pack()

    toolbar = NavigationToolbar2Tk(canvas,window)
    toolbar.update()

    canvas.get_tk_widget().pack()


window = Tk()

window.title('Plots plots plots')

window.geometry("500x500")

plot_button = Button(master = window, command=plot, height = 2, width = 10, text = 'Plot')

plot_button.pack()

window.mainloop()