from unittest import TestCase
import json
import jsonschema.validators
import copy

SME_V5 = {
    'legal_status': 'limited_company',
    'finance_term_length': 30,
    'purpose': 'stock',
    'months_revenue': 0,
    'requested_amount': 3000,
    'date_finance_requested': '2017-01-23T00:00:00+00:00',
    'date_finance_required': '2018-01-23T00:00:00+00:00',
    'trade_credit': 0,
    'revenue': 2000,
    'sic_code': 'A',
    'card_revenue':3000,
    'financial_forecast':True,
    'finance_type_requested':'term_loan',
    'revenue_growth':50,
    'purchase_orders':50,
    'guarantor_available':True,
    'directors_pensions':5000,
    'registered_brand':True,
    'familiarity_with_financing':'first_time',
    'stock_imports':50,
    'customers':100,
    'business_plan':True,
    'stock_ready':50,
    'business_premises':50000,
    'business_assets':30000,
    'region':'UKZ',
    'intellectual_property':True,
    'accounting_software':'xero',
    'overseas_revenue':50,
    'online_revenue':50,
    'company_credit_rating':'ok',
    'personal_credit_ratings':'ok',
    'directors_houses':100000,
    'exports':True,
    'total_value_of_unsatisfied_ccjs':1000,
    'profitability':50,
    'institutional_revenue':50,
    'up_to_date_accounts':True,
    'date_of_first_filed_accounts': '2015-01-23T00:00:00+00:00',
    'count_of_invoiced_customers': 100,
    'outstanding_invoices': 1000,
}

SME_CONTACT_V3 = {
    'applicant_title': 'Mr',
    'applicant_first_name': 'Dave',
    'applicant_surname': 'dd',
    'telephone': '+447445387241',
    'sme_name': 'ddsaasd',
    'email': 'nestor.arocha@fundingoptions.com',
    'company_number': '123456',
    'address_line_1': '30 Great Guildford Street',
    'address_line_2': 'Derp',
    'postcode': 'SE1 0HS',
    'city': 'London',
    'county': 'London',
}

ADDRESS_V1 = {
    'building_number_and_street_name': '30 Great Guildford Street',
    'locality_name': 'Derp',
    'post_town': 'London',
    'postcode': 'SE1 0HS',
}

PERSON_V1 = {
    'title': 'Mr',
    'first_name': 'Dave',
    'surname': 'dd',
    'telephone':'+447445387241',
    'email': 'nestor.arocha@fundingoptions.com',
    'date_of_birth': '2000-01-23T00:00:00+00:00',
    'addresses': [{
        'address':ADDRESS_V1
    }]
}

FINANCE_NEED_V1 = {
    'finance_term_length': 30,
    'purpose': 'stock',
    'date_finance_requested': '2017-01-23T00:00:00+00:00',
    'date_finance_required': '2018-01-23T00:00:00+00:00',
    'requested_amount': 3000,
    'finance_type_requested':'term_loan',
    'guarantor_available':True,
    'free_form': 'A string',
    'property_ownership': 'yes_with_mortgage',
    'permission_for_development': 'pre_application',
    'property_development_type': 'demolition_conversion',
    'property_work_started': 'yes',
    'asset_type': 'Another string',
    'type_of_mortgage': 'commercial_buy_to_let',
    'experience_in_development': 'refurbishement_and_sale',
    'deposit': 50000,
    'vehicle_type': 'Apache helicopter',
    'type_of_property': 'undeveloped_land_with_planning_permission',
}

ENTITY_V1 = {
    'name': 'ddsaasd',
    "company_number": "123456",
    'legal_status': 'limited_company',
    'months_revenue':0,
    'trade_credit':0,
    'revenue':2000,
    'sic_code':'A',
    'card_revenue':3000,
    'financial_forecast':True,
    'revenue_growth':50,
    'purchase_orders':50,
    'registered_brand':True,
    'stock_imports':50,
    'customers':100,
    'business_plan':True,
    'stock_ready':50,
    'business_premises':50000,
    'region':'UKZ',
    'intellectual_property':True,
    'business_assets':30000,
    'accounting_software':'xero',
    'overseas_revenue':50,
    'online_revenue':50,
    'company_credit_rating':'ok',
    'exports':True,
    'profitability':50,
    'institutional_revenue':50,
    'up_to_date_accounts':True,
    'registration_date': '2012-01-23T00:00:00+00:00',
    'employees':50,
    'outstanding_invoices': 1000,
    'count_of_invoiced_customers':100,
    'total_value_of_unsatisfied_ccjs':1000,
    'date_of_first_filed_accounts': '2015-01-23T00:00:00+00:00',
    'addresses': [],
    'free_form': 'A string',
}

FINANCE_APPLICATION_V3 = {
    'applicant': PERSON_V1,
    'finance_need': FINANCE_NEED_V1,
    'requesting_entity': ENTITY_V1,
    'actors': []
}

# The following are fields that do not appear in the objects when they are translated from finance_application_v3

UNTRANSLATED_SME_V5_FIELDS = [
    'directors_pensions', #Aggregate
    'date_of_first_filed_accounts', #Unsupported
    'familiarity_with_financing', #Aggregate
    'personal_credit_ratings', #Aggregate
    'directors_houses', #Aggregate
]

UNTRANSLATED_CONTACT_V3_FIELDS = [
    'county', #Deprecated
]

# The following are fields that do not appear in the objects when they are translated from sme_v5 / sme_contact_v3

UNTRANSLATED_ENTITY_V1_FIELDS = [
    'employees', #Unsupported
    'registration_date', #Unsupported
    'addresses', #TODO
    'date_of_first_filed_accounts', #To remove
    'free_form', #Not present in SME_v5
]

UNTRANSLATED_FINANCE_APPLICATION_V3_FIELDS = [
    'actors', #Complex
]

UNTRANSLATED_PERSON_V1_FIELDS = [
    'date_of_birth' #Not present in SME_v5
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
        with open('./sme_finance_application_schema/' + schema) as f:
            store['https://www.fundingoptions.com/schema/' + schema] = json.loads(f.read())


class TestJson(TestCase):
    def test_entity_json(self):
        for schema in ('entity_v1', 'person_v1', 'finance_need_v1', 'address_v1', 'finance_application_v1', 'finance_application_v2', 'finance_application_v3', 'batch_application_v1', 'batch_response_v1', 'actor_v1'):
            with self.subTest(schema=schema):
                with open('./sme_finance_application_schema/' + schema) as f:
                    content = f.read()
                self.assertTrue(json.loads(content))


def test_validity_of_data(data, schema_name):
    with open('./sme_finance_application_schema/{}'.format(schema_name)) as f:
        schema = json.loads(f.read())
        validator = jsonschema.validators.Draft4Validator(schema)
        patch_store(validator.resolver.store)
        if not validator.is_valid(data):
            raise Exception('invalid data according to {}: {}'.format(schema_name, validator.validate(SME_V5)))





class TestTranslations(TestCase):
    def completion_of_data_subtest(self, data, schema_name):
        with open('./sme_finance_application_schema/{}'.format(schema_name)) as f:
            schema = json.loads(f.read())
            expected_fields = schema['properties'].keys()
            for field in expected_fields:
                with self.subTest(field=field):
                    self.assertIn(field, data)

    def validity_of_data_subtest(self, data, schema_name):
        with open('./sme_finance_application_schema/{}'.format(schema_name)) as f:
            schema = json.loads(f.read())
            validator = jsonschema.validators.Draft4Validator(schema)
            patch_store(validator.resolver.store)
            self.assertTrue(validator.is_valid(data))

    def test_sample_data_is_valid(self):
        self.validity_of_data_subtest(SME_V5,'sme_v5')
        self.validity_of_data_subtest(SME_CONTACT_V3,'sme_contact_v3')
        self.validity_of_data_subtest(FINANCE_APPLICATION_V3,'finance_application_v3')

    def test_sample_data_is_complete(self):
        self.completion_of_data_subtest(SME_V5,'sme_v5')
        self.completion_of_data_subtest(SME_CONTACT_V3,'sme_contact_v3')
        self.completion_of_data_subtest(FINANCE_APPLICATION_V3,'finance_application_v3')
        self.completion_of_data_subtest(FINANCE_NEED_V1,'finance_need_v1')
        self.completion_of_data_subtest(ENTITY_V1,'entity_v1')
        self.completion_of_data_subtest(PERSON_V1,'person_v1')
        self.completion_of_data_subtest(ADDRESS_V1,'address_v1')
        #self.completion_of_data_subtest(ACTOR_V1,'actor_v1')


    def test_sme_v5_and_contact_v3_to_finance_application_v3_translator(self):
        from .translations import sme_v5_and_contact_v3_to_finance_application_v3_translator
        self.maxDiff = None

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

        with open('./sme_finance_application_schema/finance_application_v3') as f:
            content = f.read()
        json_content = json.loads(content)
        validator = jsonschema.validators.Draft4Validator(json_content)
        patch_store(validator.resolver.store)
        self.assertTrue(validator.is_valid(sme_v5_and_contact_v3_to_finance_application_v3_translator(SME_V5, SME_CONTACT_V3)))


    def test_finance_application_v3_to_sme_v5(self):
        from .translations import finance_application_v3_to_sme_v5
        expected_sme_v5 = copy.deepcopy(SME_V5)
        for field in UNTRANSLATED_SME_V5_FIELDS:
            expected_sme_v5.pop(field)

        translated_sme_v5 = finance_application_v3_to_sme_v5(FINANCE_APPLICATION_V3)
        self.assertDictEqual(translated_sme_v5, expected_sme_v5)

    def test_finance_application_v3_to_sme_contact_v3(self):
        from .translations import finance_application_v3_to_sme_contact_v3
        expected_sme_contact_v3 = copy.deepcopy(SME_CONTACT_V3)
        for field in UNTRANSLATED_CONTACT_V3_FIELDS:
            expected_sme_contact_v3.pop(field)

        translated_sme_contact_v3 = finance_application_v3_to_sme_contact_v3(FINANCE_APPLICATION_V3)
        self.assertDictEqual(translated_sme_contact_v3, expected_sme_contact_v3)
