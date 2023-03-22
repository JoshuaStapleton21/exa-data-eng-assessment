import os
import sys
sys.path.insert(1, '..')
import pandas as pd
import json
import importlib
import requests
import tools.misc as misc
for k,v in list(sys.modules.items()):
    if k.startswith('tools'):
        importlib.reload(v)


def get_file_list(directory:str):
    '''
    Returns a list of all files in a directory
    :param directory: the directory to search
    :return: a str list of all the files in the directory
    '''
    file_list = []
    try:
        for (dirpath, dirnames, filenames) in os.walk(directory):
            file_list.extend(filenames)
        return file_list
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
    try:
        for filename in os.listdir(directory):
            filepath = os.path.join(directory, filename)
            if filename.endswith('.json') and os.path.isfile(filepath):
                with open(filepath, 'r') as file:
                    yield json.load(file)
    except:
        print("Error: Could not read file - please pass a different directory or filename")


# we also need to be able to read from an API if this is how the data is being sent - although this is not particularly secure
def get_json_objects_from_API(url:str):
    '''
    Queries a given API / URL and returns a list of JSON objects
    :param url: the API / URL to query
    :return: a list of JSON objects
    '''
    response = requests.get(url)
    if response.status_code == 200:
        json_data = response.json()
        return json_data
    else:
        print(f"Error: {response.status_code} - {response.reason}")


def patients_to_dataframe(patients:list):
    """
    Converts a list of FHIR Patient objects to a pandas dataframe.
    :param patients: a list of FHIR Patient objects
    :return: a pandas dataframe
    """
    columns = misc.get_patient_field_list()
    data = []

    for patient in patients:
        row = []
        for attr in columns:
            if hasattr(patient, attr):
                value = getattr(patient, attr)
                if isinstance(value, list):
                    value = [str(item) if not isinstance(item, (int, float, bool)) else item for item in value]
                elif not isinstance(value, (int, float, bool)):
                    value = str(value)
                row.append(value)
            else:
                row.append(None)
        data.append(row)

    patient_df = pd.DataFrame(data, columns=columns)
    return patient_df