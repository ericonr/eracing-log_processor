#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 18 15:49:30 2018

@author: ericonr
"""

import numpy as np
import csv

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