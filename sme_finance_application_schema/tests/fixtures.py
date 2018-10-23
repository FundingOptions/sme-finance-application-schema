import copy

SME_V3 = {
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
    'card_revenue':50,
    'financial_forecast':True,
    'finance_type_requested':'term_loan',
    'revenue_growth':50,
    'directors_pensions':60000,
    'registered_brand':True,
    'customers':100,
    'business_plan':True,
    'stock_ready':50,
    'business_premises':50000,
    'business_assets':30000,
    'region':'UKZ',
    'intellectual_property':True,
    'overseas_revenue':50,
    'online_revenue':50,
    'directors_houses':60000,
    'profitability':50,
    'institutional_revenue':50,
    'up_to_date_accounts':True,
    'finance_term_general': 'long_term_investing',
    'company_number': '123456',
}

SME_V3_MISSING_INFORMATION = copy.deepcopy(SME_V3)
for missing_field in ['requested_amount']:
    SME_V3_MISSING_INFORMATION.pop(missing_field)

# company_number and finance_term_general not present on v5
# card_revenue is now a value rather than percentage

SME_V5 = copy.deepcopy(SME_V3)
SME_V5.pop('company_number')
SME_V5.pop('finance_term_general')
SME_V5.update({
    'card_revenue':1000,
    'purchase_orders':50,
    'guarantor_available':True,
    'familiarity_with_financing':'expert',
    'stock_imports':50,
    'accounting_software':'xero',
    'company_credit_rating':'ok',
    'personal_credit_ratings':'poor',
    'exports':True,
    'profitability':50,
    'institutional_revenue':50,
    'up_to_date_accounts':True,
    'count_of_invoiced_customers': 100,
    'outstanding_invoices': 1000,
    'sets_of_filed_accounts': 10,
    'count_of_unsatisfied_ccjs': 1,
    'count_of_all_ccjs': 3,
    'total_value_of_unsatisfied_ccjs':1000,
    'vat_number': '123456789',
    'is_vat_registered': False,
    'trading_startdate': '2012-01-24'
})

SME_CONTACT_V2 = {
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

SME_CONTACT_V3 = copy.deepcopy(SME_CONTACT_V2)
SME_CONTACT_V3['applicant_role'] = 'director'
SME_CONTACT_V3['applicant_residential_status'] = 'owner_with_mortgage'
SME_CONTACT_V3['applicant_property_value'] = 100000

SME_CONTACT_V2_MISSING_INFORMATION = copy.deepcopy(SME_CONTACT_V2)
for missing_field in ['sme_name', 'applicant_first_name', 'applicant_surname']:
    SME_CONTACT_V2_MISSING_INFORMATION.pop(missing_field)

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
    'applicant_role': 'director',
    'residential_status': 'owner_with_mortgage',
    'property_value': 100000,
    'addresses': [{
        'address': copy.deepcopy(ADDRESS_V1),
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
    'experience_in_development': 'refurbishment_and_sale',
    'deposit': 50000,
    'vehicle_type': 'Apache helicopter',
    'type_of_property': 'undeveloped_land_with_planning_permission',
}

ENTITY_V1 = {
    'name': 'ddsaasd',
    'company_number': "123456",
    'is_vat_registered': False,
    'legal_status': 'limited_company',
    'months_revenue':0,
    'trade_credit':0,
    'revenue':2000,
    'sic_code':'A',
    'card_revenue':1000,
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
    'vat_number': '123456789',
    'trading_startdate': '2012-01-24',
    'addresses': [{
        'role': 'trading',
        'address': copy.deepcopy(ADDRESS_V1),
    }, {
        'role': 'registered',
        'address': copy.deepcopy(ADDRESS_V1),
    }],
    'free_form': 'A string',
    'sets_of_filed_accounts': 10,
    'count_of_unsatisfied_ccjs': 1,
    'count_of_all_ccjs': 3,
}

ACTOR_V1_DIRECTOR_1 = {
    'value_of_personal_assets': 10000,
    'outstanding_mortgage_on_property': 10000,
    'value_of_property_equity': 10000,
    'value_of_pension': 10000,
    'familiarity_with_financing': 'had_finance_before',
    'personal_credit_rating': 'ok',
    'role': 'director',
    'person': copy.deepcopy(PERSON_V1),
}

ACTOR_V1_DIRECTOR_2 = {
    'value_of_personal_assets': 30000,
    'outstanding_mortgage_on_property': 30000,
    'value_of_property_equity': 30000,
    'value_of_pension': 30000,
    'familiarity_with_financing': 'first_time',
    'personal_credit_rating': 'poor',
    'role': 'director',
    'person': copy.deepcopy(PERSON_V1),
}

ACTOR_V1_GUARANTOR = {
    'value_of_personal_assets': 20000,
    'outstanding_mortgage_on_property': 20000,
    'value_of_property_equity': 20000,
    'value_of_pension': 20000,
    'familiarity_with_financing': 'expert',
    'personal_credit_rating': 'excellent',
    'role': 'guarantor',
    'person': copy.deepcopy(PERSON_V1),
}

AGGREGATED_ACTORS_V1 = {
    'sum_value_of_personal_assets': 60000,
    'sum_outstanding_mortgage_on_property': 60000,
    'sum_value_of_property_equity': 60000,
    'sum_value_of_pension': 60000,
    'max_familiarity_with_financing': 'expert',
    'max_personal_credit_rating': 'excellent',
    'min_personal_credit_rating': 'poor',
}

AGGREGATED_ACTORS_V1_INCOMPLETE = {
    'sum_value_of_property_equity': 10000,
    'sum_value_of_pension': 1000000,
    'max_familiarity_with_financing': 'expert',
    'min_personal_credit_rating': 'excellent',
}

FINANCE_APPLICATION_V3 = {
    'applicant': copy.deepcopy(PERSON_V1),
    'finance_need': FINANCE_NEED_V1,
    'requesting_entity': ENTITY_V1,
    'actors': [ACTOR_V1_DIRECTOR_1, ACTOR_V1_DIRECTOR_2, ACTOR_V1_GUARANTOR],
    'aggregated_actors': AGGREGATED_ACTORS_V1,
}

FINANCE_APPLICATION_V3_AGGREGATED_INCOMPLETE = copy.deepcopy(FINANCE_APPLICATION_V3)
for actor in FINANCE_APPLICATION_V3_AGGREGATED_INCOMPLETE['actors']:
    actor.pop('familiarity_with_financing')
FINANCE_APPLICATION_V3_AGGREGATED_INCOMPLETE['aggregated_actors'] = AGGREGATED_ACTORS_V1_INCOMPLETE
