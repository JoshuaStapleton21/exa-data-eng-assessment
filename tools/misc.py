import sys
sys.path.insert(1, '..')
import json
from fhir.resources.bundle import Bundle
from fhir.resources.patient import Patient
import importlib
for k,v in list(sys.modules.items()):
    if k.startswith('tools'):
        importlib.reload(v)


def get_example_patient_object():
    '''
    Returns an example FHIR patient object
    :return: a FHIR patient object
    '''
    # read in an example FHIR patient data file.
    with open('data/Aaron697_Jerde200_6fa23508-960e-ff22-c3d0-0519a036543b.json') as f:
        bundle_json = json.load(f)
    bundle = Bundle.parse_obj(bundle_json)
    return Patient.parse_obj(bundle.entry[0].resource)


def get_patient_field_list():
    '''
    Returns a list of all the fields in a FHIR patient object
    :return: a list of all the fields in a FHIR patient object
    '''
    patient = get_example_patient_object() # we have established in EDA that the field list is the same for all patients, so getting a field list from one patient is sufficient.
    patient_field_list = [field for field, value in patient]
    return patient_field_list