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
original_shape = file['NetGen'].shape

# Delete the existing 'stored_energy' dataset if it exists
if 'stored_energy' in file:
    del file['stored_energy']

# Create a new dataset for the stored_energy values with the same shape as the original dataset and dtype as float64
stored_energy_dataset = file.create_dataset('stored_energy', shape=original_shape, dtype=np.float64)

# Define the chunk size for the first dimension
chunk_size = 1

# Initialize a numpy array to hold the previous chunk
previous_chunk = np.zeros((chunk_size, original_shape[1]), dtype=np.float64)

# Loop through each chunk of the first dimension
for i in range(0, original_shape[0], chunk_size):
    # Calculate the end index for the current chunk
    end = min(i + chunk_size, original_shape[0])
    
    # Load the current chunk into memory
    current_chunk = file['NetGen'][i:end, :]
    
    # Add the previous chunk to the current chunk
    current_chunk += previous_chunk[:end-i, :]
    
    # Store the current chunk in the dataset
    stored_energy_dataset[i:end, :] = current_chunk
    
    # Update the previous chunk
    previous_chunk = current_chunk

    # Print the update on the number of steps completed
    print(f"Steps {i+1}-{end} of {original_shape[0]} completed")

file.close()

# Print the dataset to verify the transformation
file = h5py.File(r'E:\\NOW23\\Mid_Atlantic_160m_TPC.h5', 'r')
print_dataset(file, 'stored_energy', 0)