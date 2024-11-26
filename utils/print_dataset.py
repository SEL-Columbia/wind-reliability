def print_dataset(file, dataset_name, timestamp=None):
    # Get the power_density values for the specified timestamp or all timestamps if not provided
    if timestamp is not None:
        dataset_values = file[dataset_name][timestamp]
    else:
        dataset_values = file[dataset_name][:]

    # Get the coordinates
    coordinates = file['coordinates'][:]

    # Ensure coordinates and dataset_values have the same length
    if len(coordinates) != len(dataset_values):
        raise ValueError("Coordinates and dataset values must have the same length")

    # Zip the coordinates and power_density_values together
    coordinates_power = list(zip(coordinates, dataset_values))

    # Print the coordinates and power_density_values
    for coordinate, dataset_value in coordinates_power:
        print(f'Coordinate: {coordinate}, {dataset_name}: {dataset_value}')
    
    file.close()