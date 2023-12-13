import numpy as np
import scipy.signal as sig

'''
Electrochemistry-relating signal processing, eg data smoothing and baselining.
'''

def smooth_av(data : tuple[list,list]):
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

def smooth_filter(data : tuple[list,list], n = 15, a = 1):
    '''
    more advanced data smoothing based on scipy.signal.lfilter, 
    returns smoothed data
    '''
    b = [1.0/n] *n
    yy = sig.lfilter(b,a,data[1])

    return data[0],yy


