# Donation Import from Canada Help

The [script] uses python. This can be either Python 2 or 
Python 3.

## Steps

Export csv from Canada Help. Keep the headings, and the column order does
not matter.

Run on of the following code:

~~~bash
python export.py ${canada_help_csv} ${export_folder}
~~~

`${canada_help_csv}` and `${export_folder}` are optional and defualts 
to `CharityDataDownload.csv` and today's day (with the format DD-MM-YYYY) 
respectively.

Import contacts into CiviCRM before importing donations. Please use the
mapping prefixed with "CanadaHelp".

See [script] for more details.

[script]:donations.py

## Output CSV files

- *temporary file*
	- file used to fix CanadaHelp csv file format
- ${export_folder}/individual_contacts.csv
	- export for Import Contact with the mapping "CanadaHelp Individuals",
	- fields follows [Individual Contact Table](#individual-contact-table)
- ${export_folder}/individual_donations.csv
	- export for Import Contact with the mapping "CanadaHelp Individuals Donations"
	- fields follows [Donation Table](#donation-table)
- ${export_folder}/organization_contacts.csv
	- export for Import Contact with the mapping "CanadaHelp Organizations"
	- fields follows [Organization Contact Table](#organization-contact-table)
- ${export_folder}/organization_donations.csv
	- export for Import Contact with the mapping "CanadaHelp Organizations"
	- fields follows [Donation Table](#donation-table)

## Individual Contact Table

|Civicrm Field         |Canada Help Field    |Required|
|----------------------|---------------------|--------|
|EXTERNAL_ID           |DONOR EMAIL ADDRESS  |**YES** |
|FIRST_NAME            |DONOR FIRST NAME     |**YES** |
|LAST_NAME             |DONOR LAST NAME      |**YES** |
|ADDRESS               |DONOR ADDRESS 1      |No      |
|SUPPLEMENTAL_ADDRESS_1|DONOR ADDRESS 2      |No      |
|CITY                  |DONOR CITY           |No      |
|STATE                 |DONOR PROVINCE/STATE |No      |
|POSTAL_CODE           |DONOR POSTAL/ZIP CODE|No      |
|COUNTRY               |DONOR COUNTRY        |No      |
|PHONE                 |DONOR PHONE NUMBER   |No      |
|EMAIL                 |DONOR EMAIL ADDRESS  |**YES** |


## Organization Contact Table

|Civicrm Field         |Canada Help Field    |Required|
|----------------------|---------------------|--------|
|EXTERNAL_ID           |DONOR EMAIL ADDRESS  |**YES** |
|COMPANY_NAME          |DONOR COMPANY NAME   |**YES** |
|ADDRESS               |DONOR ADDRESS 1      |No      |
|SUPPLEMENTAL_ADDRESS_1|DONOR ADDRESS 2      |No      |
|CITY                  |DONOR CITY           |No      |
|STATE                 |DONOR PROVINCE/STATE |No      |
|POSTAL_CODE           |DONOR POSTAL/ZIP CODE|No      |
|COUNTRY               |DONOR COUNTRY        |No      |
|PHONE                 |DONOR PHONE NUMBER   |No      |
|EMAIL                 |DONOR EMAIL ADDRESS  |**YES** |


## Donation Table

|Civicrm Field  |Canada Help Field  |Required/Value|
|---------------|-------------------|--------------|
|EXTERNAL_ID    |DONOR EMAIL ADDRESS|**YES**       |
|INVOICE_NUMBER |TRANSACTION NUMBER |No            |
|TOTAL_AMOUNT   |AMOUNT             |**YES**       |
|DATE_RECEIVED  |DONATION DATE      |No            |
|DONATION_SOURCE|DONATION SOURCE    |No            |
|NOTE           |MESSAGE TO CHARITY |No            |
|FINANCIAL_TYPE |*n/a*              |`Donation`    |
|PAYMENT_METHOD |*n/a*              |`Credit Card` |

## Notes

- All text with "Anon" will becomes empty. This is a mean to reduces errors
- Anonoymous donation will go to the individual with "ANON" as the external id
- Anonoymous will not add into the contact import file
- If the field is not found or is "ANON", then field will be empty, except for
  total amount, which will be 0.00
- the date format can be either %Y/%m/%d or %Y-%m-%d
- header line is needed for the importing CanadaHelps csv file

# History of Changes 

Since Dec 13 2018
- Remove the old files as it now not being used
- Updated the `README.md` with new instuctions

Since 1-12-2015 (DD-MM-YYYY format)
- Issues Fixed
  - Duplicated entries related to same csv file
  - Time not able to insert correctly

- Added Features
  - Finding Transaction That existed in database (see getTransID in database.py)
  - Saving Donator's LoginID with accordance with their email (see getLoginID in main.py)
    - if LoginID is vcn mail then will record their id
    - if not vcn mail then LoginID will become the donator's email
    - if ANON will become 000
  - Saving Transaction ID (as Paper Receipt)
