import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backend_bases import key_press_handler
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import tkinter
import ras.echem as e



def plot_chrono_tkinter(data : tuple[list,list], on_off : tuple[list,list],root):

    '''
    Plots the whole stepped chrono trace inside a tkinter window. 
    Edit 'echem.chrono.build_window' to make changes to whether this plot exists in a given tkinter window.
    '''

    #define figure
    fig = Figure(figsize=(5, 4), dpi=100)
    #plot data on axes :)
    ax = fig.add_subplot()
    ax.plot(data[0],data[1],'b')

    #light-dark periods in grey
    for i in range(int(np.floor(len(on_off[1])-1))):
        ax.axvspan(on_off[1][i], on_off[0][i], facecolor='#cccccc', alpha=0.5)
    ax.set_title('Overall Chronoamperometry')

    #make a canvas and put the figure on it
    canvas = FigureCanvasTkAgg(fig,master=root)
    canvas.draw()
    
    #initialise and create matplotlib toolbar
    toolbar = NavigationToolbar2Tk(canvas,root,pack_toolbar=False)
    toolbar.update()

    #I don't know why this is here but it seems to make everything work so I'm leaving it
    #my guess is that it forces the connection between matplotlib & the canvas
    canvas.mpl_connect(
        "key_press_event", lambda event: print(f"you pressed {event.key}"))
    canvas.mpl_connect("key_press_event",key_press_handler)

    #decided to do the packing in a higher level function, so returns canvas,toolbar
    return canvas,toolbar

def plot_pcs_tkinter(data : tuple[list,list], on_off : tuple[list,list], max_height : float, labels : list, root):
    '''
    Want to:
    plot all the photocurrents in one window, toggle between them with a slider.
    Should be possible now I've somehow fixed the tkinter<->matplotlib issues
    '''
    #define figure
    fig = Figure(figsize=(5, 4), dpi=100)

    on_off_indeces = [[],[0.0]]

    for i in on_off[0][0:-2]:
        on_off_indeces[0].append(e.chrono_time_to_index(data,i)[0])

    for i in on_off[1][1:-2]:
        on_off_indeces[1].append(e.chrono_time_to_index(data,i)[0])

    print(on_off_indeces)

    #plot initial photocurrent on axes :)
    ax = fig.add_subplot()
    line, = ax.plot(data[0][0:int(on_off_indeces[1][1])],data[1][0:int(on_off_indeces[1][1])],'b') #fix pls rob

    #light-dark periods in grey
    for i in range(int(np.floor(len(on_off[1])-1))):
        ax.axvspan(on_off[1][i], on_off[0][i], facecolor='#cccccc', alpha=0.5)
    ax.set_title('Photocurrents')
    ax.set_ylim(0,2000)

    #make a canvas and put the figure on it
    canvas = FigureCanvasTkAgg(fig,master=root)
    canvas.draw()
    
    #initialise and create matplotlib toolbar
    toolbar = NavigationToolbar2Tk(canvas,root,pack_toolbar=False)
    toolbar.update()

    #I don't know why this is here but it seems to make everything work so I'm leaving it
    #my guess is that it forces the connection between matplotlib & the canvas
    canvas.mpl_connect(
        "key_press_event", lambda event: print(f"you pressed {event.key}"))
    canvas.mpl_connect("key_press_event",key_press_handler)

    #THIS IS A THING THAT CHANGES WHICH PHOTOCURRENT YOU PLOT WITH A LIL SLIDER

    # Needs a fix somewhere as the nmbering isn't aligned. So take a look at some point pls robbo

    def update_plot(val):
        n = int(val)
        label_n = str(labels[n-1])
        line.set_data(data[0][int(on_off_indeces[1][n-1]):int(on_off_indeces[0][n])],data[1][int(on_off_indeces[1][n-1]):int(on_off_indeces[0][n])])
        ax.set_xlim(on_off[1][n-1],on_off[0][n])
        ax.set_ylim(data[1][int(on_off_indeces[1][n-1])+900]-200,data[1][int(on_off_indeces[1][n-1])+900]+ max_height + 100)
        ax.legend([label_n])
        canvas.draw()

    slider_update = tkinter.Scale(root, from_=1, to=len(on_off[1]), orient=tkinter.HORIZONTAL,
                              command=update_plot, label="nth photocurrent")

    return canvas,toolbar,slider_update


def pcs_overlay_tkinter(data : tuple[list,list], on_off : tuple[list,list], labels : list, root):
    '''
    Plot all photocurrents overlaid on one another.
    '''


def plot_chrono(data : tuple[list,list], on_off : tuple[list,list]):

    fig,ax = plt.subplots()

    ax.plot(data[0],data[1],'b')

    for i in range(int(np.floor(len(on_off[1])-1))):
        ax.axvspan(on_off[1][i], on_off[0][i], facecolor='#cccccc', alpha=0.5)
    ax.set_title('Test chrono plot')

    ax.set_xlim([data[0][0],data[0][-1]])

    plt.show()

def plot_3_chrono(data_1 : tuple[list,list], data_2 : tuple[list,list], data_3 : tuple[list,list], on_off : tuple[list,list]):

    fig,ax = plt.subplots()

    ax.plot(data_3[0],data_3[1],'royalblue',label='++DCMU')
    ax.plot(data_1[0],data_1[1],'lightsteelblue',label='alone')
    ax.plot(data_2[0],data_2[1],'cornflowerblue',label='+DCBQ')


    for i in range(int(np.floor(len(on_off[1])-1))):
        ax.axvspan(on_off[1][i], on_off[0][i], facecolor='#cccccc', alpha=0.5)
    ax.set_title('dPSI')
    ax.legend()

    ax.set_xlim([data_1[0][0],data_1[0][-1]])

    plt.show()
