import os
import sys
sys.path.insert(1, '..')
import mysql.connector
import importlib
for k,v in list(sys.modules.items()):
    if k.startswith('tools'):
        importlib.reload(v)

# use the dotenv framework to securely store credentials as environment variables
from dotenv import load_dotenv
load_dotenv()
HOST = os.environ.get('host')
USER = os.environ.get('user')
PASSWORD = os.environ.get('password')
DATABASE = os.environ.get('database')


def connect_to_mysql_server():
    """
    Connects to a MySQL server
    :return: a mysql connection object
    """
    connection = mysql.connector.connect(
        host=HOST,
        user=USER,
        password=PASSWORD
    )
    return connection


def connect_to_patient_database(): 
    """
    Connects to the MySQL patient database
    :return: a mysql connection object
    """
    try:
        connection = mysql.connector.connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            database=DATABASE
        )   
        return connection
    except:
        print("Error: Could not connect to database. The connection strings are invalid")
        return False


def create_patient_database():
    """
    Creates a MySQL patient database if it does not exist.
    :return: a mysql connection object for the patient database
    """
    mysql_server_connection = connect_to_mysql_server()
    mysql_server_cursor = mysql_server_connection.cursor()
    mysql_server_cursor.execute("CREATE DATABASE IF NOT EXISTS {}".format(DATABASE))
    mysql_server_connection.commit()
    mysql_server_connection.close()

    return connect_to_patient_database()