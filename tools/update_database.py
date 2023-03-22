import sys
sys.path.insert(1, '..')
from sqlalchemy import text
import importlib
for k,v in list(sys.modules.items()):
    if k.startswith('tools'):
        importlib.reload(v)


def execute_sql(SQL_CREATE_COMMAND:str, patient_database_conn) -> bool:
    '''
    Executes commands in the SQL database
    :param patient_database_conn: the connection to the patient database
    :return: True if the operation succeeded
    '''
    try:
        patient_database_conn.execute(text(SQL_CREATE_COMMAND))
        return True
    except Exception as e:
        print("Error: Could not execute command. {}".format(e))
        return False
