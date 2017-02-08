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
    return _strip_dictionary(requesting_entity)


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
    return _strip_dictionary(finance_need)


def sme_contact_v3_to_address_v1_translator(sme_contact):
    address = {
        'building_number_and_street_name': sme_contact.get('address_line_1') or '',
        'postcode': sme_contact.get('postcode') or ''
    }
    return _strip_dictionary(address)


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

    return _strip_dictionary(person)


def _strip_dictionary(dictionary):
    """Remove key value pairs from dictionary where the value is null"""
    return dict(
        (key, value) for key, value in dictionary.items()
        if value is not None
    )


def _dictionary_has_populated_values(dictionary):
    return any(value for value in dictionary.values())
