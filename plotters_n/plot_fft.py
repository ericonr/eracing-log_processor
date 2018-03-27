import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from data_cleaners import filter_PIR

from plotters.colors import color_index

def fft_gen(array, d=1/100):
    array_fft = np.real(np.fft.rfft(array))
    array_freq = np.fft.rfftfreq(n=len(array), d=d)
    return array_fft, array_freq

def plot_fft(data):
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
            rfft, rfft_freq = fft_gen(data[word]['motor'])
            ax.scatter(rfft_freq, rfft, c=color_index[ci], label=label)
            ci += 1
            print('Motor speed plotted!\n')
        else:
            print('Plotting ' + word + '...')
            choice = input('Choose "r"(right), "l"(left), "b"(both), "a"(avg), "f"(filter): ')

            def scatter(axis, word, label_part, data_x, ci, d=1/100):
                label = word + ' ' + label_part
                rfft, rfft_freq = fft_gen(data_x[:], d)
                axis.scatter(rfft_freq, rfft, c=color_index[ci], label=label)

            if choice == 'r':
                scatter(ax, word, 'right', data[word]['right'], ci)
                ci += 1
            elif choice == 'l':
                scatter(ax, word, 'left', data[word]['left'], ci)
                ci += 1
            elif choice == 'b':
                scatter(ax, word, 'right', data[word]['right'], ci)
                ci += 1
                scatter(ax, word, 'left', data[word]['left'], ci)
                ci += 1
            elif choice == 'a':
                scatter(ax, word, 'avg_r', data[word]['avg_r'], ci)
                ci += 1
            elif choice == 'f':
                scatter(ax, word, 'filtered', filter_PIR(data[word]['avg_r']), ci)
                ci += 1
            
            print(word + ' plotted!\n')
    
    ax.set_xlabel('Frequency [Hz]')
    ax.legend()
    plt.show()