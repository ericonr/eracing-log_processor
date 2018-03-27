import numpy as np

def sanitize_array(array):
    array = np.array(array)
    array = array[np.isfinite(array)]
    array = array[np.logical_not(np.isnan(array))]
    array = array[np.nonzero(array)]
    return array

def filter_PIR(array):
    for index, element in enumerate(array):
        if element > 30000:
            array[index] = array[index-1]

    diff = np.diff(array)
    for index, element in enumerate(diff):
        if element > 83766:
            array[index] = array[index-1] + 83766
        elif element < -83766:
            array[index] = array[index-1] - 83766

    return array