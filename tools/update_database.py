import os
import sys
sys.path.insert(1, '..')
import tools.misc as misc
import importlib
for k,v in list(sys.modules.items()):
    if k.startswith('tools'):
        importlib.reload(v)


def create_table(SQL_CREATE_COMMAND:str, patient_database_conn) -> bool:
    '''
    Creates the tables in the patient database
    :param patient_database_conn: the connection to the patient database
    :return: True if the operation succeeded
    '''
    patient_database_cusor = patient_database_conn.cursor()
    try:
        patient_database_cusor.execute(SQL_CREATE_COMMAND)
        return True
    except:
        print("Error: Could not create patient table.")
        return False


def write_patient_data(SQL_INSERT_COMMAND:str, patient_database_conn) -> bool:
    '''
    Writes the patient data into the patient table
    :param patient_database_conn: the connection to the patient database
    :param patient_data: the patient data
    :return: True if the operation succeeded
    '''
    patient_database_cusor = patient_database_conn.cursor()
    try:
        patient_database_cusor.execute(SQL_INSERT_COMMAND)
        return True
    except:
        print("Error: Could not create patient table.")
        return False

