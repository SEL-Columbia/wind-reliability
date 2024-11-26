import h5py
import numpy as np
import os
import pandas as pd
from scipy import stats
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../utils')))
import print_dataset

# Open the Climatological Seasonl Year in write mode
file = h5py.File(r'E:\\NOW23\\Mid_Atlantic_160m_TPC.h5', 'r+')

# Get the shape of the original dataset
original_shape = file['CSTPD'].shape

# Delete the existing 'Pgeneration' dataset if it exists
if 'Pgeneration' in file:
    del file['Pgeneration']

# Create a new dataset for the Pgeneration values with the same shape as the original dataset and dtype as float64
pgeneration_dataset = file.create_dataset('Pgeneration', shape=original_shape, dtype=np.float64)

# Define the chunk size for the first dimension
chunk_size = 1000

# Load the average_CSWPD values into memory
average_CSWPD = file['average_CSTPD'][:]

# Loop through each chunk of the first dimension
for i in range(0, original_shape[0], chunk_size):
    # Calculate the end index for the current chunk
    end = min(i + chunk_size, original_shape[0])
    
    # Load the current chunk into memory
    chunk = file['CSTPD'][i:end, :]
    
    # Calculate the Pgeneration values for the current chunk and write them to the new dataset
    pgeneration_dataset[i:end, :] = chunk / average_CSWPD
    
    # Print the update on the number of steps completed
    print(f"Steps {i+1}-{end} of {original_shape[0]} completed")

# Close the file
file.close()

# Print the dataset to verify the transformation
file = h5py.File(r'E:\\NOW23\\Mid_Atlantic_160m_TPC.h5', 'r')
print_dataset.print_dataset(file, 'Pgeneration', 0)