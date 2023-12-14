import ras.plot as p
import tkinter

'''
Functions to assemble various interactable user interface windows for different purposes :)
'''

def build_echem_window(data,on_off,max_height,labels):

    '''
    Builds and assembles tkinter window with overall chronoamp trace
    and individual pc window
    '''

    root = tkinter.Tk()
    root.wm_title("Chronoamperometry/Photocurrents")

    plot_1 = p.plot_chrono_tkinter(data,on_off,root)
    plot_2 = p.plot_pcs_tkinter(data,on_off,max_height,labels,root)

    button_quit = tkinter.Button(master=root, text="Quit",command=root.destroy)

    button_quit.pack(side=tkinter.BOTTOM)

    plot_1[0].get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=True)
    plot_1[1].pack(side=tkinter.TOP, fill=tkinter.X)

    plot_2[2].pack(side=tkinter.BOTTOM)
    plot_2[1].pack(side=tkinter.BOTTOM, fill=tkinter.X)
    plot_2[0].get_tk_widget().pack(side=tkinter.BOTTOM, fill=tkinter.BOTH, expand=True)

    tkinter.mainloop()
