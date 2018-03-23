# sme_finance_application_schema

![Travis CI](https://travis-ci.org/FundingOptions/sme-finance-application-schema.svg?branch=master)

## Disclaimer
These schema are released to:
* Allow Funding Options to communicate with Partners (including Lenders)
* Facilitate industry implementation of the Government referral scheme

We actively welcome queries, feedback and suggestions from any interested parties, which can be provided via [our GitHub repository](https://github.com/FundingOptions/sme-finance-application-schema) or techsupport@fundingoptions.com.

They are not in any way intended to be construed as authoritative or official, and are provided without commitment or warranty.

## Overview
These schema are designed to describe a range of pertinent characteristics of a Small to Medium Enterprise (SME) and of their financing needs, to facilitate faster and better identification of suitability for various business finance products and providers.

As at March 2018 there are two schema in use by Funding Options:

* finance_application_v3 - this is the current schema in use by Funding Options for communicating with Partners excepting banks Referring to Funding Options under the Bank Referral Scheme. This references multiple child schema.
* finance_application_v2 - this is in use by the Bank Referral Scheme and was frozen in 2016-08 prior to scheme launch. This references two child schema, sme_v4 and sme_contact_v3.

## Use outside the Bank Referral Scheme
As at March 2018, finance_application_v3 is the current schema for use by Partners of Funding Options outside the Bank Referral Scheme. finance_application_v3 references several child schema:
* person_v1
* actor_v1
* entity_v1
* finance_need_v1
* aggregated_actors_v1
* address_v1

## Use inside the Bank Referral Scheme
finance_application_v2 was the schema adopted by the Bank Referral Scheme in 2016 prior to scheme launch. It has not changed since. The relevant release of the schema repository is v1.7.

finance_application_v2 references two child schema:
* sme_v4 or sme_v5
* sme_contact_v3

Please note that use of finance_application_v2 is not supported outside the context of the Bank Referral Scheme - use finance_application_v3 instead.

In order to be compliant with the Government referral scheme as described in the draft Regulations to illustrate the Treasury’s current intention as to the exercise of powers under clause 5 of the Small Business, Enterprise and Employment Bill, SME finance applications must contain certain specified information. Therefore, the documents (SME finance applications and accompanying Identifying information) created from the finance_application_v2 schema are required to have the following properties to be complaint with the scheme:

| Specified information | Schema | Property |
| - | - | - |
| "(a) the name of the small or medium sized business;" | sme_contact_v3 | sme_name |
| "(b) the postal address, email address and telephone number of the business;" | sme_contact_v3 | address_line_1, postcode |
| "(b) the postal address, email address and telephone number of the business;" | sme_contact_v3 | email |
| "(b) the postal address, email address and telephone number of the business;" | sme_contact_v3 | telephone |
| "(c) the amount of finance requested by the business;" | sme_v4 | requested_amount |
| "(d) the type of finance requested by the business (where a specific type of finance has been requested by the business);" | sme_v4 | finance_type_requested |
| "(e) the legal structure of the business (limited company, limited partnership, partnership sole trader, or other);" | sme_v4 | legal_status |
| "(f) the period in years and months for which the business has been trading and receiving income;" | sme_v4 | months_revenue |
| "(g) the date by which the business requires finance by or, if such date is not known, the date by which the business has requested finance." | sme_v4 | date_finance_required |
| "(g) the date by which the business requires finance by or, if such date is not known, the date by which the business has requested finance." | sme_v4 | date_finance_requested |

## Versioning
Non-breaking changes will be added to the most recent version of the schema. Breaking changes will require a new version of the schema to be issued. This is explicitly in preference to tagging releases. This versioning system was decided on in order to:
* make this repository accessible to all participants in the Bank Referral Scheme
* make it possible to work with data in multiple formats

## Schema detail
The schema themselves are written in JSON, according to [JSON schema v4](http://json-schema.org/). It is therefore easy to use the schema to construct JSON objects. The schema contain sufficient information to begin designing compatible XML documents (following conversion to Document Type Definitions), CSV files or similar.

Please visit [our Github repository](https://github.com/FundingOptions/sme-finance-application-schema) for more details.
