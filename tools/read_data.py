import os
import sys
sys.path.insert(1, '..')
import pandas as pd
import json
import importlib
for k,v in list(sys.modules.items()):
    if k.startswith('tools'):
        importlib.reload(v)


def get_patient_file_list(directory:str):
    '''
    Returns a list of all the patient files in the directory
    :param directory: the directory to search
    :return: a str list of all the patient files in the directory
    '''
    patient_file_list = []
    try:
        for (dirpath, dirnames, filenames) in os.walk(directory):
            patient_file_list.extend(filenames)
        return patient_file_list
    except:
        print("Error: Could not find directory")


def read_patient_file(directory:str, filename:str):
    '''
    Reads a .json patient file and returns a dictionary
    :param directory: the directory to search
    :param filename: the filename to read
    :return: a dictionary of the patient file
    '''
    try:
        with open(os.path.join(directory, filename)) as f:
            data = json.load(f)
        return data
    except:
        print("Error: Could not read file - please pass a different directory or filename")


# use this for larger datasets as it is faster
def read_json_files(directory:str):
    """
    A generator function that reads and yields JSON files in a directory.
    :param directory: The directory containing the JSON files.
    :yield: A dictionary representing the contents of a JSON file.
    """
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if filename.endswith('.json') and os.path.isfile(filepath):
            with open(filepath, 'r') as file:
                yield json.load(file)

