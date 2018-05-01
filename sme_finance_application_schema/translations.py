import re

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
    if applicant.get('addresses'):
        if len(applicant['addresses']) > 1:
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
                  'sic_code', 'profitability', 'business_assets',
                  'overseas_revenue', 'exports', 'stock_imports', 'purchase_orders',
                  'up_to_date_accounts', 'financial_forecast',
                  'business_plan', 'card_revenue', 'online_revenue', 'institutional_revenue',
                  'stock_ready', 'revenue_growth', 'intellectual_property', 'trade_credit',
                  'business_premises', 'registered_brand', 'customers', 'region',
                  'company_credit_rating', 'accounting_software', 'sets_of_filed_accounts',
                  'total_value_of_unsatisfied_ccjs', 'count_of_invoiced_customers', 'outstanding_invoices',
                  'count_of_unsatisfied_ccjs', 'count_of_all_ccjs', 'blended_credit_rating'):
        if field in finance_application.get('requesting_entity', {}):
            sme_v5[field] = finance_application['requesting_entity'][field]
    for field in ('requested_amount', 'finance_type_requested', 'date_finance_required',
                  'date_finance_requested', 'finance_term_length', 'guarantor_available', 'purpose'):
        if field in finance_application.get('finance_need', {}):
            sme_v5[field] = finance_application['finance_need'][field]

    if finance_application.get('actors'):
        director_or_guarantors = [x for x in finance_application['actors'] if x['role'] in ('director','guarantor')]
        for actor in director_or_guarantors:
            if 'value_of_property_equity' in actor:
                sme_v5.setdefault('directors_houses', 0)
                sme_v5['directors_houses'] += actor['value_of_property_equity']

            if 'value_of_pension' in actor:
                sme_v5.setdefault('directors_pensions', 0)
                sme_v5['directors_pensions'] += actor['value_of_pension']

            if 'familiarity_with_financing' in actor:
                familiarity_list = [
                    'first_time',
                    'had_finance_before',
                    'expert',
                ]

                sme_v5.setdefault('familiarity_with_financing', familiarity_list[0])
                max_familiarity = max(
                    sme_v5['familiarity_with_financing'],
                    actor['familiarity_with_financing'],
                    key=familiarity_list.index,
                )
                sme_v5['familiarity_with_financing'] = max_familiarity

            if 'personal_credit_rating' in actor:
                credit_list = [
                    'very_poor',
                    'poor',
                    'ok',
                    'good',
                    'excellent',
                ]

                sme_v5.setdefault('personal_credit_ratings', credit_list[-1])
                min_credit_rating = min(
                    sme_v5['personal_credit_ratings'],
                    actor['personal_credit_rating'],
                    key=credit_list.index,
                )
                sme_v5['personal_credit_ratings'] = min_credit_rating

    # Aggregated actors only used if no actor information available
    aggregated = finance_application.get('aggregated_actors', {})
    if aggregated.get('sum_value_of_property_equity') and 'directors_houses' not in sme_v5:
        sme_v5['directors_houses'] = aggregated.get('sum_value_of_property_equity')
    if aggregated.get('sum_value_of_pension') and 'directors_pensions' not in sme_v5:
        sme_v5['directors_pensions'] = aggregated.get('sum_value_of_pension')
    if aggregated.get('max_familiarity_with_financing') and 'familiarity_with_financing' not in sme_v5:
        sme_v5['familiarity_with_financing'] = aggregated.get('max_familiarity_with_financing')
    if aggregated.get('min_personal_credit_rating') and 'personal_credit_ratings' not in sme_v5:
        sme_v5['personal_credit_ratings'] = aggregated.get('min_personal_credit_rating')

    return sme_v5


def sme_v5_and_contact_v3_to_finance_application_v3_translator(sme, sme_contact):
    applicant = sme_contact_v3_to_person_v1_translator(sme_contact)
    requesting_entity = sme_v5_and_contact_v3_to_requesting_entity_v1_translator(sme, sme_contact)
    finance_need = sme_v5_to_finance_need_v1_translator(sme)
    aggregated_actors = sme_v5_to_aggregated_actors_v1_translator(sme)
    return _remove_key_if_value_is_none({
        'applicant': applicant,
        'requesting_entity': requesting_entity,
        'finance_need': finance_need,
        'aggregated_actors': aggregated_actors or None,
    })


def sme_v3_and_contact_v2_to_finance_application_v3_translator(sme, sme_contact, backfill_required_properties=False):
    applicant = sme_contact_v2_to_person_v1_translator(sme_contact, backfill_required_properties=backfill_required_properties)
    requesting_entity = sme_v3_and_contact_v2_to_requesting_entity_v1_translator(sme, sme_contact, backfill_required_properties=backfill_required_properties)
    finance_need = sme_v3_to_finance_need_v1_translator(sme, backfill_required_properties=backfill_required_properties)
    aggregated_actors = sme_v3_to_aggregated_actors_v1_translator(sme)
    return _remove_key_if_value_is_none({
        'applicant': applicant,
        'requesting_entity': requesting_entity,
        'finance_need': finance_need,
        'aggregated_actors': aggregated_actors or None,
    })


def sme_v3_and_contact_v2_to_requesting_entity_v1_translator(sme, sme_contact, backfill_required_properties=False):
    requesting_entity = {
        'name': sme_contact.get('sme_name'),
        'company_number': sme_contact.get('company_number'),
        'legal_status': sme.get('legal_status'),
        'months_revenue': sme.get('months_revenue'),
        'revenue': sme.get('revenue'),
        'sic_code': sme.get('sic_code'),
        'profitability': sme.get('profitability'),
        'business_assets': sme.get('business_assets'),
        'overseas_revenue': sme.get('overseas_revenue'),
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
    }
    requesting_entity = _remove_key_if_value_is_none(requesting_entity)
    if backfill_required_properties:
        requesting_entity = _backfill_required_properties(requesting_entity, {'name': 'Unknown', 'months_revenue': 0})

    # sme_v3 expresses card_revenue as a percentage, entity_v1 as a value
    card_revenue_as_percentage = requesting_entity.get('card_revenue')
    revenue = requesting_entity.get('revenue')
    if card_revenue_as_percentage and revenue:
        card_revenue_as_value = round(revenue*(card_revenue_as_percentage/100))
        requesting_entity['card_revenue'] = card_revenue_as_value
    elif card_revenue_as_percentage:
        # If we can't work it out, discard it
        requesting_entity.pop('card_revenue')

    # sme_v3 doesnt have a limit on months_revenue, entity_v1 does
    if int(requesting_entity.get('months_revenue', 0)) > 1800:
        requesting_entity['months_revenue'] = 1800

    # sme_v3 has an error in the partnership sizes
    if requesting_entity.get('legal_status') == 'partnership_less_than_5':
        requesting_entity['legal_status'] = 'partnership_less_than_equal_to_3'
    elif requesting_entity.get('legal_status') == 'partnership_more_than_4':
        requesting_entity['legal_status'] = 'partnership_greater_than_3'

    return requesting_entity


def sme_v5_and_contact_v3_to_requesting_entity_v1_translator(sme, sme_contact):
    # sme_v5 has additional properties to v3
    # sme_contact_v3 has different requirements to v2
    requesting_entity = sme_v3_and_contact_v2_to_requesting_entity_v1_translator(sme, sme_contact)
    additional_data_from_sme_v5 = {
        'exports': sme.get('exports'),
        'stock_imports': sme.get('stock_imports'),
        'purchase_orders': sme.get('purchase_orders'),
        'company_credit_rating': sme.get('company_credit_rating'),
        'blended_credit_rating': sme.get('blended_credit_rating'),
        'accounting_software': sme.get('accounting_software'),
        'total_value_of_unsatisfied_ccjs': sme.get('total_value_of_unsatisfied_ccjs'),
        'outstanding_invoices': sme.get('outstanding_invoices'),
        'count_of_invoiced_customers': sme.get('count_of_invoiced_customers'),
        'sets_of_filed_accounts': sme.get('sets_of_filed_accounts'),
        'count_of_all_ccjs': sme.get('count_of_all_ccjs'),
        'count_of_unsatisfied_ccjs': sme.get('count_of_unsatisfied_ccjs'),
        # Overwrite the card revenue provided by the sme_v3 translator since sme_v5 provides as a value
        'card_revenue': sme.get('card_revenue'),
    }
    requesting_entity.update(additional_data_from_sme_v5)
    return _remove_key_if_value_is_none(requesting_entity)


def sme_v3_to_finance_need_v1_translator(sme, backfill_required_properties=False):
    finance_need = {
        'requested_amount': sme.get('requested_amount'),
        'finance_type_requested': sme.get('finance_type_requested'),
        'date_finance_required': sme.get('date_finance_required'),
        'date_finance_requested': sme.get('date_finance_requested'),
        'finance_term_length': sme.get('finance_term_length'),
        'purpose': sme.get('purpose'),
    }
    finance_need = _remove_key_if_value_is_none(finance_need)
    if backfill_required_properties:
        finance_need = _backfill_required_properties(finance_need, {'requested_amount': 0})
    return finance_need


def sme_v5_to_finance_need_v1_translator(sme):
    # sme_v5 has additional properties to v3
    finance_need = sme_v3_to_finance_need_v1_translator(sme)
    additional_data_from_sme_v5 = {
        'guarantor_available': sme.get('guarantor_available'),
    }
    finance_need.update(additional_data_from_sme_v5)
    return _remove_key_if_value_is_none(finance_need)


def sme_v3_to_aggregated_actors_v1_translator(sme):
    aggregated_actors = {
        'sum_value_of_personal_assets': sme.get('directors_houses'),
        'sum_value_of_property_equity': sme.get('directors_houses'),
        'sum_value_of_pension': sme.get('directors_pensions'),
    }
    return _remove_key_if_value_is_none(aggregated_actors)


def sme_v5_to_aggregated_actors_v1_translator(sme):
    # sme_v5 has additional properties to v3
    aggregated_actors = sme_v3_to_aggregated_actors_v1_translator(sme)
    additional_data_from_sme_v5 = {
        'max_familiarity_with_financing': sme.get('familiarity_with_financing'),
        'min_personal_credit_rating': sme.get('personal_credit_ratings'),
    }
    aggregated_actors.update(additional_data_from_sme_v5)
    return _remove_key_if_value_is_none(aggregated_actors)


def sme_contact_v3_to_address_v1_translator(sme_contact):
    address = {
        'building_number_and_street_name': sme_contact.get('address_line_1') or 'Unknown',
        'postcode': sme_contact.get('postcode') or 'Unknown',
        'post_town': sme_contact.get('city'),
        'locality_name': sme_contact.get('address_line_2'),
    }
    return _remove_key_if_value_is_none(address)


def sme_contact_v2_to_person_v1_translator(sme_contact, backfill_required_properties=False):
    person = {
        'title': sme_contact.get('applicant_title'),
        'first_name': sme_contact.get('applicant_first_name'),
        'surname': sme_contact.get('applicant_surname'),
        'email': sme_contact.get('email'),
        'telephone': sme_contact.get('telephone')
    }
    address = sme_contact_v3_to_address_v1_translator(sme_contact)
    if _dictionary_has_populated_values(address):
        person['addresses'] = [{'address': address}]

    person = _remove_key_if_value_is_none(person)

    if backfill_required_properties:
        person = _backfill_required_properties(person, {'first_name': 'Unknown', 'surname': 'Unknown'})

    telephone = person.get('telephone')
    if telephone:
        person['telephone'] = sme_contact_v2_telephone_to_e164_telephone(telephone)

    return person


def sme_contact_v2_telephone_to_e164_telephone(telephone):
    # We frequently find ourselves needing to remove whitespace
    telephone = telephone.replace(' ', '')
    # Generally, correction to E.164 involves dropping the leading zeros
    telephone = re.sub('^0+', '', telephone)
    return telephone


def sme_contact_v3_to_person_v1_translator(sme_contact):
    # The only difference between sme_contact_v2 and v3 is the requirements
    return sme_contact_v2_to_person_v1_translator(sme_contact)


def _remove_key_if_value_is_none(dictionary):
    return dict(
        (key, value) for key, value in dictionary.items()
        if value is not None
    )


def _backfill_required_properties(object_, backfill_values):
    for required_property, value in backfill_values.items():
        if required_property not in object_:
            object_[required_property] = value
    return object_


def _dictionary_has_populated_values(dictionary):
    return any(value for value in dictionary.values())
