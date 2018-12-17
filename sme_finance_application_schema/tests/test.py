import copy
import json
from jsonschema.validators import Draft4Validator
from pkg_resources import resource_string, resource_listdir, resource_isdir
import re
from unittest import TestCase


from .fixtures import (
    SME_V3,
    SME_V3_MISSING_INFORMATION,
    SME_V5,
    SME_CONTACT_V2,
    SME_CONTACT_V2_MISSING_INFORMATION,
    SME_CONTACT_V3,
    ADDRESS_V1,
    PERSON_V1,
    FINANCE_NEED_V1,
    ENTITY_V1,
    ACTOR_V1_DIRECTOR_1,
    ACTOR_V1_DIRECTOR_2,
    ACTOR_V1_GUARANTOR,
    FINANCE_APPLICATION_V3,
    AGGREGATED_ACTORS_V1,
    AGGREGATED_ACTORS_V1_INCOMPLETE,
    FINANCE_APPLICATION_V3_AGGREGATED_INCOMPLETE,
)
from sme_finance_application_schema.translations import (
    sme_v5_and_contact_v3_to_finance_application_v3_translator,
    finance_application_v3_to_sme_v5,
    finance_application_v3_to_sme_contact_v3,
    sme_v3_and_contact_v2_to_finance_application_v3_translator,
    sme_contact_v2_to_person_v1_translator,
    sme_contact_v2_telephone_to_e164_telephone,
)


# The following are fields that do not appear in the objects when they are translated from finance_application_v3
UNTRANSLATED_SME_V5_FIELDS = []
UNTRANSLATED_CONTACT_V3_FIELDS = [
    #Deprecated
    'county',
]


# The following are fields that do not appear in the objects when they are translated from sme_v3 / sme_contact_v2
UNTRANSLATED_FROM_SME_V3_CONTACT_V2_TO_ENTITY_V1_FIELDS = [
    # Not present in SME_V3
    'employees',
    'registration_date',
    'addresses',
    'free_form',
    'main_source_of_revenue',
    'accounting_software',
    'company_credit_rating',
    'count_of_all_ccjs',
    'count_of_invoiced_customers',
    'count_of_unsatisfied_ccjs',
    'exports',
    'outstanding_invoices',
    'purchase_orders',
    'sets_of_filed_accounts',
    'stock_imports',
    'total_value_of_unsatisfied_ccjs',
    'vat_number',
    'trading_startdate',
    'is_vat_registered'
]
UNTRANSLATED_FROM_SME_V3_CONTACT_V2_TO_FINANCE_APPLICATION_V3_FIELDS = [
    # Unsupported
    'actors',
]
UNTRANSLATED_FROM_SME_V3_CONTACT_V2_TO_PERSON_V1_FIELDS = [
    # Not present in SME_V3 or CONTACT_V2
    'date_of_birth',
    'applicant_role',
    'residential_status',
    'previous_address',
    'property_ownership',
    'property_value'
]
UNTRANSLATED_FROM_SME_V3_CONTACT_V2_TO_FINANCE_NEED_V1_FIELDS = [
    # Not present in SME_V3
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
    'guarantor_available',
    'main_source_of_revenue',
]
UNTRANSLATED_FROM_SME_V3_CONTACT_V2_TO_ADDRESS_V1_FIELDS = []
UNTRANSLATED_FROM_SME_V3_CONTACT_V2_TO_AGGREGATED_ACTORS_V1_FIELDS = [
    # Cannot generate from SME_V3
    'max_personal_credit_rating',
    'sum_outstanding_mortgage_on_property',
    'max_familiarity_with_financing',
    'min_personal_credit_rating',
]


# The following are fields that do not appear in the objects when they are translated from sme_v5 / sme_contact_v3
UNTRANSLATED_FROM_SME_V5_CONTACT_V3_TO_ENTITY_V1_FIELDS = [
    # Not present in SME_V5
    'employees',
    'registration_date',
    'addresses',
    'free_form',
    'main_source_of_revenue',
]
UNTRANSLATED_FROM_SME_V5_CONTACT_V3_TO_FINANCE_APPLICATION_V3_FIELDS = [
    # Unsupported
    'actors',
]
UNTRANSLATED_FROM_SME_V5_CONTACT_V3_TO_PERSON_V1_FIELDS = [
    # Not present in SME_V5 or CONTACT_V3
    'date_of_birth'
]
UNTRANSLATED_FROM_SME_V5_CONTACT_V3_TO_FINANCE_NEED_V1_FIELDS = [
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
    'main_source_of_revenue',
]
UNTRANSLATED_FROM_SME_V5_CONTACT_V3_TO_ADDRESS_V1_FIELDS = []
UNTRANSLATED_FROM_SME_V5_CONTACT_V3_TO_AGGREGATED_ACTORS_V1_FIELDS = [
    # Cannot generate from SME_v5
    'max_personal_credit_rating',
    'sum_outstanding_mortgage_on_property',
]


def patch_store(store):
    for schema_name in ('entity_v1', 'person_v1', 'finance_need_v1', 'address_v1', 'actor_v1', 'aggregated_actors_v1'):
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
        self.validity_of_data_subtest(SME_V3,'sme_v3')
        self.validity_of_data_subtest(SME_V3_MISSING_INFORMATION,'sme_v3')
        self.validity_of_data_subtest(SME_CONTACT_V2,'sme_contact_v2')
        self.validity_of_data_subtest(SME_CONTACT_V2_MISSING_INFORMATION,'sme_contact_v2')
        self.validity_of_data_subtest(SME_V5,'sme_v5')
        self.validity_of_data_subtest(SME_CONTACT_V3,'sme_contact_v3')
        self.validity_of_data_subtest(FINANCE_APPLICATION_V3,'finance_application_v3')
        self.validity_of_data_subtest(FINANCE_APPLICATION_V3_AGGREGATED_INCOMPLETE,'finance_application_v3')
        self.validity_of_data_subtest(FINANCE_NEED_V1,'finance_need_v1')
        self.validity_of_data_subtest(ENTITY_V1,'entity_v1')
        self.validity_of_data_subtest(PERSON_V1,'person_v1')
        self.validity_of_data_subtest(ADDRESS_V1,'address_v1')
        self.validity_of_data_subtest(ACTOR_V1_DIRECTOR_1,'actor_v1')
        self.validity_of_data_subtest(ACTOR_V1_DIRECTOR_2,'actor_v1')
        self.validity_of_data_subtest(ACTOR_V1_GUARANTOR,'actor_v1')
        self.validity_of_data_subtest(AGGREGATED_ACTORS_V1,'aggregated_actors_v1')
        self.validity_of_data_subtest(AGGREGATED_ACTORS_V1_INCOMPLETE,'aggregated_actors_v1')


    def test_sample_data_is_complete(self):
        self.completion_of_data_subtest(SME_V3,'sme_v3')
        self.completion_of_data_subtest(SME_CONTACT_V2,'sme_contact_v2')
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
        self.completion_of_data_subtest(AGGREGATED_ACTORS_V1,'aggregated_actors_v1')
        # TODO - test entity_address and actor_address structures


class TestTranslations(TestCase):
    def setUp(self):
        self.expected_finance_application_v3_from_sme_v3_and_contact_v2 = copy.deepcopy(FINANCE_APPLICATION_V3)
        for field in UNTRANSLATED_FROM_SME_V3_CONTACT_V2_TO_FINANCE_APPLICATION_V3_FIELDS:
            self.expected_finance_application_v3_from_sme_v3_and_contact_v2.pop(field)
        for field in UNTRANSLATED_FROM_SME_V3_CONTACT_V2_TO_ENTITY_V1_FIELDS:
            self.expected_finance_application_v3_from_sme_v3_and_contact_v2['requesting_entity'].pop(field)
        for field in UNTRANSLATED_FROM_SME_V3_CONTACT_V2_TO_PERSON_V1_FIELDS:
            self.expected_finance_application_v3_from_sme_v3_and_contact_v2['applicant'].pop(field)
        for field in UNTRANSLATED_FROM_SME_V3_CONTACT_V2_TO_FINANCE_NEED_V1_FIELDS:
            self.expected_finance_application_v3_from_sme_v3_and_contact_v2['finance_need'].pop(field)
        for field in UNTRANSLATED_FROM_SME_V3_CONTACT_V2_TO_ADDRESS_V1_FIELDS:
            self.expected_finance_application_v3_from_sme_v3_and_contact_v2['applicant']['addresses'][0]['address'].pop(field)
        for field in UNTRANSLATED_FROM_SME_V3_CONTACT_V2_TO_AGGREGATED_ACTORS_V1_FIELDS:
            self.expected_finance_application_v3_from_sme_v3_and_contact_v2['aggregated_actors'].pop(field)

        self.expected_finance_application_v3_from_sme_v5_and_contact_v3 = copy.deepcopy(FINANCE_APPLICATION_V3)
        for field in UNTRANSLATED_FROM_SME_V5_CONTACT_V3_TO_FINANCE_APPLICATION_V3_FIELDS:
            self.expected_finance_application_v3_from_sme_v5_and_contact_v3.pop(field)
        for field in UNTRANSLATED_FROM_SME_V5_CONTACT_V3_TO_ENTITY_V1_FIELDS:
            self.expected_finance_application_v3_from_sme_v5_and_contact_v3['requesting_entity'].pop(field)
        for field in UNTRANSLATED_FROM_SME_V5_CONTACT_V3_TO_PERSON_V1_FIELDS:
            self.expected_finance_application_v3_from_sme_v5_and_contact_v3['applicant'].pop(field)
        for field in UNTRANSLATED_FROM_SME_V5_CONTACT_V3_TO_FINANCE_NEED_V1_FIELDS:
            self.expected_finance_application_v3_from_sme_v5_and_contact_v3['finance_need'].pop(field)
        for field in UNTRANSLATED_FROM_SME_V5_CONTACT_V3_TO_ADDRESS_V1_FIELDS:
            self.expected_finance_application_v3_from_sme_v5_and_contact_v3['applicant']['addresses'][0]['address'].pop(field)
        for field in UNTRANSLATED_FROM_SME_V5_CONTACT_V3_TO_AGGREGATED_ACTORS_V1_FIELDS:
            self.expected_finance_application_v3_from_sme_v5_and_contact_v3['aggregated_actors'].pop(field)


    def test_sme_v5_and_contact_v3_to_finance_application_v3(self):
        translated_finance_application_v3 = sme_v5_and_contact_v3_to_finance_application_v3_translator(SME_V5, SME_CONTACT_V3)
        self.assertDictEqual(translated_finance_application_v3, self.expected_finance_application_v3_from_sme_v5_and_contact_v3)


    def test_finance_application_v3_to_sme_v5(self):
        expected_sme_v5 = copy.deepcopy(SME_V5)
        for field in UNTRANSLATED_SME_V5_FIELDS:
            expected_sme_v5.pop(field)

        translated_sme_v5 = finance_application_v3_to_sme_v5(FINANCE_APPLICATION_V3)
        self.assertDictEqual(translated_sme_v5, expected_sme_v5)

    def test_finance_application_v3_to_sme_v5_partial_aggregated(self):
        expected_sme_v5 = copy.deepcopy(SME_V5)
        expected_sme_v5.update({
            'familiarity_with_financing': 'expert',
        })
        translated_sme_v5 = finance_application_v3_to_sme_v5(FINANCE_APPLICATION_V3_AGGREGATED_INCOMPLETE)
        self.assertDictEqual(translated_sme_v5, expected_sme_v5)


    def test_finance_application_v3_to_sme_contact_v3_no_backfill(self):
        expected_sme_contact_v3 = copy.deepcopy(SME_CONTACT_V3)
        for field in UNTRANSLATED_CONTACT_V3_FIELDS:
            expected_sme_contact_v3.pop(field)

        translated_sme_contact_v3 = finance_application_v3_to_sme_contact_v3(FINANCE_APPLICATION_V3)
        self.assertDictEqual(translated_sme_contact_v3, expected_sme_contact_v3)


    def test_finance_application_v3_to_sme_contact_v3_with_backfill(self):
        expected_sme_contact_v3 = copy.deepcopy(SME_CONTACT_V3)
        expected_sme_contact_v3.pop('applicant_first_name')
        expected_sme_contact_v3.pop('applicant_surname')
        expected_sme_contact_v3.pop('sme_name')
        for field in UNTRANSLATED_CONTACT_V3_FIELDS:
            expected_sme_contact_v3.pop(field)

        finance_application_v3_with_backfilled_details = copy.deepcopy(FINANCE_APPLICATION_V3)
        backfill_value = 'Unknown'
        finance_application_v3_with_backfilled_details['applicant']['first_name'] = backfill_value
        finance_application_v3_with_backfilled_details['applicant']['surname'] = backfill_value
        finance_application_v3_with_backfilled_details['requesting_entity']['name'] = backfill_value
        translated_sme_contact_v3 = finance_application_v3_to_sme_contact_v3(finance_application_v3_with_backfilled_details, remove_backfilling=True)
        self.assertDictEqual(translated_sme_contact_v3, expected_sme_contact_v3)


    def test_sme_v3_and_contact_v2_to_finance_application_v3_no_backfill(self):
        translated_finance_application_v3 = sme_v3_and_contact_v2_to_finance_application_v3_translator(SME_V3, SME_CONTACT_V2)
        self.assertDictEqual(translated_finance_application_v3, self.expected_finance_application_v3_from_sme_v3_and_contact_v2)


    def test_sme_v3_and_contact_v2_to_finance_application_v3_with_backfill(self):
        translated_finance_application_v3 = sme_v3_and_contact_v2_to_finance_application_v3_translator(SME_V3_MISSING_INFORMATION, SME_CONTACT_V2_MISSING_INFORMATION)
        with self.assertRaises(AssertionError):
            self.assertDictEqual(translated_finance_application_v3, self.expected_finance_application_v3_from_sme_v3_and_contact_v2)

        expected_finance_application_v3 = copy.deepcopy(self.expected_finance_application_v3_from_sme_v3_and_contact_v2)
        expected_finance_application_v3['requesting_entity']['name'] = 'Unknown'
        expected_finance_application_v3['finance_need']['requested_amount'] = 0
        expected_finance_application_v3['applicant']['first_name'] = 'Unknown'
        expected_finance_application_v3['applicant']['surname'] = 'Unknown'
        translated_finance_application_v3 = sme_v3_and_contact_v2_to_finance_application_v3_translator(SME_V3_MISSING_INFORMATION, SME_CONTACT_V2_MISSING_INFORMATION, backfill_required_properties=True)
        self.assertDictEqual(translated_finance_application_v3, expected_finance_application_v3)


    def test_sme_v3_and_contact_v2_to_finance_application_v3_incorrect_months_revenue(self):
        sme_v3_with_incorrect_months_revenue = copy.deepcopy(SME_V3)
        sme_v3_with_incorrect_months_revenue.update({'months_revenue': 2000})
        expected_finance_application_v3 = copy.deepcopy(self.expected_finance_application_v3_from_sme_v3_and_contact_v2)
        expected_finance_application_v3['requesting_entity']['months_revenue'] = 1800
        translated_finance_application_v3 = sme_v3_and_contact_v2_to_finance_application_v3_translator(sme_v3_with_incorrect_months_revenue, SME_CONTACT_V2)
        self.assertDictEqual(translated_finance_application_v3, expected_finance_application_v3)


    def test_sme_v3_and_contact_v2_to_finance_application_v3_incorrect_legal_status(self):
        legal_status_mapping = {
            'partnership_less_than_5': 'partnership_less_than_equal_to_3',
            'partnership_more_than_4': 'partnership_greater_than_3'
        }
        for original_value, new_value in legal_status_mapping.items():
            with self.subTest(original_value=original_value, new_value=new_value):
                sme_v3_with_incorrect_legal_status = copy.deepcopy(SME_V3)
                sme_v3_with_incorrect_legal_status.update({'legal_status': original_value})
                expected_finance_application_v3 = copy.deepcopy(self.expected_finance_application_v3_from_sme_v3_and_contact_v2)
                expected_finance_application_v3['requesting_entity']['legal_status'] = new_value
                translated_finance_application_v3 = sme_v3_and_contact_v2_to_finance_application_v3_translator(sme_v3_with_incorrect_legal_status, SME_CONTACT_V2)
                self.assertDictEqual(translated_finance_application_v3, expected_finance_application_v3)


    def test_sme_contact_v2_to_person_v1_translator(self):
        sme_contact_v2_with_normal_phone_number = copy.deepcopy(SME_CONTACT_V2)
        sme_contact_v2_with_normal_phone_number['telephone'] = '07445387241'
        person_v1 = sme_contact_v2_to_person_v1_translator(sme_contact_v2_with_normal_phone_number)
        expected_person_v1 = copy.deepcopy(PERSON_V1)
        for field in UNTRANSLATED_FROM_SME_V3_CONTACT_V2_TO_PERSON_V1_FIELDS:
            expected_person_v1.pop(field)
        expected_person_v1['telephone'] = '7445387241'
        self.assertDictEqual(person_v1, expected_person_v1)


    def test_sme_contact_v2_telephone_to_e164_telephone(self):
        telephone = '  07736 936 496 '
        expected_telephone = '7736936496'
        translated_telephone = sme_contact_v2_telephone_to_e164_telephone(telephone)
        self.assertEqual(expected_telephone, translated_telephone)
        telephone = '+447736 936496'
        expected_telephone = '+447736936496'
        translated_telephone = sme_contact_v2_telephone_to_e164_telephone(telephone)
        self.assertEqual(expected_telephone, translated_telephone)

