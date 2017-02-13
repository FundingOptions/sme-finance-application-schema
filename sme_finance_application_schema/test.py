from unittest import TestCase
import json
import jsonschema.validators

SME = {"legal_status": "limited_company", "finance_term_length": 30, "purpose": "stock", "months_revenue": 0, "requested_amount": 3000, "date_finance_requested": "2017-01-23T00:00:00+00:00", "trade_credit": 0, "revenue": 2000, "sic_code": "A"}
SME_CONTACT = {"applicant_surname": "dd", "telephone": "+447445387241", "sme_name": "ddsaasd", "email": "nestor.arocha@fundingoptions.com"}

def patch_store(store):
    for schema in ('entity_v1', 'person_v1', 'finance_need_v1', 'address_v1'):
        with open('./sme_finance_application_schema/' + schema) as f:
            store['https://www.fundingoptions.com/schema/' + schema] = json.loads(f.read())


class TestJson(TestCase):
    def test_entity_json(self):
        with open('./sme_finance_application_schema/entity_v1') as f:
            content = f.read()
        self.assertTrue(json.loads(content))


class TestTranslations(TestCase):
    def test_sme_v5_and_contact_v3_to_finance_application_v3_translator(self):
        from .translations import sme_v5_and_contact_v3_to_finance_application_v3_translator
        self.maxDiff = None
        self.assertDictEqual(sme_v5_and_contact_v3_to_finance_application_v3_translator(SME, SME_CONTACT), 
                {'applicant': {'first_name':'', 'surname': 'dd', 'telephone':'+447445387241', 'email': 'nestor.arocha@fundingoptions.com'},
                    'finance_need': {"finance_term_length": 30, "purpose": "stock", "date_finance_requested": "2017-01-23T00:00:00+00:00", "requested_amount": 3000, },
                    'requesting_entity': {'name': 'ddsaasd', 'legal_status': 'limited_company', 'months_revenue':0, 'trade_credit':0, 'revenue':2000, 'sic_code':'A'}})
        with open('./sme_finance_application_schema/finance_application_v3') as f:
            content = f.read()
        json_content = json.loads(content)
        validator = jsonschema.validators.Draft4Validator(json_content)
        patch_store(validator.resolver.store)
        validator.is_valid(sme_v5_and_contact_v3_to_finance_application_v3_translator(SME, SME_CONTACT))
        self.assertTrue(validator.is_valid(sme_v5_and_contact_v3_to_finance_application_v3_translator(SME, SME_CONTACT)))
