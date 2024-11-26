import h5py
import numpy as np
import os
import pandas as pd
from scipy import stats
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../utils')))
import print_dataset

# Create an 'average year' or a 'climatological seasonal year' by averaging the wind speed of the same timestep of all the years
# We could create a new h5 file or overwrite the existing one, as long as the coordinate dataset and the time_index dataset are copied

# Open the HDF5 file in write mode
file = h5py.File(r'E:\\NOW23\\Mid_Atlantic_160m_TPC.h5', 'r+')

# Open 21 years of data in read mode
files = []
for year in range(2000, 2021):
    file_path = f'E:\\NOW23\\Mid_Atlantic_{year}_160m.h5'
    files.append(h5py.File(file_path, 'r'))

# Average the 21 years of data

original_shape = file_2000['windspeed_160m'].shape

# Delete the existing 'CSTPD' dataset if it exists
if 'CSTPD' in file:
    del file['CSTPD']

# Create a new dataset for the CSTPD values with the same shape as the original dataset and dtype as float64
CSTPD_dataset = file.create_dataset('CSTPD', shape=original_shape, dtype=np.float64)

# Define the chunk size for the first dimension
chunk_size = 1000

# Loop through each chunk of the first dimension
for i in range(0, original_shape[0], chunk_size):
    # Calculate the end index for the current chunk
    end = min(i + chunk_size, original_shape[0])
    
    # Load the current chunk into memory and calculate average
    chunks = [files[year - 2000]['turbine_power_density'][i:end, :] for year in range(2000, 2021)]
    average_chunk = np.mean(chunks, axis=0)
    
    # Write the average chunk to the new dataset
    CSTPD_dataset[i:end, :] = average_chunk
    
    # Print the update on the number of steps completed
    print(f"Steps {i+1}-{end} of {original_shape[0]} completed")

# Close the file
file.close()

# Print the dataset to verify the transformation
file = h5py.File(r'E:\\NOW23\\Mid_Atlantic_160m.h5', 'r')
print_dataset.print_dataset(file, 'CSTPD', 0)