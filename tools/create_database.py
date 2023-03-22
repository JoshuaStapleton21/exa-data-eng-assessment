import os
import sys
sys.path.insert(1, '..')
from sqlalchemy import create_engine
import importlib
for k,v in list(sys.modules.items()):
    if k.startswith('tools'):
        importlib.reload(v)


# use the dotenv framework to securely store credentials as environment variables
from dotenv import load_dotenv
load_dotenv()
HOST = os.environ.get('host')
USER = os.environ.get('user')
ENGINE = create_engine("{}://{}:".format(HOST, USER), echo=False) # change to true for verbose output


# create and connect to a a basic in-memory sqla database using the login credentials
def connect_to_sqla_server():
    """
    Creates and connects to a SQLAlchemy server
    :return: an sqla engine connection
    """
    return ENGINE.connect()