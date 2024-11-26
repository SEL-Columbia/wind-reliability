import h5py
import numpy as np
import pandas as pd
from scipy import stats

# Read the NOW23 h5 file in write mode
file = h5py.File(r'E:\\NOW23\\Mid_Atlantic_2015_160m.h5', 'r+')

# 