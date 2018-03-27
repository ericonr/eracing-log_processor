import numpy as np
import matplotlib.pyplot as plt

from data_cleaners import filter_PIR

from plotters.colors import color_index
from data_man.lists import *

def fft_gen(array, d=1/100):
    array_fft = np.real(np.fft.rfft(array))
    array_freq = np.fft.rfftfreq(n=len(array), d=d)
    return array_fft, array_freq

def plot_fft(data, ax):
    ci = 0
    
    data_keys = [key for key in data.keys()]
    get_word = receive_list('Data that can be plotted vs frequency', 'Choose the data you want to plot', data_keys)

    for word in get_word:
        data_to_plot, labels = data[word].choose_plot(include_time=False)
        for index, array in enumerate(data_to_plot):
            label = word + ' ' + labels[index]

            rfft, rfft_freq = fft_gen(array[:], data[word]._d)
            ax.scatter(rfft_freq, rfft, c=color_index[ci], label=label)
            ci += 1
    
    ax.set_title('Fourier Transform')
    ax.set_xlabel('Frequency [Hz]')
    ax.set_ylabel('Magnitude')
    ax.legend()