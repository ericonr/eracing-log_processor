import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt

from plotters.colors import color_index
from data_man.data_cleaners import filter_PIR
from data_man.lists import *

def plot_vs_time(data, ax):
    ci = 0
    
    data_keys = [key for key in data.keys()]
    get_word = receive_list('Data that can be plotted vs time', 'Choose the data you want to plot', data_keys)

    for word in get_word:
        data_to_plot, labels = data[word].choose_plot()
        for index, array in enumerate(data_to_plot):
            label = word + ' ' + labels[index]
            ax.scatter(array[1], array[0], c=color_index[ci], label=label)
            ci += 1
    
    ax.set_title('Time plot')
    ax.set_xlabel('Time [s]')
    ax.legend()