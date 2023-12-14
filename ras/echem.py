import numpy as np
import scipy.signal as sig
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backend_bases import key_press_handler
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import tkinter

'''
The home for functions relating to manipulation of electrochemical data.
Prefaced chrono_ are those for chronoamperometry, photocurrents etc, 
data smoothing, baselining, signal manipulation etc are prefaced 'sig'.
'''

'''
Chronoamperometry-related functions:
'''

def chrono_light_dark(on_off : list, light_start : float, time : list) -> tuple[list[float],list[float]]:
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

def chrono_pc_height(data: tuple, indeces: tuple) -> tuple:
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

def chrono_time_to_index(data : tuple, time : float):
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

def av_pcs(pcs):
    '''
    Averages two or more photocurrents with each other, 
    returns averaged trace (with time axis) and associated error on current.
    '''

'''
Signal processing:
'''
def sig_smooth_av(data : tuple[list,list]):
    '''
    very rough data smoothing based on average of neighbouring points
    '''
    av_data = np.zeros(len(data[1])) #make empty array for smoothed data

    for i in range(len(data[1])):
        if i == 0:
            # special case for start of array - average first two points
            av_data[i] = (data[1][i] + data[1][i+1])/2
        if i == len(data[1]) - 1:
            # special case for end of array - average last two points
            av_data[i] = (data[1][i] + data[1][i-1])/2
        else:
            # general case - average of point and points either side
            av_data[i] = (data[1][i-1] + data[1][i] + data[1][i-1])/3
    #return numpy array of data
    return data[0],av_data

def sig_smooth_filter(data : tuple[list,list], n = 15, a = 1):
    '''
    more advanced data smoothing based on scipy.signal.lfilter, 
    returns smoothed data
    '''
    b = [1.0/n] *n
    yy = sig.lfilter(b,a,data[1])

    return data[0],yy


'''
General use functions:
'''

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