import echem.chrono as c
import gen.file_imports as f
from tkinter import *

echem_1 = f.read_chrono('C:\\Users\\hh001\\Documents\\Robin\\PhD\\Midi_PhD\\eChem experiments\\Data\\Raw Data\\20231121\\20231121_dPSI_lighttit_alone.ascii')
echem_2 = f.read_chrono('C:\\Users\\hh001\\Documents\\Robin\\PhD\\Midi_PhD\\eChem experiments\\Data\\Raw Data\\20231121\\20231121_dPSI_lighttit_200uM_DCBQ.ascii')
echem_3 = f.read_chrono('C:\\Users\\hh001\\Documents\\Robin\\PhD\\Midi_PhD\\eChem experiments\\Data\\Raw Data\\20231121\\20231121_dPSI_lighttit_400uM_DCBQ_1mM_DCMU.ascii')

on_offs = c.light_dark([60,90],30,echem_1[0])

c.plot_3_chrono(echem_1,echem_2,echem_3,on_offs)
