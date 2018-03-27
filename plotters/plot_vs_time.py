import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt

from plotters.colors import color_index
from data_cleaners import filter_PIR

def plot_vs_time(data):
    ci = 0
    
    data_keys = list(data.keys())
    print('Data that can be plotted: ' + str(data_keys))
    get = input('Choose what you want: ').split()
    get = list(map(int, get))
    get_word = []
    for index in get:
        get_word.append(data_keys[index])
    
    fig, ax = plt.subplots()
    for word in get_word:
        if word == 'VCU_1':
            print('Plotting motor-speed...')
            label = 'Motor_speed'
            ax.scatter(data[word]['time'], data[word]['motor'], c=color_index[ci], label=label)
            ci += 1
            print('Motor speed plotted!\n')
        else:
            print('Plotting ' + word + '...')
            choice = input('Choose "r"(right), "l"(left), "b"(both), "a"(avg), "f"(filter): ')
            if choice == 'r':
                label = word + ' right'
                ax.scatter(data[word]['time'], data[word]['right'], c=color_index[ci], label=label)
                ci += 1
            elif choice == 'l':
                label = word + ' left'
                ax.scatter(data[word]['time'], data[word]['left'], c=color_index[ci], label=label)
                ci += 1
            elif choice == 'b':
                label = word + ' right'
                ax.scatter(data[word]['time'], data[word]['right'], c=color_index[ci], label=label)
                ci += 1
                label = word + ' left'
                ax.scatter(data[word]['time'], data[word]['left'], c=color_index[ci], label=label)
                ci += 1
            elif choice == 'a':
                label = word + ' average'
                ax.scatter(data[word]['time'], data[word]['avg_r'], c=color_index[ci], label=label)
                ci += 1
            elif choice == 'f':
                label = word + ' filter'
                ax.scatter(data[word]['time'], filter_PIR(data[word]['avg_r'][:]), c=color_index[ci], label=label)
                ci += 1
            print(word + ' plotted!\n')
    
    ax.set_xlabel('Time [s]')
    ax.legend()
    plt.show()