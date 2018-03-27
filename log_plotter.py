#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 18 02:03:45 2018

@author: ericonr
"""

import argparse as arg
from pathlib import Path

from data_man.data_loaders import verify_data
from plotters.plot_vs_time import plot_vs_time
from plotters.plot_ratio import plot_rpm_motor, plot_rpm_motor_hist
from plotters.plot_fft import plot_fft

path_parser = arg.ArgumentParser(description='Select the path of the files to be processed: ')
path_parser.add_argument('-p', '--path')
path = Path( path_parser.parse_args().path )
print('Path to files: ' + str(path) + '\n')

#OO it

filenames = {'PirF':'Final_Log_PirF.csv', 'PirR':'Final_Log_PirR.csv', 'PirF_filtrado':'Final_Log_PirF_Filtro.csv', 'PirR_filtrado':'Final_Log_PirR_Filtro.csv', 'VCU_1':'Final_Log_VCU_Info_1.csv'}
for key in filenames.keys():
    filenames[key] = path / filenames[key]

PirF = {'exists':False}
PirR = {'exists':False}
PirF_filtrado = {'exists':False}
PirR_filtrado = {'exists':False}
VCU_1 = {'exists':False}
data = {'PirF':PirF, 'PirR':PirR, 'PirF_filtrado':PirF_filtrado, 'PirR_filtrado':PirR_filtrado, 'VCU_1':VCU_1}
verify_data(data, filenames)

plot_function = {'vs-time':plot_vs_time, 'RPM/Motor':plot_rpm_motor, 'RPM/Motor-histogram':plot_rpm_motor_hist, 'Discrete FFT':plot_fft}
plots = list(plot_function.keys())
while(1):
    print('Plot options: ' + str(plots))
    plot_type = int(input('Choose one: '))
    plot_function[plots[plot_type]](data)