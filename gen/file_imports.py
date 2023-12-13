

'''
The home for functions relating to file import, in whatever form you need. 
Was initially located in 'echem' package, but moved to 'gen' as of 06/12/23
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
