import unittest
import importlib
import sys
from fhir.resources.bundle import Bundle
for k,v in list(sys.modules.items()):
    if k.startswith('tools'):
        importlib.reload(v)


class TestFHIRData(unittest.TestCase):
    JSON_OBJ = None

    def test_patient_is_first_entry_in_list(self):
        if self.JSON_OBJ['entry'][0]['resource']['resourceType'] != "Patient":
            self.assertEqual(self.JSON_OBJ['entry'][0]['resource']['resourceType'], "Patient", msg="Patient object not first in entry list")

    
    def test_json_obj_is_fhir_bundle(self):
        try:
            Bundle.parse_obj(self.JSON_OBJ)
        except:
            self.fail("JSON object is not a FHIR Bundle")


    def test_only_one_patient_field_per_bundle(self):
        # Loop through each entry in the bundle and count patient fields
        for entry in self.JSON_OBJ['entry']:
            if 'resource' in entry and entry['resource']['resourceType'] == 'Patient':
                patient_count = 1
                for sub_entry in self.JSON_OBJ['entry']:
                    if 'resource' in sub_entry and sub_entry['resource']['resourceType'] == 'Patient' and sub_entry['resource']['id'] != entry['resource']['id']:
                        patient_count += 1
                # fail the test if more than one patient field is found
                self.assertEqual(patient_count, 1, msg="Multiple patient fields found in bundle")


    def test_all_fields_in_patient(self):
        expected_fields = ['resourceType', 'fhir_comments', 'id', 'implicitRules', 'implicitRules__ext', 'language', 'language__ext', 'meta', 'contained', 'extension', 'modifierExtension', 'text', 'active', 'active__ext', 'address', 'birthDate', 'birthDate__ext', 'communication', 'contact', 'deceasedBoolean', 'deceasedBoolean__ext', 'deceasedDateTime', 'deceasedDateTime__ext', 'gender', 'gender__ext', 'generalPractitioner', 'identifier', 'link', 'managingOrganization', 'maritalStatus', 'multipleBirthBoolean', 'multipleBirthBoolean__ext', 'multipleBirthInteger', 'multipleBirthInteger__ext', 'name', 'photo', 'telecom']

        # Check that all fields in patient object are in the expected list
        for field in self.JSON_OBJ['entry'][0]['resource']:
            # fail the test if a field is not found in the expected field list
            self.assertIn(field, expected_fields, msg=f"{field} field not found in expected fields list")


if __name__ == '__main__':
    unittest.main()
