import argparse as arg
from pathlib import Path

from data_man.data_storage import PIR, MotorSpeed
from data_man.data_loaders import csv_reader

path_parser = arg.ArgumentParser(description='Select the path of the files to be processed: ')
path_parser.add_argument('-p', '--path')
path = Path( path_parser.parse_args().path )
print('Path to files: ' + str(path) + '\n')

csv_reader1 = csv_reader(path)

pir_types = ['PirF', 'PirR', 'PirF_filtrado', 'PirR_filtrado']
vcu_types = ['VCU_1']

data = {}
for pir in pir_types:
    data[pir] = PIR(csv_reader1, pir)
    data[pir].verify_loaded()
for vcu in vcu_types:
    data[vcu] = MotorSpeed(csv_reader1)
    data[vcu].verify_loaded()

