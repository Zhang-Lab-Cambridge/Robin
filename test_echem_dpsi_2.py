import echem.chrono as c
import echem.file_imports as f
from tkinter import *

echem_1 = f.read_chrono('C:\\Users\\hh001\\Documents\\Robin\\PhD\\Midi_PhD\\eChem experiments\\Data\\Raw Data\\20231123\\20231123_dPSI_rep5_alone.ascii')
echem_2 = f.read_chrono('C:\\Users\\hh001\\Documents\\Robin\\PhD\\Midi_PhD\\eChem experiments\\Data\\Raw Data\\20231123\\20231123_dPSI_rep5_200uM_dcbq.ascii')
echem_3 = f.read_chrono('C:\\Users\\hh001\\Documents\\Robin\\PhD\\Midi_PhD\\eChem experiments\\Data\\Raw Data\\20231123\\20231123_dPSI_rep5_200uM_dcbq_1mM_dcmu.ascii')

on_offs = c.light_dark([60,90],30,echem_1[0])

c.plot_3_chrono(echem_1,echem_2,echem_3,on_offs)
