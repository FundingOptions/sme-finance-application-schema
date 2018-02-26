from unittest import TestCase
import json
import jsonschema.validators

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
}

SME_CONTACT_V3 = {
    'applicant_title': 'Mr',
    'applicant_first_name': 'Dave',
    'applicant_surname': 'dd',
    'telephone': '+447445387241',
    'sme_name': 'ddsaasd',
    'email': 'nestor.arocha@fundingoptions.com',
    'company_number': '123456',
    'address_line_1': 'Unit 109',
    'address_line_2': '30 Great Guildford Street',
    'postcode': 'SE1 0HS',
    'city': 'London',
    'county': 'London',
}

FINANCE_APPLICATION_V3 = {
    'applicant': {
        'first_name': '',
        'surname': 'dd',
        'telephone':'+447445387241',
        'email': 'nestor.arocha@fundingoptions.com'
    },
    'finance_need': {
        'finance_term_length': 30,
        'purpose': 'stock',
        'date_finance_requested': '2017-01-23T00:00:00+00:00',
        'date_finance_required': '2018-01-23T00:00:00+00:00',
        'requested_amount': 3000,
        'finance_type_requested':'term_loan',
        'guarantor_available':True,
    },
    'requesting_entity': {
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
        'total_value_of_unsatisfied_ccjs':1000
    },
    'actors': []
}

KNOWN_UNTRANSLATED_SME_V5_FIELDS = [
    'directors_pensions',
    'date_of_first_filed_accounts',
    'familiarity_with_financing',
    'personal_credit_ratings',
    'directors_houses',
    'total_value_of_unsatisfied_ccjs',
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


def test_completion_of_data(data, schema_name):
    with open('./sme_finance_application_schema/{}'.format(schema_name)) as f:
        schema = json.loads(f.read())
        expected_fields = schema['properties'].keys()
        for field in expected_fields:
            if field not in data:
                raise Exception('sample data missing field according to {}: {}'.format(schema_name, field))


class TestTranslations(TestCase):
    def test_sample_data_is_valid(self):
        test_validity_of_data(SME_V5,'sme_v5')
        test_validity_of_data(SME_CONTACT_V3,'sme_contact_v3')
        test_validity_of_data(FINANCE_APPLICATION_V3,'finance_application_v3')


    def test_sample_data_is_complete(self):
        test_completion_of_data(SME_V5,'sme_v5')
        test_completion_of_data(SME_CONTACT_V3,'sme_contact_v3')
        test_completion_of_data(FINANCE_APPLICATION_V3,'finance_application_v3')


    def test_finance_application_v3_to_sme_v5_completeness(self):
        """
        This confirms that all fields in sme_v5 are accounted for
        when creating one out of a finance_application_v3
        """
        with open('./sme_finance_application_schema/sme_v5') as f:
            sme_v5 = json.loads(f.read())
            all_fields = sme_v5['properties'].keys()

        expected_fields = [x for x in all_fields if x not in KNOWN_UNTRANSLATED_SME_V5_FIELDS]

        from .translations import finance_application_v3_to_sme_v5
        sme_v5 = finance_application_v3_to_sme_v5(FINANCE_APPLICATION_V3)
        for field in expected_fields:
            with self.subTest(field=field):
                self.assertIn(field, sme_v5)

    def test_sme_v5_and_contact_v3_to_finance_application_v3_translator(self):
        from .translations import sme_v5_and_contact_v3_to_finance_application_v3_translator
        self.maxDiff = None
        self.assertDictEqual(sme_v5_and_contact_v3_to_finance_application_v3_translator(SME_V5, SME_CONTACT_V3), FINANCE_APPLICATION_V3)
        with open('./sme_finance_application_schema/finance_application_v3') as f:
            content = f.read()
        json_content = json.loads(content)
        validator = jsonschema.validators.Draft4Validator(json_content)
        patch_store(validator.resolver.store)
        self.assertTrue(validator.is_valid(sme_v5_and_contact_v3_to_finance_application_v3_translator(SME_V5, SME_CONTACT_V3)))

    def test_finance_application_v3_to_sme_v5(self):
        from .translations import finance_application_v3_to_sme_v5
        for field in KNOWN_UNTRANSLATED_SME_V5_FIELDS:
            SME_V5.pop(field)
        self.assertDictEqual(finance_application_v3_to_sme_v5(FINANCE_APPLICATION_V3), SME_V5)

    def test_finance_application_v3_to_sme_contact_v3(self):
        from .translations import finance_application_v3_to_sme_contact_v3
        self.assertDictEqual(finance_application_v3_to_sme_contact_v3(FINANCE_APPLICATION_V3), SME_CONTACT_V3)
