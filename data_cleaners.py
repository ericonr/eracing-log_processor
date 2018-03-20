import numpy as np
import pandas as pd

def sanitize_array(array):
    array = np.array(array)
    array = array[np.isfinite(array)]
    array = array[np.logical_not(np.isnan(array))]
    array = array[np.nonzero(array)]
    return array