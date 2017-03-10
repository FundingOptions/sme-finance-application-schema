def finance_application_v3_to_sme_contact_v3(finance_application):
    applicant = finance_application['applicant']
    requesting_entity = finance_application['requesting_entity']
    sme_contact_v3 = {
        'sme_name': requesting_entity['name'],
        'applicant_surname': applicant['surname'],
        'applicant_first_name': applicant.get('first_name') or None,  # disallow blank values
        'applicant_title': applicant.get('title'),
        'email': applicant.get('email'),
        'telephone': applicant.get('telephone'),
        'company_number': requesting_entity.get('company_number'),
    }
    if 'addresses' in applicant:
        if len(applicant['addresses']) != 1:
            raise ValueError("Cannot safely convert applicant with multiple addresses to sme_contact_v3")

        address = applicant['addresses'][0]['address']
        sme_contact_v3.update({
            'address_line_1': address['building_number_and_street_name'],
            'address_line_2': address.get('locality_name'),
            'city': address.get('post_town'),
            'postcode': address['postcode']
        })
    return _remove_key_if_value_is_none(sme_contact_v3)


def finance_application_v3_to_sme_v5(finance_application):
    sme_v5 = {}
    for field in ('legal_status', 'months_revenue', 'revenue',
        'sic_code', 'profitability', 'directors_houses', 'business_assets',
        'overseas_revenue', 'exports', 'stock_imports', 'purchase_orders',
        'directors_pensions', 'up_to_date_accounts', 'financial_forecast',
        'business_plan', 'card_revenue', 'online_revenue', 'institutional_revenue',
        'stock_ready', 'revenue_growth', 'intellectual_property', 'trade_credit',
        'business_premises', 'registered_brand', 'customers', 'region',
        'company_credit_rating', 'familiarity_with_financing', 'accounting_software'):
        if field in finance_application['requesting_entity']:
            sme_v5[field] = finance_application['requesting_entity'][field]
    for field in ( 'requested_amount', 'finance_type_requested', 'date_finance_required',
            'date_finance_requested', 'finance_term_length', 'guarantor_available', 'purpose'):
        if field in finance_application['finance_need']:
            sme_v5[field] = finance_application['finance_need'][field]
    return sme_v5

def sme_v5_and_contact_v3_to_finance_application_v3_translator(sme, sme_contact):
    applicant = sme_contact_v3_to_person_v1_translator(sme_contact)
    requesting_entity = sme_v5_and_contact_v3_to_requesting_entity_v1_translator(sme, sme_contact)
    finance_need = sme_v5_to_finance_need_v1_translator(sme)
    return {
        'applicant': applicant,
        'requesting_entity': requesting_entity,
        'finance_need': finance_need
    }


def sme_v5_and_contact_v3_to_requesting_entity_v1_translator(sme, sme_contact):
    requesting_entity = {
        'name': sme_contact.get('sme_name'),
        'company_number': sme_contact.get('company_number'),
        'legal_status': sme.get('legal_status'),
        'months_revenue': sme.get('months_revenue'),
        'revenue': sme.get('revenue'),
        'sic_code': sme.get('sic_code'),
        'profitability': sme.get('profitability'),
        'directors_houses': sme.get('directors_houses'),
        'business_assets': sme.get('business_assets'),
        'overseas_revenue': sme.get('overseas_revenue'),
        'exports': sme.get('exports'),
        'stock_imports': sme.get('stock_imports'),
        'purchase_orders': sme.get('purchase_orders'),
        'directors_pensions': sme.get('directors_pensions'),
        'up_to_date_accounts': sme.get('up_to_date_accounts'),
        'financial_forecast': sme.get('financial_forecast'),
        'business_plan': sme.get('business_plan'),
        'card_revenue': sme.get('card_revenue'),
        'online_revenue': sme.get('online_revenue'),
        'institutional_revenue': sme.get('institutional_revenue'),
        'stock_ready': sme.get('stock_ready'),
        'revenue_growth': sme.get('revenue_growth'),
        'intellectual_property': sme.get('intellectual_property'),
        'trade_credit': sme.get('trade_credit'),
        'business_premises': sme.get('business_premises'),
        'registered_brand': sme.get('registered_brand'),
        'customers': sme.get('customers'),
        'region': sme.get('region'),
        'company_credit_rating': sme.get('company_credit_rating'),
        'familiarity_with_financing': sme.get('familiarity_with_financing'),
        'accounting_software': sme.get('accounting_software')
    }
    return _remove_key_if_value_is_none(requesting_entity)


def sme_v5_to_finance_need_v1_translator(sme):
    finance_need = {
        'requested_amount': sme.get('requested_amount'),
        'finance_type_requested': sme.get('finance_type_requested'),
        'date_finance_required': sme.get('date_finance_required'),
        'date_finance_requested': sme.get('date_finance_requested'),
        'finance_term_length': sme.get('finance_term_length'),
        'guarantor_available': sme.get('guarantor_available'),
        'purpose': sme.get('purpose'),
    }
    return _remove_key_if_value_is_none(finance_need)


def sme_contact_v3_to_address_v1_translator(sme_contact):
    address = {
        'building_number_and_street_name': sme_contact.get('address_line_1') or '',
        'postcode': sme_contact.get('postcode') or '',
        'post_town': sme_contact.get('city')
    }
    return _remove_key_if_value_is_none(address)


def sme_contact_v3_to_person_v1_translator(sme_contact):
    person = {
        'title': sme_contact.get('applicant_title'),
        'first_name': sme_contact.get('applicant_first_name') or '',
        'surname': sme_contact.get('applicant_surname') or '',
        'email': sme_contact.get('email'),
        'telephone': sme_contact.get('telephone')
    }
    address = sme_contact_v3_to_address_v1_translator(sme_contact)
    if _dictionary_has_populated_values(address):
        person['addresses'] = [{'address': address}]

    return _remove_key_if_value_is_none(person)


def _remove_key_if_value_is_none(dictionary):
    return dict(
        (key, value) for key, value in dictionary.items()
        if value is not None
    )


def _dictionary_has_populated_values(dictionary):
    return any(value for value in dictionary.values())
