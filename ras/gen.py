import numpy as np

'''
General functions, eg file manipulation and import, uv vis analysis :)
'''

'''
Functions relating to file import, in whatever form you need. 
Was initially located in 'echem' package, but moved to 'gen' as of 06/12/23
Rewired into gen file in 'ras' overall package 14/12/23
'''

def read_chrono(file_name : str) -> tuple[list,list]:
    '''
    Takes .ascii file location of chronoamperometry experiment, returns tuple of time vs current
    '''
    file = open(file_name, 'r')
    lines = file.readlines() #list of lines in the file
    file.close()

    time = []
    current = []


    for i in range(len(lines)):
        if i > 0:
            string = lines[i].split() #splits at gaps, in this case tabs but should be general
            time.append(float(string[0]))
            current.append(float(string[1]))
        
    return time,current


def read_uvvis(file_name : str, trace_n: int) -> tuple[list,list]:
    #has now been edited for files that have multiple 'samples' in, ie csv has more than two columns of usable data
    '''
    Takes .csv file location of uv-vis file, and the index of the particular dataset required, returns wavelength vs intensity
    '''
    file = open(file_name, 'r')
    lines = file.readlines() #list of lines in the file
    file.close()

    wavelength = []
    intensity = []

    for i in range(len(lines)):
        if i > 1 and lines[i] != '\n':
            string = lines[i].split(',') #splits at gaps, in this case tabs but should be general
            #print(string)
            wavelength.append(float(string[2*trace_n+0]))
            intensity.append(float(string[2*trace_n+1]))

    return wavelength, intensity


'''
UV Vis analysis:
'''

def chla_mol(data : tuple[list,list], epsilon = 79.95, l = 1.0, vol = 200.0, mr = 893.5) -> list[float,float,float]:
    '''
    Finds ChlA peak height in UV-Vis spectrum, then finds ChlA conc and associated error 
    from absorption peak height + error. Value of epsilon is that of methanol 
    - change if using other things. Volume of methanol used = 200ul as standard, 
    remains in ul. L = cuvette width in cm, Mr = that of ChlA. Returns value in mol ChlA :)
    '''

    intensity = np.array(data[1])
    peak = np.max(intensity[0:400])
    peak_loc = np.where(intensity == peak)[0][0]
    peak_wl = data[0][peak_loc]

    baseline = np.mean(data[1][0:25])

    err_bl = np.std(data[1][0:25])
    err_tot = np.sqrt(2)*err_bl

    total_height = peak-baseline

    if 650 < peak_wl < 700:

        c = total_height / (epsilon * l) #concentration of ChlA in mg/ml
        mass = c * vol/1000 #calculates mass on electrode in mg
        n = mass/mr * 1e-3 #calculates num. mmol, converts to mol :)
        chl_err = (err_tot/(epsilon*l)) * ((vol/1000)/mr) * 1e-3

        return n,chl_err

    else:
        raise Exception('Cannot find ChlA peak in reasonable location: found peak at ' + data[0][peak_loc])
    
