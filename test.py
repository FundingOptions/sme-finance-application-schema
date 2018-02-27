import copy
import json
import jsonschema.validators
from unittest import TestCase

from examples import *
from pkg_resources import resource_filename
from sme_finance_application_schema.translations import *


# The following are fields that do not appear in the objects when they are translated from finance_application_v3
UNTRANSLATED_SME_V5_FIELDS = [
    'date_of_first_filed_accounts', #To remove - no translation written
]
UNTRANSLATED_CONTACT_V3_FIELDS = [
    'county', #Deprecated
]


# The following are fields that do not appear in the objects when they are translated from sme_v5 / sme_contact_v3
UNTRANSLATED_ENTITY_V1_FIELDS = [
    'employees', #Not present in SME_v5
    'registration_date', #Not present in SME_v5
    'addresses', #Not present in SME_v5
    'date_of_first_filed_accounts', #To remove - no translation written
    'free_form', #Not present in SME_v5
]
UNTRANSLATED_FINANCE_APPLICATION_V3_FIELDS = [
    'actors', #Unsupported
]
UNTRANSLATED_PERSON_V1_FIELDS = [
    'date_of_birth' #Not present in SME_V5 or CONTACT_V3
]
UNTRANSLATED_FINANCE_NEED_V1_FIELDS = [
    'free_form', #Not present in SME_v5
    'property_ownership', #Not present in SME_v5
    'permission_for_development', #Not present in SME_v5
    'property_development_type', #Not present in SME_v5
    'property_work_started', #Not present in SME_v5
    'asset_type', #Not present in SME_v5
    'type_of_mortgage', #Not present in SME_v5
    'experience_in_development', #Not present in SME_v5
    'deposit', #Not present in SME_v5
    'vehicle_type', #Not present in SME_v5
    'type_of_property', #Not present in SME_v5
]
UNTRANSLATED_ADDRESS_V1_FIELDS = [
    'locality_name', #TODO
]


def patch_store(store):
    for schema in ('entity_v1', 'person_v1', 'finance_need_v1', 'address_v1', 'actor_v1'):
        resource = resource_filename('sme_finance_application_schema', schema)
        with open(resource) as f:
            store['https://www.fundingoptions.com/schema/' + schema] = json.loads(f.read())


class TestJson(TestCase):
    def test_entity_json(self):
        for schema in ('entity_v1', 'person_v1', 'finance_need_v1', 'address_v1', 'finance_application_v1', 'finance_application_v2', 'finance_application_v3', 'batch_application_v1', 'batch_response_v1', 'actor_v1'):
            with self.subTest(schema=schema):
                resource = resource_filename('sme_finance_application_schema', schema)
                with open(resource) as f:
                    content = f.read()
                self.assertTrue(json.loads(content))


def test_validity_of_data(data, schema_name):
    resource = resource_filename('sme_finance_application_schema', schema_name)
    with open(resource) as f:
        schema = json.loads(f.read())
        validator = jsonschema.validators.Draft4Validator(schema)
        patch_store(validator.resolver.store)
        if not validator.is_valid(data):
            raise Exception('invalid data according to {}: {}'.format(schema_name, validator.validate(SME_V5)))


class TestTranslations(TestCase):
    def completion_of_data_subtest(self, data, schema_name):
        resource = resource_filename('sme_finance_application_schema', schema_name)
        with open(resource) as f:
            schema = json.loads(f.read())
            expected_fields = schema['properties'].keys()
            for field in expected_fields:
                with self.subTest(field=field):
                    self.assertIn(field, data)


    def validity_of_data_subtest(self, data, schema_name):
        resource = resource_filename('sme_finance_application_schema', schema_name)
        with open(resource) as f:
            schema = json.loads(f.read())
            validator = jsonschema.validators.Draft4Validator(schema)
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


    def test_sme_v5_and_contact_v3_to_finance_application_v3_translator(self):
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

        resource = resource_filename('sme_finance_application_schema', 'finance_application_v3')
        with open(resource) as f:
            content = f.read()
        json_content = json.loads(content)
        validator = jsonschema.validators.Draft4Validator(json_content)
        patch_store(validator.resolver.store)
        self.assertTrue(validator.is_valid(sme_v5_and_contact_v3_to_finance_application_v3_translator(SME_V5, SME_CONTACT_V3)))


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
