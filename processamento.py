#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 18 15:49:30 2018

@author: ericonr
"""

import numpy as np
import pandas as pd
from scipy import stats
import csv
import matplotlib.pyplot as plt

def csv_read(file, type_file):
    #make this OO later (decoders)
    
    PIR_Headers = ['left', 'right', 'avg_r', 'avg_k', 'time']
    #PIR_filtro_Headers = ['left', 'right', 'time']
    VCU_1_Headers = ['motor', 'torque', 'phase', 'power', 'speed', 'distance', 'time']
    headers_dict = {'PIR':PIR_Headers, 'VCU_1':VCU_1_Headers}
    
    print('Carregando dados de ' + str(file) + '...')
    csv_data = np.genfromtxt(file, delimiter=';', skip_header=1).T
    print('Dados carregados!')
    
    csv_dict = {}
    if type_file in headers_dict.keys():
        headers = headers_dict[type_file]
    else:
        with open(file, 'r') as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=';')
            headers = list(csv_reader)[0]
        
    
    for index, header in enumerate(headers):
        if header == '':
            continue
        csv_dict[header] = csv_data[index]
        
    csv_dict['exists'] = True
    print('Dicionario gerado!\n')
        
    return csv_dict

def verify_data(data, filenames):
    for key in data.keys():
        if not data[key]['exists']:
            if key == 'VCU_1':
                data[key] = csv_read(filenames[key], key)
            elif 'Pir' in key:
                data[key] = csv_read(filenames[key], 'PIR')

color_index = ['b', 'orange', 'g', 'r', 'gray', 'black']

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
            ax.scatter(data[word]['time'], data[word]['motor'], c=color_index[ci])
            ci += 1
            print('Motor speed plotted!\n')
        else:
            print('Plotting ' + word + '...')
            print('Choose "r"(right), "l"(left), "b"(both) or "a"(avg): ')
            choice = input()
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
            print(word + ' plotted!\n')
    
    ax.set_xlabel('Time [s]')
    ax.legend()
    plt.show()
            
def sanitize_array(array):
    array = np.array(array)
    array = array[np.isfinite(array)]
    array = array[np.logical_not(np.isnan(array))]
    array = array[np.nonzero(array)]
    return array

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
        
def plot_rpm_motor(data):
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

def plot_rpm_motor_hist(data):
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