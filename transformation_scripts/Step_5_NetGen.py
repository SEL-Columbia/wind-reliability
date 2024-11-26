import h5py
import numpy as np
import os
import pandas as pd
from scipy import stats
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../utils')))
import print_dataset

# Open the the Climatological Seasonl Year file in write mode
file = h5py.File(r'E:\\NOW23\\Mid_Atlantic_160m_TPC.h5', 'r+')

# Get the shape of the original dataset
original_shape = file['Pgeneration'].shape

# Delete the existing 'draught' dataset if it exists
if 'NetGen' in file:
    del file['NetGen']

# Create a new dataset for the draught values with the same shape as the original dataset and dtype as float64
NetGen_dataset = file.create_dataset('NetGen', shape=original_shape, dtype=np.float64)

# Define the chunk size for the first dimension
chunk_size = 1000

# Loop through each chunk of the first dimension
for i in range(0, original_shape[0], chunk_size):
    # Calculate the end index for the current chunk
    end = min(i + chunk_size, original_shape[0])
    
    # Load the current chunk into memory
    chunk = file['Pgeneration'][i:end, :]
    
    # Calculate the draught values for the current chunk and write them to the new dataset
    NetGen_dataset[i:end, :] = chunk - 1
    
    # Print the update on the number of steps completed
    print(f"Steps {i+1}-{end} of {original_shape[0]} completed")

# Close the file
file.close()

# Print the dataset to verify the transformation
file = h5py.File(r'E:\\NOW23\\Mid_Atlantic_160m_TPC.h5', 'r')
print_dataset(file, 'NetGen', 0)