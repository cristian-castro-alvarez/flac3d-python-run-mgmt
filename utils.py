import json
import os
from typing import Dict


class ProjectConfig():
    """
    Class that contains the structure of the project and creates folders for outputs
    """
    def __init__(self, input_folder: str = None, output_folder: str = None):
        self.cwd = os.getcwd()

        if input_folder is not None:
            self.input_folder = os.path.join(self.cwd, input_folder)

        if output_folder is not None:
            self.output_folder = os.path.join(self.cwd, output_folder)

    def make_input_folder(self):
        if not os.path.exists(self.input_folder):
            os.mkdir(self.input_folder)
        return self.input_folder

    def make_output_folder(self):
        if not os.path.exists(self.output_folder):
            os.mkdir(self.output_folder)
        return self.output_folder
    
    @staticmethod
    def make_results_folder(parent: os.PathLike, results: str):
        if not os.path.exists(os.path.join(parent, results)):
            os.mkdir(os.path.join(parent, results))
        return os.path.join(parent, results)


def LoadConfigFile(config_file: os.PathLike) -> Dict:
    """
    Takes a .json file and loads a config file in form of a dictionary
    """
    with open(config_file) as file:
        config_dict = json.load(file)
    return config_dict