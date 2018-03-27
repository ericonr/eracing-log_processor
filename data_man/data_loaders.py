#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 18 15:49:30 2018

@author: ericonr
"""

import numpy as np
import csv

#tentando tornar OO
class csv_reader():
    def __init__(self, path):
        self.path = path

    def load_data(self, filename, headers=None):
        file_path = self.path / filename

        print('Loading data from ' + str(filename) + '...')
        csv_data = np.genfromtxt(file_path, delimiter=';', skip_header=1).T
        print('Data loaded!')

        if headers is None:
            with open(file_path, 'r') as csvfile:
                csv_reader = csv.reader(csvfile, delimiter=';')
                headers = list(csv_reader)[0]

        csv_dict={}
        for index, header in enumerate(headers):
            if header == '':
                continue
            csv_dict[header] = csv_data[index]

        print('Dictionary generated!\n')

        return csv_dict

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