import plotly.express as px
import pandas as pd
import seaborn as sns
import numpy as np
import lasio
import matplotlib.pyplot as plt
from copy import copy
import matplotlib.colors as mcolors
import random

#General Data Container
field = {}
MUD_WEIGHT = 12.4

def load_las (path):
    """
    Function takes a path to the file and transforms it to pandas dataframe
    """
    las = lasio.read(r'{}'.format(path))
    return las.df()

def load_to_field(well, section, mseda):
    """
    Function loads dataframe to dictionary "field"
    """
    if well in field.keys():
        field[well][section] = {}
        field[well][section]['mseda'] = mseda
    else:
        field[well] = {}
        field[well][section] = {}
        field[well][section]['mseda'] = mseda
    #Calculating delta ECD
    field[well][section]['mseda']['DECD']=field[well][section]['mseda']['ECD'] - MUD_WEIGHT
    field[well][section]['mseda']['SS'] = field[well][section]['mseda']['STICK']/(field[well][section]['mseda']['RPM']*2)

def update_database(file_name, well_name, section):
    df=load_las(file_name)
    load_to_field(well_name, section, df)

class iptim():

    def __init__(self):
        self.df = {}
        self.wells = [None]
        self.section = None
        self.colors = {'WEll_1': 'k', 'WELL_2': 'orange', 'WELL_3': 'g', 'WELL_4': 'magenta'}
        self.parameters = {'SPPA': 'Stand pipe pressure, psi', 'ROP': 'ROP, m/h', 'SWOB': 'WOB, klbf', 'STOR': 'Surface Torque, kft lbf',
        'SMSE': 'MSE, kpsi', 'DECD': 'ΔECD, ppg', 'TFLO': 'Flowrate, gpm', 'RPM': 'RPM, c/min', 'SS': 'Stick Slip'}
    
    def load_to_df(self, path, well, section, main=False):
        las = lasio.read(r'{}'.format(path))
        if well in self.df.keys():
            self.df[well][section] = {}
            self.df[well][section]['mseda'] = las.df()
        else:
            self.df[well] = {}
            self.df[well][section] = {}
            self.df[well][section]['mseda'] = las.df()
        #Calculating delta ECD
        self.df[well][section]['mseda']['DECD']=self.df[well][section]['mseda']['ECD'] - MUD_WEIGHT
        self.df[well][section]['mseda']['SS'] = self.df[well][section]['mseda']['STICK']/(self.df[well][section]['mseda']['RPM']*2)

        if main==True: self.wells[0] = len(self.wells) - 1
        self.section = float(section)

    def show_params(self):
        return list(self.parameters.keys())
    
    def show_well_base(self):
        return list(self.df.keys())
    
    def set_well (self, l):
        if self.wells[0] == None:
            self.wells = [None]
            self.wells = self.wells + 1
        else:
            self.wells = [self.wells[0]]
            self.wells = self.wells + 1
        
    def get_color(self, well):
        color = random.choice(list(mcolors.BASE_COLORS.items()))[0]
        while color in self.colors.values():
            color = random.choice(list(mcolors.BASE_COLORS.items()))[0]
        if well not in self.colors.keys():
            self.colors[well] = color
        return self.colors[well]
    
    def add_line(self, well, section, parm, color, main=False):
        return self.ax.plot(self.df[well][section]['mseda'].index, self.df[well][section]['mseda'][parm],
        label=well, color=color, lw=1.6, if main==True else 1, zorder = 2 if main==True else 1, alpha=1 if main==True else 0.6)
    
    def draw(self, parm, xlim=None, ylim=None):
        self.fig = plt.figure(figsize=(15, 3))
        self.ax = self.fig.add_subplot(111)
        self.fig.suptitle(self.parameters[parm].split(',')[0], fontdict={'fontsize': 22, 'fontweight': 'bold', 
        'color': 'black'})
        for i in range(1, len(self,wells)):
            self.add_line(self.wells[i], self.section, parm, self.get_color(self.wells[i]), True if self.wells[0]==i else False)
        self.ax.legend(loc='right', fontsize=14, markerscale = 2.0), self.ax.tick_params(labelsize=12)
        self.ax.set_ylabel(self.parameters[parm], fontdict={'fontsize': 15, 'color': 'black'}), self.ax.grid(axis='y')

        if xlim is not None:
            self.ax.set_xticks(np.arange(xlim[0], xlim[1]+1, xlim[2]))
            self.ax.set_xlim(xlim[0], xlim[1])
        if ylim is not None:
            self.ax.set_yticks(np.arange(ylim[0], ylim[1]+1, ylim[2]))
            self.ax.set_xlim(ylim[0], ylim[1])
        return plt.show()

    def get_figure(self):
        return self.fig
if __name__ == '__main__':
    charts=optim()
    charts.load_to_df('WELL01_mseda.las', 'WELL_1', 8.5, True)
    charts.load_to_df('WELL02_mseda.las', 'WELL_2', 8.5)
    charts.load_to_df('WELL03_mseda.las', 'WELL_3', 8.5)
    charts.load_to_df('WELL04_mseda.las', 'WELL_4', 8.5)
    charts.draw('SPPA', [7700, 10000, 100], [2000, 4000, 500])
    charts.draw('ROP', [7700, 10000, 100], [0, 80, 20])
    charts.draw('SWOB', [7700, 10000, 100], [0, 50, 10])
    charts.draw('STOR', [7700, 10000, 100], [30, 80, 10])
        