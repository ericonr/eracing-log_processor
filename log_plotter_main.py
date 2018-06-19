#! /usr/bin/env python3

import argparse as arg
import click
import signal
from pathlib import Path

import matplotlib.pyplot as plt

from data_man.lists import *

from data_man.data_storage import PIR, MotorSpeed
from data_man.data_loaders import csv_reader

from plotters.plot_vs_time import plot_vs_time
from plotters.plot_ratio import plot_ratio, plot_ratio_hist
from plotters.plot_fft import plot_fft

def close(x, y):
    print("Bye, darling!")
    exit()
signal.signal(signal.SIGINT, close)

@click.command()
@click.option('--load-all/--load-none', default=False, help='Set if you wish to load all known files into memory.')
@click.argument('folder_path')
def cli(load_all, folder_path):
    """This application runs a command line interface for plotting relevant
    graphs using data from .csv files in FOLDER_PATH.
    """
    try:
        path = Path(folder_path)
    except:
        print('This is not a path.')
        exit()
        
    csv_reader1 = csv_reader(path)

    data = {}
    
    pir_types = ['PirF', 'PirR', 'PirF_filtrado', 'PirR_filtrado']
    vcu_types = ['VCU_1']
    
    for pir in pir_types:
        data[pir] = PIR(csv_reader1, pir_type=pir)
    for vcu in vcu_types:
        data[vcu] = MotorSpeed(csv_reader1)
    if load_all:
        for key in data.keys():
            data[key].verify_loaded()
    
    plot_function = {'vs-time':plot_vs_time, 'Ratio':plot_ratio, 'Ratio histogram':plot_ratio_hist, 'Discrete FFT':plot_fft}
    plots = [key for key in plot_function.keys()]
    while(1):
        plot_types = receive_list('\nPlot options', 'Choose which plots you want', plots)
        length_plot_types = len(plot_types)
    
        if length_plot_types == 1:
            fig, ax = plt.subplots()
            name = plot_types[0]
            plot_function[name](data, ax)
        else:
            fig, ax = plt.subplots(nrows=len(plot_types))
            for index, name in enumerate(plot_types):
                plot_function[name](data, ax[index])
    
        fig.show()
    

cli()