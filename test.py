import copy
import json
from jsonschema.validators import Draft4Validator
from pkg_resources import resource_string, resource_listdir, resource_isdir
import re
from unittest import TestCase

from examples import (
    SME_V5,
    SME_CONTACT_V3,
    ADDRESS_V1,
    PERSON_V1,
    FINANCE_NEED_V1,
    ENTITY_V1,
    ACTOR_V1_DIRECTOR_1,
    ACTOR_V1_DIRECTOR_2,
    ACTOR_V1_GUARANTOR,
    FINANCE_APPLICATION_V3,
)
from sme_finance_application_schema.translations import (
    sme_v5_and_contact_v3_to_finance_application_v3_translator,
    finance_application_v3_to_sme_v5,
    finance_application_v3_to_sme_contact_v3,
)


# The following are fields that do not appear in the objects when they are translated from finance_application_v3
UNTRANSLATED_SME_V5_FIELDS = [
    #To remove - no translation written
    'date_of_first_filed_accounts',
]
UNTRANSLATED_CONTACT_V3_FIELDS = [
    #Deprecated
    'county',
]


# The following are fields that do not appear in the objects when they are translated from sme_v5 / sme_contact_v3
UNTRANSLATED_ENTITY_V1_FIELDS = [
    # Not present in SME_V5
    'employees',
    'registration_date',
    'addresses',
    'free_form',
    # To remove - no translation written
    'date_of_first_filed_accounts',
]
UNTRANSLATED_FINANCE_APPLICATION_V3_FIELDS = [
    # Unsupported
    'actors',
]
UNTRANSLATED_PERSON_V1_FIELDS = [
    # Not present in SME_V5 or CONTACT_V3
    'date_of_birth'
]
UNTRANSLATED_FINANCE_NEED_V1_FIELDS = [
    # Not present in SME_V5
    'free_form',
    'property_ownership',
    'permission_for_development',
    'property_development_type',
    'property_work_started',
    'asset_type',
    'type_of_mortgage',
    'experience_in_development',
    'deposit',
    'vehicle_type',
    'type_of_property',
]
UNTRANSLATED_ADDRESS_V1_FIELDS = [
    # TODO - Translation is missing
    'locality_name',
]


def patch_store(store):
    for schema_name in ('entity_v1', 'person_v1', 'finance_need_v1', 'address_v1', 'actor_v1'):
        content = resource_string('sme_finance_application_schema', schema_name).decode()
        store['https://www.fundingoptions.com/schema/' + schema_name] = json.loads(content)

def _list_schema_names():
    package_name = 'sme_finance_application_schema'
    python_resource_re = re.compile(r'.*\.py[cod]?$')
    for filename in resource_listdir(package_name, ''):  # type: str
        if python_resource_re.match(filename):
            continue
        elif filename.startswith(('_','.')):  # we care not about hidden files
            continue
        elif resource_isdir(package_name, filename):  # we have no nesting
            continue
        yield filename


class TestJson(TestCase):
    def test_entity_json(self):
        for schema_name in _list_schema_names():
            with self.subTest(schema=schema_name):
                content = resource_string('sme_finance_application_schema', schema_name).decode()
                self.assertTrue(json.loads(content))


class TestSampleData(TestCase):
    def completion_of_data_subtest(self, data, schema_name):
        content = resource_string('sme_finance_application_schema', schema_name).decode()
        schema = json.loads(content)
        expected_fields = schema['properties'].keys()
        for field in expected_fields:
            with self.subTest(field=field):
                self.assertIn(field, data)


    def validity_of_data_subtest(self, data, schema_name):
        content = resource_string('sme_finance_application_schema', schema_name).decode()
        schema = json.loads(content)
        validator = Draft4Validator(schema)
        patch_store(validator.resolver.store)
        self.assertTrue(validator.is_valid(data))


    def test_sample_data_is_valid(self):
        self.validity_of_data_subtest(SME_V5,'sme_v5')
        self.validity_of_data_subtest(SME_CONTACT_V3,'sme_contact_v3')
        self.validity_of_data_subtest(FINANCE_APPLICATION_V3,'finance_application_v3')
        self.validity_of_data_subtest(FINANCE_NEED_V1,'finance_need_v1')
        self.validity_of_data_subtest(ENTITY_V1,'entity_v1')
        self.validity_of_data_subtest(PERSON_V1,'person_v1')
        self.validity_of_data_subtest(ADDRESS_V1,'address_v1')
        self.validity_of_data_subtest(ACTOR_V1_DIRECTOR_1,'actor_v1')
        self.validity_of_data_subtest(ACTOR_V1_DIRECTOR_2,'actor_v1')
        self.validity_of_data_subtest(ACTOR_V1_GUARANTOR,'actor_v1')


    def test_sample_data_is_complete(self):
        self.completion_of_data_subtest(SME_V5,'sme_v5')
        self.completion_of_data_subtest(SME_CONTACT_V3,'sme_contact_v3')
        self.completion_of_data_subtest(FINANCE_APPLICATION_V3,'finance_application_v3')
        self.completion_of_data_subtest(FINANCE_NEED_V1,'finance_need_v1')
        self.completion_of_data_subtest(ENTITY_V1,'entity_v1')
        self.completion_of_data_subtest(PERSON_V1,'person_v1')
        self.completion_of_data_subtest(ADDRESS_V1,'address_v1')
        self.completion_of_data_subtest(ACTOR_V1_DIRECTOR_1,'actor_v1')
        self.completion_of_data_subtest(ACTOR_V1_DIRECTOR_2,'actor_v1')
        self.completion_of_data_subtest(ACTOR_V1_GUARANTOR,'actor_v1')
        # TODO - test entity_address and actor_address structures


class TestTranslations(TestCase):
    def test_sme_v5_and_contact_v3_to_finance_application_v3(self):
        expected_finance_application_v3 = copy.deepcopy(FINANCE_APPLICATION_V3)
        for field in UNTRANSLATED_FINANCE_APPLICATION_V3_FIELDS:
            expected_finance_application_v3.pop(field)
        for field in UNTRANSLATED_ENTITY_V1_FIELDS:
            expected_finance_application_v3['requesting_entity'].pop(field)
        for field in UNTRANSLATED_PERSON_V1_FIELDS:
            expected_finance_application_v3['applicant'].pop(field)
        for field in UNTRANSLATED_FINANCE_NEED_V1_FIELDS:
            expected_finance_application_v3['finance_need'].pop(field)
        for field in UNTRANSLATED_ADDRESS_V1_FIELDS:
            expected_finance_application_v3['applicant']['addresses'][0]['address'].pop(field)

        translated_finance_application_v3 = sme_v5_and_contact_v3_to_finance_application_v3_translator(SME_V5, SME_CONTACT_V3)
        self.assertDictEqual(translated_finance_application_v3, expected_finance_application_v3)


    def test_finance_application_v3_to_sme_v5(self):
        expected_sme_v5 = copy.deepcopy(SME_V5)
        for field in UNTRANSLATED_SME_V5_FIELDS:
            expected_sme_v5.pop(field)

        translated_sme_v5 = finance_application_v3_to_sme_v5(FINANCE_APPLICATION_V3)
        self.assertDictEqual(translated_sme_v5, expected_sme_v5)


    def test_finance_application_v3_to_sme_contact_v3(self):
        expected_sme_contact_v3 = copy.deepcopy(SME_CONTACT_V3)
        for field in UNTRANSLATED_CONTACT_V3_FIELDS:
            expected_sme_contact_v3.pop(field)

        translated_sme_contact_v3 = finance_application_v3_to_sme_contact_v3(FINANCE_APPLICATION_V3)
        self.assertDictEqual(translated_sme_contact_v3, expected_sme_contact_v3)
