import os
import uuid
import itasca as it

from running_parameters import set_running_parameters, set_global_variables
from utils import ProjectConfig, LoadConfigFile

OUTPUT_FILE_NAME = 'summary.csv'
CONFIG_FILE_NAME = 'config.json'


def run(config_file: os.PathLike, output_folder: os.PathLike, file_name: os.PathLike) -> None:
    """
    Run the desired cases over geom.sav
    Stores a table with the summary of runs in FILE_NAME
    Stores the .sav files in each named folder
    """
    # Set a dictionary with all the global variables for the run 
    config_dict = LoadConfigFile(config_file=config_file)
    
    # Run the cases
    for density in config_dict['density']:
        for poisson in config_dict['poisson']:
            for young_modulus in config_dict['young_modulus_gpa']:
                # Model Name and Model Path
                model_name = uuid.uuid4().hex
                model_path = ProjectConfig.make_results_folder(parent=output_folder, results=model_name)
                
                # Load the geometry
                it.command("model restore 'geom.sav'")
                # Create dictionary with variables for the run and print this run summary
                parameters_dict = set_running_parameters(
                                    uuid=model_name,
                                    density=float(density),
                                    young_modulus=float(young_modulus)*1_000_000_000,
                                    poisson=float(poisson),
                                    file_name=file_name
                                    )
                # Set global variables in FLAC3D 
                set_global_variables(parameters_dict)
                # Run the case
                it.command("program call 'elastic_run.dat'")
                # Save it
                it.command(f"model save '{model_path}/{model_name}_elas.sav'")
    

if __name__ == '__main__':
    """
    Example script for running multiple FLAC3D models
    Takes as input 'geom.sav' which is the desired geometry with boundary conditions and gravity already set
    """
    
    # Avoid Python of losing its memory
    it.command("""
    python-reset-state false
    """)
    
    # Set the desired architecture
    output_folder = ProjectConfig(output_folder='sensitivity_analysis').make_output_folder()

    # Execute
    run(config_file=CONFIG_FILE_NAME, output_folder=output_folder, file_name=OUTPUT_FILE_NAME)