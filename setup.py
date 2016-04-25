from setuptools import setup, find_packages
setup(name='sme_finance_application_schema',
      version='1.0',
      description='Schemas to facilitate industry implementation of the Government referral scheme',
      author='Funding Options',
      author_email='tech_support@fundingoptions.com',
      url='https://github.com/FundingOptions/sme-finance-application-schema',
      packages = find_packages(exclude=['tests.*']),
      package_dir={'sme_finance_application_schema': 'sme_finance_application_schema'},
      package_data={'sme_finance_application_schema': ['*']},
     )

