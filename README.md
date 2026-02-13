# wind-reliability

Repository for the "A Combined Capacity Factor-Reliability Framework for Offshore Wind Siting: A Case Study in the U.S. Mid-Atlantic Region" paper. 
Corresponding author: Jiarong Xie, jx2543@columbia.edu

## Overview

This repository contains code and results in the aforementioned paper. It includes the transformation of data needed to calculate the values of abundance and reliability metric as well as the visualization of the results with the methods used for identifying the locations of various wind behavior that are used as inputs for the New York State capacity expansion model sectr-ny. 

The scripts reads the geospatial and temporal h5 files published by NREL under the dataset NOW-23: https://data.openei.org/submissions/4500. Our paper mainly focus on the Mid-Atlantic Region at 160m height, but the script should be able to work with all regions and altitude. The dataset are in 5-minute intervals with grid cells in 2 by 2 km resolution. Due to the size of eahc file, (~ 100+ GB), and the number of available files (21 years), they are not uploaded in this GitHub page. 

The transformation scripts calculates the abundance by fitting all the windspeed data into a turbine power curve (TPC), provided by NREL: https://nrel.github.io/turbine-models/2020ATB_NREL_Reference_15MW_240.html#link-to-tabular-data and calculate the 21-year capacity factor for each location before ranking them. The details to how the reliability values were calculated are provided in the paper. Step 7 in the transformation scripts utilized the `cupy` package to efficiently calculate the maximum differences in all the local minima and maxima pairs in the climatological year and require the installment of the NVIDIA CUDA software to run. For machines without the NVIDIA GPUs or are unable to install CUDA, the `cupy` code could be alternatively modified to be ran with `numpy`. The runtime could might increase as a result.

## Repository Strucuture

```
wind-reliability
├── README.md
├── setup.py
├── data/
├── data_visualization.ipynb
├── transformation_scripts/
│   ├── 
├── utils
│   ├── print_dataset.py
```
