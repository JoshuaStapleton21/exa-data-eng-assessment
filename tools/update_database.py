import os
import sys
sys.path.insert(1, '..')
import tools.misc as misc
import importlib
for k,v in list(sys.modules.items()):
    if k.startswith('tools'):
        importlib.reload(v)


def create_tables(patient_database_conn):
    '''
    Creates the tables in the patient database
    :param patient_database_conn: the connection to the patient database
    :return: None
    '''
    patient_table_fields = misc.get_patient_field_list()

    patient_database_cusor = patient_database_conn.cursor()
    patient_database_cusor.execute("CREATE TABLE PATIENT")
    
    patient_database_conn.close()



