import h5py
import numpy as np
import os
import pandas as pd
from scipy import stats
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../utils')))
import print_dataset

# Open the HDF5 file in write mode
file = h5py.File(r'E:\\NOW23\\Mid_Atlantic_160m_TPC.h5', 'r+')

# Get the shape of the original dataset
original_shape = file['CSTPD'].shape

# Delete the existing 'average_CSWPD' dataset if it exists
if 'average_CSTPD' in file:
    del file['average_CSTPD']

# Create a new dataset for the average_CSWPD values with the same shape as the original dataset and dtype as float64
average_CSTPD_dataset = file.create_dataset('average_CSTPD', shape=(original_shape[1],), dtype=np.float64)

# Define the chunk size for the first dimension
chunk_size = 1000

# Initialize a numpy array to hold the sum of the chunks
sum_of_chunks = np.zeros((original_shape[1],), dtype=np.float64)

# Initialize a variable to hold the total number of values
total_values = 0

# Loop through each chunk of the first dimension
for i in range(0, original_shape[0], chunk_size):
    # Calculate the end index for the current chunk
    end = min(i + chunk_size, original_shape[0])
    
    # Load the current chunk into memory
    chunk = file['CSTPD'][i:end, :]
    
    # Add the chunk to the sum_of_chunks
    sum_of_chunks += np.sum(chunk, axis=0)
    
    # Update the total number of values
    total_values += chunk.shape[0]

    # Print the update on the number of steps completed
    print(f"Steps {i+1}-{end} of {original_shape[0]} completed")

# Calculate the average and write it to the new dataset
average_CSTPD_dataset[...] = sum_of_chunks / total_values

file.close()

# Print the dataset to verify the transformation
file = h5py.File(r'E:\\NOW23\\Mid_Atlantic_160m_TPC.h5', 'r')
print_dataset(file, 'average_CSTPD')