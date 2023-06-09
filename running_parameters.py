import csv
import math
import os
import itasca as it
import numpy as np
from typing import List, Union, Dict


def write_summary(file_name: os.PathLike, variable_names: List[str], variable_values: List[Union[int, str, float]]) -> None:
    if not os.path.isfile(file_name):
        with open(file_name, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(variable_names)
            writer.writerow(variable_values)
    else:
        with open(file_name, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(variable_values)


def set_running_parameters(
        uuid: str, 
        density: float,
        young_modulus: float,
        poisson: float,
        file_name: os.PathLike
        ) -> Dict:
    """
    Function to set all the variables in FLAC3D
    It writes all the variables used into a csv
    """
    # Store variables / Write file
    variable_names = [
        'uuid',
        'density',
        'young_modulus',
        'poisson'
    ]
    
    variable_values = [
        uuid,
        density,
        young_modulus,
        poisson
    ]
    
    # Write variables
    write_summary(file_name=file_name, variable_names=variable_names, variable_values=variable_values)
    
    return {variable_names[i]: variable_values[i] for i in range(len(variable_values))}
    

def set_global_variables(parameters_dict: Dict) -> None:
    """
    Input:
    - parameters_dict: Dictionary with all the parameters for the run
    """
    # Set global variables for FISH
    for k, v in parameters_dict.items():
        if k != 'uuid':
            it.command(f"[global global_{k}={v}]")