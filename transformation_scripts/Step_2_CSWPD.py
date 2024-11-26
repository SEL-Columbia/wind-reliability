import h5py
import numpy as np
import os
import pandas as pd
from scipy import stats
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../utils')))
import print_dataset



# Open the HDF5 file and call the print_dataset function
file = h5py.File(r'E:\\NOW23\\Mid_Atlantic_160m.h5', 'r')
print_dataset.print_dataset(file, 'CSWPD', 0)