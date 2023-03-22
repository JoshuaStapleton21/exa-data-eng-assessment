# this is a script to execute the pipeline based on the execute_pipeline notebook

import sys
sys.path.insert(1, '..')
import tools.read_data as rd
import tools.create_database as cd
import tools.update_database as ud
from sqlalchemy import text
import pandas as pd
import unittest
import time
import json
from tools.data_tests import TestFHIRData
from fhir.resources.patient import Patient
from fhir.resources.bundle import Bundle
import importlib
for k,v in list(sys.modules.items()):
    if k.startswith('tools'):
        importlib.reload(v)


# read in the json data using a generator method - usually slightly faster for larger datasets
patient_json_list = []
start = time.time()
for json_obj in rd.read_json_files('data'):
    patient_json_list.append(json_obj)
end = time.time()
print("Time taken to retrieve json objects using generator method:", end - start)


# read in the json data using a standard method - usually slightly slower for larger datasets
patient_json_list_alt = []
start = time.time()
patient_file_list = rd.get_file_list('data')
for json_obj in patient_file_list:
    patient_json_list_alt.append(rd.read_patient_file('data', json_obj))
end = time.time()
print("Time taken to retrieve json objects using standard method:", end - start)

# check the two different methods correctly calculated the same list
assert patient_json_list == patient_json_list_alt, "Two alternative methods of calculating the same FHIR data list have returned different results"


# run all tests on the incoming data
print("Running data tests")
test_runner = unittest.TextTestRunner()
for json_obj in patient_json_list:
    TestFHIRData.JSON_OBJ = json_obj
    test_suite = unittest.TestLoader().loadTestsFromTestCase(TestFHIRData)
    test_results = test_runner.run(test_suite)


print("Creating raw tabular dataset")
# write the raw tabular data to a csv file. This needs to be normalized and cleaned before it can be used for analysis.
FHIR_patient_object_list = [Patient.parse_obj(Bundle.parse_obj(patient_json).entry[0].resource) for patient_json in patient_json_list]
patient_df = rd.patients_to_dataframe(FHIR_patient_object_list).drop(columns=['resource_type']) # we can drop this column because it is constant by definition
print("Writing raw tabular data to csv file in 0NF format")
patient_df.to_csv('data_output/patient_data_tabular_raw.csv', index=False)


# 1NF normalization - each table cell should have a single value
# the columns in the dataframe in need of normalization are extension, address, maritalStatus, name, telecom, etc.
# a naive solution would be to explode the columns that are lists. This, however, tends to become monolithic, as the number of table rows grows exponentially.
print("Creating 1NF tabular dataset")
print("exploding column: extension")
patient_exploded_df = patient_df.explode('extension') # start by exploding extension - the first column of type list
for column in patient_df.columns.drop('extension'):
    if type(patient_df[column][0]) == list:
        print("exploding column: " + column)
        patient_exploded_df = patient_exploded_df.explode(column)

print("Writing tabular data to csv file in 1NF format")
patient_exploded_df.to_csv('data_output/1NF_data/patient_data_tabular.csv', index=False)

# 2NF normalization - create additional tables for initial table cells with multiple/list entires
# this is a more complex solution, but it is more scalable, easier to maintain, and there is less data redundancy
print("Creating 2NF tabular dataset")
patient_df_2NF = patient_df.copy()
for column in patient_df_2NF.columns:
    if type(patient_df_2NF[column][0]) == list:
        print("exploding column: " + column)
        patient_exploded_df = patient_df_2NF.explode(column)
        patient_df_2NF = patient_df_2NF.drop(columns=[column])

        # drop all columns from the exploded dataframe that are in the original dataframe except ID
        NF_columns = list(patient_df_2NF.columns)
        NF_columns.remove('id')
        patient_exploded_df.drop(columns=NF_columns, inplace=True)
        patient_exploded_df.to_csv('data_output/2NF_data/patient_data_tabular_' + column + '.csv', index=False)

# finally, write the original table with all multi-value columns removed to a csv file
print("Writing tabular data to csv file in 2NF format")
patient_df_2NF.to_csv('data_output/2NF_data/patient_data_tabular.csv', index=False)


# get/open the connection to the patient database
print("Creating patient database and relevant tables")
patient_database_conn = cd.connect_to_sqla_server()

# dropping tables if they already exist
patient_database_conn.execute(text("DROP TABLE IF EXISTS patient"))
patient_database_conn.execute(text("DROP TABLE IF EXISTS address"))
patient_database_conn.execute(text("DROP TABLE IF EXISTS communication"))
patient_database_conn.execute(text("DROP TABLE IF EXISTS extension"))
patient_database_conn.execute(text("DROP TABLE IF EXISTS identifier"))
patient_database_conn.execute(text("DROP TABLE IF EXISTS name"))
patient_database_conn.execute(text("DROP TABLE IF EXISTS telecom"))

# create the tables in the patient database with 2NF standards - these correspond to the csv files in the data_output 2NF folder generated in the previous steps
TWONF_CREATE_PATIENT_TABLE_SQL = """
        CREATE TABLE patient (
            fhir_comments string,
            id string,
            implicitRules string,
            implicitRules__ext string,
            language string,
            language__ext string,
            meta string,
            contained string,
            modifierExtension string,
            text string,
            active string,
            active__ext string,
            birthDate string,
            birthDate__ext string,
            contact string,
            deceasedBoolean string,
            deceasedBoolean__ext string,
            deceasedDateTime string,
            deceasedDateTime__ext string,
            gender string,
            gender__ext string,
            generalPractitioner string,
            link string,
            managingOrganization string,
            maritalStatus string,
            multipleBirthBoolean string,
            multipleBirthBoolean__ext string,
            multipleBirthInteger string,
            multipleBirthInteger__ext string,
            photo string
        );
    """

ud.execute_sql(TWONF_CREATE_PATIENT_TABLE_SQL, patient_database_conn)

# create the address table
TWONF_CREATE_ADDRESS_TABLE_SQL = """
    CREATE TABLE address (
        id bool,
        address string
    );
"""
ud.execute_sql(TWONF_CREATE_ADDRESS_TABLE_SQL, patient_database_conn)

# create the communication table
TWONF_CREATE_COMMUNICATION_TABLE_SQL = """
    CREATE TABLE communication (
        id string,
        communication string
    );
"""
ud.execute_sql(TWONF_CREATE_COMMUNICATION_TABLE_SQL, patient_database_conn)

# create the extension table
TWONF_CREATE_EXTENSION_TABLE_SQL = """
    CREATE TABLE extension (
        id string,
        extension string
    );
"""
ud.execute_sql(TWONF_CREATE_EXTENSION_TABLE_SQL, patient_database_conn)

# create the identifier table
TWONF_CREATE_IDENTIFIER_TABLE_SQL = """
    CREATE TABLE identifier (
        id string,
        identifier string
    );
"""
ud.execute_sql(TWONF_CREATE_IDENTIFIER_TABLE_SQL, patient_database_conn)

# create the name table
TWONF_CREATE_NAME_TABLE_SQL = """
    CREATE TABLE name (
        id string,
        name string
    );
"""
ud.execute_sql(TWONF_CREATE_NAME_TABLE_SQL, patient_database_conn)

# create the telecom table
TWONF_CREATE_TELECOM_TABLE_SQL = """
    CREATE TABLE telecom (
        id string, 
        telecom string
    );
"""
ud.execute_sql(TWONF_CREATE_TELECOM_TABLE_SQL, patient_database_conn)

# IMPORTANT:
# I decided to use the generic, more pythonic variable types for the database table fields (ie: string as opposed to VARCHAR).
# This is because I am not 100% sure what types of data will be coming in, and if FHIR data types map exactly to SQL data types.
# Once we have a stronger idea of the data types based on incoming data consistency, we can update the table fields to be more specific and SQL compliant.


# populate the main table
patient_df = pd.read_csv('data_output/2NF_data/patient_data_tabular.csv')
print("Writing 2NF tabular data to SQL database")

def replace_quotes(df): # this can mess up formatting
    """
    Replaces all instances of " with ' in all cells in a pandas DataFrame.
    """
    return df.applymap(lambda x: str(x).replace("\"", "'"))
patient_df = replace_quotes(patient_df)

for index, row in patient_df.iterrows():
    values = row.to_list()
    values_string = '\", \"'.join(values)
    values_string = '\"'+values_string+'\"'
    insert_sql = "INSERT INTO patient (fhir_comments, id, implicitRules, implicitRules__ext, language, language__ext, meta, contained, modifierExtension, text, active, active__ext, birthDate, birthDate__ext, contact, deceasedBoolean, deceasedBoolean__ext, deceasedDateTime, deceasedDateTime__ext, gender, gender__ext, generalPractitioner, link, managingOrganization, maritalStatus, multipleBirthBoolean, multipleBirthBoolean__ext, multipleBirthInteger, multipleBirthInteger__ext, photo) VALUES ("+values_string+")"
    patient_database_conn.execute(text(insert_sql))


# populate the sub tables
sub_table_list = rd.get_file_list('data_output/2NF_data')
sub_table_list.remove('patient_data_tabular.csv')
for table in sub_table_list: # populate all sub tables
    table_data = pd.read_csv('data_output/2NF_data/'+table)
    table_name = str(table_data.columns[1]) # same as the second column name
    for index, row in table_data.iterrows():
        patient_id = "\""+row['id']+"\""
        # enclose with double quotes to ensure it is recognized as a string
        value = "\""+row[table_name].replace("\"","'")+"\""
        insert_sql = "INSERT INTO "+table_name+" (id, "+table_name+") VALUES ({}, {})".format(patient_id, value)
        patient_database_conn.execute(text(insert_sql))


# example of how to query the database
print("Example 2NF tabulated dataset query")
result = patient_database_conn.execute(text("SELECT * FROM extension"))
df = pd.DataFrame(result.all(), columns=result.keys())
print(df)