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

# Get the stored_energy dataset
stored_energy_dataset = file['stored_energy']

# Get the shape of the dataset
shape = stored_energy_dataset.shape

# Initialize an empty list to store the max_deficit for each coordinate
energy_deficit_w = []

# Define the size of the chunks
chunk_size = 1000  # Adjust this value based on the size of your GPU's memory

# Loop through all the coordinates in chunks
for i in range(0, shape[1], chunk_size):
    print(f"\rProcessing coordinates {i+1} to {min(i+chunk_size, shape[1])} of {shape[1]}", end="")

    # Load the current chunk into the GPU's memory
    stored_energy_chunk = cp.asarray(stored_energy_dataset[:, i:i+chunk_size])

    # Loop through all the coordinates in the current chunk
    for j in range(stored_energy_chunk.shape[1]):
        # Create an array of all the stored_energy values for the current coordinate
        stored_energy_current_coordinate = stored_energy_chunk[:, j]

        # Calculate the first derivative of the array
        derivative = cp.diff(stored_energy_current_coordinate)

        # Identify where the derivative changes sign
        sign_changes = cp.diff(cp.sign(derivative))

        # Local maxima occur where the derivative changes from positive to negative
        local_maxima = cp.where(sign_changes == -2)[0] + 1

        # Local minima occur where the derivative changes from negative to positive
        local_minima = cp.where(sign_changes == 2)[0] + 1

        # Get the values at the local maxima and minima
        local_maxima_values = stored_energy_current_coordinate[local_maxima]
        local_minima_values = stored_energy_current_coordinate[local_minima]

        if len(local_maxima_values) > len(local_minima_values):
            local_maxima_values = local_maxima_values[:-1]
        elif len(local_maxima_values) < len(local_minima_values):
            local_minima_values = local_minima_values[1:]

        # Calculate the differences between local_maxima_values and local_minima_values but ignore the last local_maxima_values value
        differences = local_maxima_values - local_minima_values
        max_deficit = cp.max(differences)

        # Append the max_deficit to the list
        energy_deficit_w.append(max_deficit)
        print(f"\rMax deficit for coordinate {i+j+1}: {max_deficit}")

# Convert the list to a numpy array
energy_deficit_w_array = np.array([item.item() for item in energy_deficit_w])

# Create a new dataset in the file for the max_deficit
file.create_dataset('energy_deficit_w', data=energy_deficit_w_array)

# Close the file
file.close()

# Print the dataset to verify the transformation
file = h5py.File(r'E:\\NOW23\\Mid_Atlantic_160m_TPC.h5', 'r')
print_dataset(file, 'energy_deficit')

# Converting the energy_deficit dataset to percentile
file = h5py.File(r'E:\\NOW23\\Mid_Atlantic_160m_TPC.h5', 'r+')

original_shape = file['energy_deficit'].shape

# Delete the existing 'energy_deficit' dataset if it exists
if 'percentile_rank_of_seasonal_variability' in file:
    del file['percentile_rank_of_seasonal_variability']

energy_deficit_data = file['energy_deficit'][:]

percentile_rank_of_seasonal_variability = file.create_dataset('percentile_rank_of_seasonal_variability', data = stats.rankdata(-energy_deficit_data, nan_policy='omit')*100/original_shape[0])

file.close()

# Print the dataset to verify the transformation
file = h5py.File(r'E:\\NOW23\\Mid_Atlantic_160m.h5', 'r')
print_dataset(file, 'percentile_rank_of_seasonal_variability')