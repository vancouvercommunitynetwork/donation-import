# Donation Import from CanadaHelps

The [script] uses python. This can be either Python 2 or 
Python 3.

## Input CSV file

The CSV file from CanadaHelps must have these columns.

|CanadaHelps Field    |Required For                                                                                                                                             |
|---------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------|
|DONOR FIRST NAME     |[Individual Contact Table](#individual-contact-table)                                                                                                    |
|DONOR LAST NAME      |[Individual Contact Table](#individual-contact-table)                                                                                                    |
|DONOR COMPANY NAME   |[Organization Contact Table](#organization-contact-table)                                                                                                |
|DONOR ADDRESS 1      |[Individual Contact Table](#individual-contact-table)<br/>[Organization Contact Table](#organization-contact-table)                                      |
|DONOR ADDRESS 2      |[Individual Contact Table](#individual-contact-table)<br/>[Organization Contact Table](#organization-contact-table)                                      |
|DONOR CITY           |[Individual Contact Table](#individual-contact-table)<br/>[Organization Contact Table](#organization-contact-table)                                      |
|DONOR PROVINCE/STATE |[Individual Contact Table](#individual-contact-table)<br/>[Organization Contact Table](#organization-contact-table)                                      |
|DONOR POSTAL/ZIP CODE|[Individual Contact Table](#individual-contact-table)<br/>[Organization Contact Table](#organization-contact-table)                                      |
|DONOR COUNTRY        |[Individual Contact Table](#individual-contact-table)<br/>[Organization Contact Table](#organization-contact-table)                                      |
|DONOR PHONE NUMBER   |[Individual Contact Table](#individual-contact-table)<br/>[Organization Contact Table](#organization-contact-table)                                      |
|DONOR EMAIL ADDRESS  |[Individual Contact Table](#individual-contact-table)<br/>[Organization Contact Table](#organization-contact-table)<br/>[Donation Table](#donation-table)|
|TRANSACTION NUMBER   |[Donation Table](#donation-table)                                                                                                                        |
|AMOUNT               |[Donation Table](#donation-table)                                                                                                                        |
|DONATION DATE        |[Donation Table](#donation-table)<br/>[Membership Table](#membership-table)                                                                              |
|DONATION SOURCE      |[Donation Table](#donation-table)                                                                                                                        |
|MESSAGE TO CHARITY   |[Donation Table](#donation-table)                                                                                                                        |

## Steps

Export csv from CanadaHelps. Keep the headings, and the column order does
not matter.

Run the following code:

~~~bash
python donations.py ${canada_help_csv} ${export_folder}
~~~

`${canada_help_csv}` and `${export_folder}` are optional and default 
to `CharityDataDownload.csv` and today's day (with the format DD-MM-YYYY) 
respectively. The `${export_folder}` folder will be created as needed.

Import contacts into CiviCRM before importing donations. Please use the
mapping prefixed with "CanadaHelps".

[script]:donations.py

## Output CSV files

- *temporary file*
	- file used to fix CanadaHelps csv file format
- ${export_folder}/individual_contacts.csv
	- export for Import Contact with the mapping "CanadaHelps Individuals",
	- fields follows [Individual Contact Table](#individual-contact-table)
- ${export_folder}/individual_donations.csv
	- export for Import Contact with the mapping "CanadaHelps Individuals Donations"
	- fields follows [Donation Table](#donation-table)
- ${export_folder}/organization_contacts.csv
	- export for Import Contact with the mapping "CanadaHelps Organizations"
	- fields follows [Organization Contact Table](#organization-contact-table)
- ${export_folder}/organization_donations.csv
	- export for Import Contact with the mapping "CanadaHelps Organizations"
	- fields follows [Donation Table](#donation-table)
- ${export_folder}/memberships.csv
	- export for Import Memberships with the mapping "CanadaHelps Donations"
	- fields follows [Membership Table](#membership-table)

### Individual Contact Table

|CiviCRM Field         |CanadaHelps Field    |Required|
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


### Organization Contact Table

|CiviCRM Field         |CanadaHelps Field    |Required|
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


### Donation Table

|CiviCRM Field  |CanadaHelps Field  |Required/Value|
|---------------|-------------------|--------------|
|EXTERNAL_ID    |DONOR EMAIL ADDRESS|**YES**       |
|INVOICE_NUMBER |TRANSACTION NUMBER |No            |
|TOTAL_AMOUNT   |AMOUNT             |**YES**       |
|DATE_RECEIVED  |DONATION DATE      |No            |
|DONATION_SOURCE|DONATION SOURCE    |No            |
|NOTE           |MESSAGE TO CHARITY |No            |
|FINANCIAL_TYPE |*n/a*              |`Donation`    |
|PAYMENT_METHOD |*n/a*              |`Credit Card` |


### Membership Table

|CiviCRM Field        |CanadaHelps Field  |Required/Value|
|---------------------|-------------------|--------------|
|EXTERNAL_ID          |DONOR EMAIL ADDRESS|**YES**       |
|MEMBERSHIP_TYPE      |AMOUNT             |`VCN Member`  |
|MEMBERSHIP_START_DATE|DONATION DATE      |No            |

## Notes

- All text with "Anon" will becomes empty. This is a mean to reduces errors
- Anonymous donation will go to the individual with "ANON" as the external id
- Anonymous will not add into the contact import file
- If the field is not found or is "ANON", then field will be empty, except for
  total amount, which will be 0.00
- the date format can be either `%Y/%m/%d` or `%Y-%m-%d`
- header line is needed for the importing CanadaHelps csv file

# History of Changes 

Since March 18 2025
- Added unit tests
- Issues Fixed
  - CSV input data not explicitly being encoded as UTF-8 after being read
  - Incorrect error handling when converting date

Since March 11 2025
- Added support to allow different input CSV file encodings to be read
   - Included sample CSVs with different formats

Since Jun 13 2022
- Added logic and documentation for membership CSV export

Since Jun 03 2022
- Updated `README.md` with a table for input CSV file fields
- Fixed spelling errors in `README.md`

Since Dec 13 2018
- Remove the old files as it now not being used
- Updated the `README.md` with new instructions

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
