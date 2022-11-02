from tkinter import *
from tkinter import ttk
import optimization as opt
import pandas as pd
import numpy as np
import matplotlib.figure import Figure
from matplotlib.backends.backedn_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk
)

class Optimchart:
    def __init__(self, root, df):
        self.root = root
        self.root.title('Optimization charts')
        self.root.geometry('1200x600')
        self.root.columnconfigure(0, weight = 4, minsize = 800)
        self.root.columnconfigure(1, weight = 1, minsize = 300)

        self.style = ttk.Style()
        self.style.configure('TButton', font = ('Arial', 11, 'bold'))
        self.style.configure('Header.TLabel', font = ('Arial', 15, 'bold'))
        self.style.configure('Header.TFrame', background = '#E0F0D7')
        self.style.configure('Header.TButton')

        #GUI chart frame
        self.chart_frame = ttk.Frame(self.root, relief = RAISED, borderwidth = 2)
        self.chart_frame.columnconfigure(0, weight = 1, minsize = 1100)
        #self.chart_frame.rowconfigure(0, weight = 1)
        self.chart_frame['borderwidth'] = 20
        self.chart_frame.grid(column=0, row=0)

        #GUI navigation frame
        self.nav_frame = ttk.Frame(self.root, relief = GROOVE, borderwidth = 5)
        self.nav_frame.columnconfigure(0, weight = 0, minsize = 300)
        self.nav_frame.grid(column=1, row=0)

        #nav_frame Header
        rig_frame = ttk.Frame(self.nav_frame, style = 'Header.TFrame')
        rig_frame.grid(row = 0, column = 0, padx = 2, pady= 2)
        odoptu = ttk.Button(rig_frame, text = 'ODOPTU', style = 'Header.TButton')
        odoptu.grid(row = 0, column = 0, padx = 3, pady = 3)
        berkut = ttk.Button(rig_frame, text = 'BERKUT')
        odoptu.grid(row = 0, column = 1, padx = 3, pady = 3)
        orlan = ttk.Button(rig_frame, text = 'ORLAN')
        odoptu.grid(row = 0, column = 2, padx = 3, pady = 3)

        #preload files to database
        self.df = df
        self.df.load_to_df('odwi05_mseda.las', 'ODWI-05', 8.5, True)
        self.df.load_to_df('odwi03_mseda.las', 'ODWI-03', 8.5)
        self.df.load_to_df('op14_mseda.las', 'OP-14', 8.5)
        self.df.load_to_df('op39_mseda.las', 'OP-39', 8.5)

        #nav_frame well checkboxes
        self.checkbox_frame = ttk.Frame(self.nav_frame)
        self.checkbox_frame.grid(row=2, column = 0)
        self.well_var = []
        self.wells_base = list(self.df.show_well_base())

        for i in range(len(self.wells_base)):
            self.well_var[self.wells_base[i]] = {}
            self.well_var[self.wells_base[i]]['bool'] = BooleanVar()
        self.build_well_content(self.checkbox_frame, self.well_var)

        #nav_frame parameters checkbox
        self.parm_frame = ttk.Frame(self.nav_frame)
        self.parm_frame.grid(row = 1, column = 0)
        self.parm_var = {}
        self.parms = self.df.show_params()

        for i in range(len(self.parms)):
            self.parm_var[self.parms[i]] = {}
            self.parm_var[self.parms[i]]['bool'] = BooleanVar()
        self.build_parm_content(self.parm_frame, self.parm_var)

        #nav_frame_well sections
        self.sect = IntVar()
        self.build_well_sect(self.nav_frame, self.sect)

    def build_parm_content(self, root, var):
        header = ttk.Label(root, text='Parametrs in database', justify = CENTER, font = 18)
        header.grid(column = 0, row = 0)
        frame = ttk.Frame (root)
        frame.grid(row = 1, column = 0)
        count = 0
        for key in var.keys():
            var[key]['button'] = Checkbutton(frame, text = key, onvalue = True, offvalue = False,
                    variable = var[key]['bool'], command = self.well_chart)
            var[key]['button'].grid(row=count, column = 0, sticky=W)
            count += 1
    
    def build_well_content(self, root, var):

        header = ttk.Label(root, text = 'Wells in database', justify = CENTER, font = 18)
        header.grid(column = 0, row = 0)
        frame = ttk.Frame(root)
        frame.grid(row = 1, column = 0)
        count = 0
        for key in var.keys():
            var[key]['button'] = Checkbutton(frame, text = key, onvalue = True, offvalue = False,
                    variable = var[key]['bool'], command = self.well_chart)
            var[key]['button'].grid(row=count, column = 0, sticky=W)
            count += 1

    def build_well_sect(self, root, sect):
        
        frame = ttk.Frame(root)
        header = ttk.Label(frame, text = 'Sections available', justify = CENTER, font = 18)
        frame.grid(row=3, column = 0)
        combobox = ttk.Combobox(frame, textbariable = sect, state = 'readonly')
        combobox['values'] = (24, 17.5, 12.25, 8.5)
        combobox.current(3)
        header.grid(column = 0, row = 0)
        combobox.grid(column = 0, row = 1, sticky = W)

    def chart_build(self,fig,row):
        figure_canvas = FigureCanvasTkAgg(fig, master = self.chart_frame)
        figure_canvas.get_tk_widget().grid(row=row, column = 0)

    def well_chart(self):
        self.wells_show = []
        self.params = []
        for key in self.parm_var.keys():
            if self.parm_var[key]['bool'].get() == True:
                self.params.append(key)
        for key in self.well_var.keys():
            if self.well_var[key]['bool'].get() == True:
                self.wells_show.append(key)
        self.df.set_well(self.wells_show)
        for i, par in enumerate(self.params):
            if par == 'SPPA': self.df.draw('SPPA', [7700, 10000, 100], [2000, 4000, 500])
            if par == 'ROP': self.df.draw('ROP', [7700, 10000, 100], [0, 80, 20])
            if par == 'SWOB': self.df.draw('SWOB', [7700, 10000, 100], [0, 50, 10])
            if par == 'STOR': self.df.draw('STOR', [7700, 10000, 100], [30, 80, 10])
            if par == 'SMSE': self.df.draw('SMSE', [7700, 10000, 100])
            if par == 'DECD': self.df.draw('DECD', [7700, 10000, 100])
            if par == 'TFLO': self.df.draw('TFLO', [7700, 10000, 100])
            if par == 'RPM': self.df.draw('RPM', [7700, 10000, 100])
            if par == 'SS': self.df.draw('SS', [7700, 10000, 100])
            self.chart_build(self.df.get_figure(), i)

if __name__ == '__main__':
    root = Tk()
    app = Optimchart(root, opt.optim())
    #app.chart_build(the_plot.fig)
    root.mainloop()

