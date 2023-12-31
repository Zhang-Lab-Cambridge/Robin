import ras.gui as gui
import ras.echem as echem
import ras.gen as gen
import ras.plot as plot

echem_1 = gen.read_chrono('C:\\Users\\hh001\\Documents\\Robin\\PhD\\Midi_PhD\\eChem experiments\\Data\\Raw Data\\20231123\\20231123_dPSI_rep5_alone.ascii')
light = [0.1,0.1,0.1,0.1,0.25,0.5,1,2.5,5,7.5,10,12.2,12.2,10,7.5,5,2.5,1,0.5,0.25,0.1,0.1]

o = echem.chrono_light_dark([60,90],30,echem_1[0])
gui.build_echem_window(echem_1,o,300,light)
