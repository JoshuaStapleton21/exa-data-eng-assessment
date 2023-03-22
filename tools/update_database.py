import os
import sys
sys.path.insert(1, '..')
import importlib
for k,v in list(sys.modules.items()):
    if k.startswith('tools'):
        importlib.reload(v)


def create_tables(patient_database_conn):
    patient_database_cusor = patient_database_conn.cursor()

    # create patient table based on list of 
    ['resource_type', 'fhir_comments', 'id', 'implicitRules', 'implicitRules__ext', 'language', 'language__ext', 'meta', 'contained', 'extension', 'modifierExtension', 'text', 'active', 'active__ext', 'address', 'birthDate', 'birthDate__ext', 'communication', 'contact', 'deceasedBoolean', 'deceasedBoolean__ext', 'deceasedDateTime', 'deceasedDateTime__ext', 'gender', 'gender__ext', 'generalPractitioner', 'identifier', 'link', 'managingOrganization', 'maritalStatus', 'multipleBirthBoolean', 'multipleBirthBoolean__ext', 'multipleBirthInteger', 'multipleBirthInteger__ext', 'name', 'photo', 'telecom']

    patient_database_cusor.execute("CREATE TABLE PATIENT")
    
    patient_database_conn.close()