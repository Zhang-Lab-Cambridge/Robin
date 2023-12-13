import numpy as np

'''
Functions regarding the manipulation of UV-Vis data. Moved from 'echem' to 'gen' as of 06/12/23
eg finding ChlA concentration from a given UV-Vis spectrum, analysis of spectra for growth curves etc
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
    

