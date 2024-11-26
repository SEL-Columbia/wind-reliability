import h5py
import numpy as np
import os
import pandas as pd
from scipy import stats
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../utils')))
import print_dataset

# Import the function from print_dataset.py

# Read the NOW23 h5 file in write mode
file = h5py.File(r'E:\\NOW23\\Mid_Atlantic_2015_160m.h5', 'r+')

# Fit a curve of the turbine power as a function of the wind speed
# Read the NREL example 15MW turbine power curve
turbine_curve = pd.read_csv('../data/2020ATB_NREL_Reference_15MW_240.csv')

# Filter the data to include only wind speeds between 4 and 11 m/s
mask = (turbine_curve['Wind Speed [m/s]'] >= 4) & (turbine_curve['Wind Speed [m/s]'] <= 11)
wind_speed_filtered = turbine_curve['Wind Speed [m/s]'][mask]
power_filtered = turbine_curve['Power [kW]'][mask]

# Fit a polynomial to the filtered data
degree = 2
coefficients = np.polyfit(wind_speed_filtered, power_filtered, degree)
polynomial = np.poly1d(coefficients)

# Define a function to calculate the power output based on wind speeds
def calculate_power(wind_speeds):
    """
    Calculate the power output based on wind speeds.
    
    Parameters:
    wind_speeds (array-like): Array of wind speeds.
    
    Returns:
    np.ndarray: Array of power outputs.
    """
    wind_speeds = np.array(wind_speeds)
    power_output = np.zeros_like(wind_speeds)
    
    # Apply the polynomial fit for wind speeds between 4 and 11 m/s
    mask_4_to_11 = (wind_speeds >= 4) & (wind_speeds <= 11)
    power_output[mask_4_to_11] = polynomial(wind_speeds[mask_4_to_11])
    
    # Set power to 0 for wind speeds less than 4 m/s
    mask_less_than_4 = wind_speeds < 4
    power_output[mask_less_than_4] = 0
    
    # Set power to 15000 for wind speeds between 11 and 25 m/s
    mask_11_to_25 = (wind_speeds > 11) & (wind_speeds <= 25)
    power_output[mask_11_to_25] = 15000

    power_output[wind_speeds > 25] = 0
    
    return power_output

# Calculate the store the power density values in a new dataset in the h5 file 
# We do this in chunks to avoid loading the entire dataset into memory at once

original_shape = file['windspeed_160m'].shape

# Delete the existing 'power_density' dataset if it exists
if 'turbine_power_density' in file:
    del file['turbine_power_density']

# Create a new dataset for the power_density values with the same shape as the original dataset and dtype as float64
power_density_dataset = file.create_dataset('turbine_power_density', shape=original_shape, dtype=np.float64)

# Define the chunk size for the first dimension
chunk_size = 1000

# Loop through each chunk of the first dimension
for i in range(0, original_shape[0], chunk_size):
    # Calculate the end index for the current chunk
    end = min(i + chunk_size, original_shape[0])
    
    # Load the current chunk into memory and calculate power density. 
    # The wind speed data is scaled by the scale factor attribute so we need to divide by it to get the values in m/s.
    chunk = calculate_power(file['windspeed_160m'][i:end, :] / file['windspeed_160m'].attrs['scale_factor'])
    
    # Print the chunk to track progress. This line can be commented out to speed up the process.
    print(f"Chunk {i+1}-{end}:\n{chunk}")
    
    # Write the power density chunk to the new dataset
    power_density_dataset[i:end, :] = chunk
    
    # Print the update on the number of steps completed
    print(f"Steps {i+1}-{end} of {original_shape[0]} completed")

file.close()

# Print the dataset to verify the transformation
file = h5py.File(r'E:\\NOW23\\Mid_Atlantic_2015_160m.h5', 'r')
print_dataset(file, 'turbine_power_density', 0)