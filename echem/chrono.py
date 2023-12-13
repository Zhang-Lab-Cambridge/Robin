import numpy as np
import scipy.signal as sig
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backend_bases import key_press_handler
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import tkinter


'''
The home for functions relating to data manipulation and photocurrent height extraction from chronoamperometry data.
Functions for splitting up the trace into individual phtoocurrents can be found in 'splitting', 
and data smoothing, baselining, signal manipulation etc can be found in 'signal'.
'''

def light_dark(on_off : list, light_start : float, time : list) -> tuple[list[float],list[float]]:
    '''
    Outputs times at which light turns on and off. 
    Input on_off len(2) -> time spent on and off in seconds (eg [60,90] for live cells)
    '''
    on_times = [light_start] #initialises an array of times the light turns on
    off_times = [0.0,light_start+on_off[0]] #initialises array of times light turns off

    for i in range(100):
        #loop to add to our intial arrays, they've been initalised so it's just adding a constant offset each time
        if off_times[i+1] > time[-1]:
            #keeps arrays only as long as the time period the data exists over :)
            break
        on_times.append(on_times[i] + on_off[1]+ on_off[0])
        off_times.append(off_times[i+1] + on_off[0] + on_off[1])
    
    return on_times,off_times

def pc_height(data: tuple, indeces: tuple) -> tuple:
    '''
    More general version of the old function, takes as input: \n 1. any data including a photocurrent (data), \n
    2. the times to start averaging in the light and in the dark (to subtract the two) 
    and the time over which to average (eg 5s). These are both in array index form, not time form \n
    Form of: [[light_start, light_time],[dark_start, dark_time]]
    '''
    #NB TO FUTURE SELF: we should have another function that converts from time to index, to take into account the fact
    #that some of my data is at 0.2s per datapoint and some is at 0.1s :/

    #take average current in light period and dark period
    light_height = np.mean(data[1][indeces[0][0] : indeces[0][0]+indeces[0][1]])
    dark_height = np.mean(data[1][indeces[1][0] : indeces[1][0]+indeces[1][1]])

    #take std of current in same period
    light_std = np.std(data[1][indeces[0][0] : indeces[0][0]+indeces[0][1]])
    dark_std = np.std(data[1][indeces[1][0] : indeces[1][0]+indeces[1][1]])

    #subtract one from the other to give photocurrent, find associated error
    height = light_height - dark_height
    std = np.sqrt(light_std**2 + dark_std**2) #adding in quadrature to propagate error on intial averages

    return height, std

def time_to_index(data : tuple, time : float):
    '''
    Takes data tuple [time,current], and time you wish to convert. Searches time axis of data for closest timepoint, 
    returns the associated index :) Should inform you of the closest timepoint found also!
    '''
    if time in data[0]:
        #if the time is directly in the data, just gimme the index
        index = data[0].index(time)
    else:
        for i in range(len((data[0]))):
            if i > 0 and data[0][i-1] <= time <= data[0][i]:
                #find the two timepoints in the data that the quoted timepoint is between
                low_diff = time - data[0][i-1] #how close is it to the  lower bound?
                high_diff = data[0][i] - time #how close is it to the upper bound?

                #following if statement tree just gives index of the closest data_time to the given time
                if low_diff < high_diff: 
                    index = i-1
                elif high_diff <= low_diff:
                    index = i
                else:
                    #this should technically never be raised by the laws of maths, but is here just in case
                    raise("I am confusion, please help")
            else:
                print(time)
                print("can't find")
                raise(Exception)

    print(index)
                
    return index, data[0][index]
                

def norm_to_cla(data : tuple[list,list], n_chl : float) -> tuple[list,list]:
    '''
    Normalises current to no. moles of ChlA in sample, 
    for easy comparison between runs. n_chl is in nmol, 
    function output has current in A/mol
    '''
    new_data = [[],[]]
    for i in data:
        new_data[0].append[i[0]]
        new_data[1].append[i[1]/(n_chl*1e9)]

    return new_data

def av_pcs(pcs):
    '''
    Averages two or more photocurrents with each other, 
    returns averaged trace (with time axis) and associated error on current.
    '''

    


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
        on_off_indeces[0].append(time_to_index(data,i)[0])

    for i in on_off[1][1:-2]:
        on_off_indeces[1].append(time_to_index(data,i)[0])

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
