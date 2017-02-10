# sme_finance_application_schema
## Dislaimer
These schema are released to facilitate industry implementation of the Government referral scheme. We actively welcome queries, feedback and suggestions from any interested parties, which can be provided via our GitHub repository or to info@fundingoptions.com.
They are not in any way intended to be construed as authoritative or official, and are provided without commitment or warranty.
## Overview
These schema are designed to describe a range of pertinent characteristics of a Small to Medium Enterprise (SME) and of their financing needs, to facilitate faster and better identification of suitability for various business finance products and providers. A limited subset of data elements within the schema can facilitate minimum compliance with new SME finance referrals regulations (the "Government referral scheme"). However, the provision of additional information where available can be expected to provide a better experience for the referred SME.

These schema describe two main data objects - an SME finance application ('SME finance application') and contact details for the SME ('Identifying information'). The purpose of having two separate schema is to allow the identifying information to be separated from the application for compliance with the Government referral scheme. A third schema ('SME finance application wrapper') combines the first two. These schema are designed to allow interoperability between sources of SMEs seeking finance and potential providers of finance.schema are designed to describe a range of pertinent characteristics of a Small to Medium Enterprise (SME) and of their financing needs, to facilitate faster and better identification of suitability for various business finance products and providers.

The SME finance application and the Identifying information are contained within a 'Finance application', which contains metadata (including a referrer-provided unique identifier) about the application. To support the transfer of multiple applications, a 'Batch application' object is also described.

Finally, a 'Finance application response' and accompanying 'Batch response' are described to allow the platform to communicate back to the referring partner.

## Further reading
https://www.fundingoptions.com/schemas/
