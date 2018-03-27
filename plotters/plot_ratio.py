import numpy as np
import pandas as pd
from scipy import stats

from data_man.data_cleaners import sanitize_array
from data_man.lists import *
from plotters.colors import color_index

def generate_rpm_motor(data):    
    data_keys = [key for key in data.keys()]
    get_word = receive_list('Data whose ratio can be calculated', 'Choose the data you want to plot', data_keys)

    pd_able = []
    word_index = []

    for word in get_word:
        data_to_plot, labels = data[word].choose_plot()
        for index, array in enumerate(data_to_plot):
            label = word + ' ' + labels[index]
            word_index.append(label)

            data_frame = {label:array[0], 'time':array[1]}
            data_frame = pd.DataFrame(data_frame, columns=['time', label])

            pd_able.append(data_frame)

    matched_times = pd.merge_asof(pd_able[0], pd_able[1], on='time')
    
    razao = matched_times[word_index[0]] / matched_times[word_index[1]]
    razao_san = sanitize_array(razao[:])

    razao_label = word_index[0] + ' / ' + word_index[1]

    return matched_times, razao, razao_san, word_index, razao_label
        
def plot_ratio(data, ax):
    matched_times, razao, razao_san, word_index, razao_label = generate_rpm_motor(data)
    ci = 0
    label = 'Ratio ' + razao_label
    ax.scatter(matched_times['time'], razao, c=color_index[ci], label=label)
    ax.set_title(label + ' vs time')
    ax.set_xlabel('Time [s]')
    ax.set_ylabel('Ratio [1]')
    ax.legend()

def plot_ratio_hist(data, ax):
    matched_times, razao, razao_san, word_index, razao_label = generate_rpm_motor(data)
    print('Mean ratio '+ razao_label + ' ' + str(razao_san.mean()))
    print('Mode of ratio ' + razao_label + ' ' + str(stats.mode(razao_san)))

    label = 'Ratio ' + razao_label
    e_range = int(input('Choose the end of the range: '))
    n_divisions = int(input('Choose the number of divisions: '))
    ax.hist(razao_san, range=(0, e_range), bins=n_divisions, label=label)
    ax.set_title(label + ' histogram')
    ax.set_xlabel('Frequency')
    ax.set_ylabel('Ratio [1]')
    ax.legend()