import argparse as arg
import signal
from pathlib import Path

import matplotlib.pyplot as plt

from lists import *

from data_man.data_storage import PIR, MotorSpeed
from data_man.data_loaders import csv_reader

from plotters_n.plot_vs_time import plot_vs_time
from plotters_n.plot_ratio import plot_ratio, plot_ratio_hist
from plotters_n.plot_fft import plot_fft

def close(x, y):
    print("Bye, darling!")
    exit()
signal.signal(signal.SIGINT, close)

path_parser = arg.ArgumentParser(description='Select the path of the files to be processed: ')
path_parser.add_argument('-p', '--path')
path_parser.add_argument('--load-all', dest='all', action='store_const', const=True, default=False)

path = Path( path_parser.parse_args().path )
print('Path to files: ' + str(path) + '\n')
load_all = path_parser.parse_args().all

csv_reader1 = csv_reader(path)

pir_types = ['PirF', 'PirR', 'PirF_filtrado', 'PirR_filtrado']
vcu_types = ['VCU_1']

data = {}

for pir in pir_types:
    data[pir] = PIR(csv_reader1, pir)
    if load_all:
        data[pir].verify_loaded()
for vcu in vcu_types:
    data[vcu] = MotorSpeed(csv_reader1)
    if load_all:
        data[vcu].verify_loaded()

plot_function = {'vs-time':plot_vs_time, 'Ratio':plot_ratio, 'Ratio histogram':plot_ratio_hist, 'Discrete FFT':plot_fft}
plots = [key for key in plot_function.keys()]
while(1):
    plot_types = receive_list('Plot options', 'Choose which plots you want', plots)
    length_plot_types = len(plot_types)

    if length_plot_types == 1:
        fig, ax = plt.subplots()
        name = plot_types[0]
        plot_function[name](data, ax)
    else:
        fig, ax = plt.subplots(nrows=len(plot_types))
        for index, name in enumerate(plot_types):
            plot_function[name](data, ax[index])

    plt.show()