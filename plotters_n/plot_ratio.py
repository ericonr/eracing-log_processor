import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt

from data_cleaners import sanitize_array
from plotters.colors import color_index

def generate_rpm_motor(data):    
    data_keys = list(data.keys())
    print('Data that can be chosen: ' + str(data_keys))
    get = input('Choose what you want (1st / 2nd): ').split()
    get = list(map(int, get))
    get_word = []
    for index in get:
        get_word.append(data_keys[index])
        
    pd_able = []
    word_index = []
    for word in get_word:
        if word == 'VCU_1':
            data_frame = pd.DataFrame(data[word], columns=['time', 'motor'])
            word_index.append('motor')
        elif 'Pir' in word:
            data_frame = pd.DataFrame(data[word], columns=['time', 'avg_r'])
            word_index.append('avg_r')
        
        pd_able.append(data_frame)
    matched_times = pd.merge_asof(pd_able[0], pd_able[1], on='time')
    
    razao = matched_times[word_index[0]] / matched_times[word_index[1]]
    razao_san = sanitize_array(razao[:])
    return matched_times, razao, razao_san, get_word
        
def plot_ratio(data):
    matched_times, razao, razao_san, get_word = generate_rpm_motor(data)
    razao_label = get_word[0] + '/' + get_word[1]
    print('Razao media '+ razao_label + ' ' + str(razao_san.mean()))
    print('Moda da razao ' + razao_label + ' ' + str(stats.mode(razao_san)))

    fig, ax = plt.subplots()
    ci = 0
    label = 'Ratio ' + razao_label
    ax.scatter(matched_times['time'], razao, c=color_index[ci], label=label)
    ax.legend()
    plt.show()

def plot_ratio_hist(data):
    matched_times, razao, razao_san, get_word = generate_rpm_motor(data)
    razao_label = get_word[0] + '/' + get_word[1]
    print('Razao media '+ razao_label + ' ' + str(razao_san.mean()))
    print('Moda da razao ' + razao_label + ' ' + str(stats.mode(razao_san)))
    
    fig, ax = plt.subplots()
    label = 'Ratio ' + razao_label
    e_range = int(input('Choose the end of the range: '))
    n_divisions = int(input('Choose the number of divisions: '))
    ax.hist(razao_san, range=(0, e_range), bins=n_divisions, label=label)
    ax.legend()
    plt.show()