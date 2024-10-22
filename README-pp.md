# Donation Import from PayPal

This script requires Python 3.

## Input CSV file

The CSV file from PayPal must have these columns.

|PayPal Field          |Required For                                                                                                                         |
|----------------------|-------------------------------------------------------------------------------------------------------------------------------------|
|Payout Date           |                                                                                                                                     |
|Donation Date         |[Donation Table](#donation-table)<br/>[Membership Table](#membership-table)                                                          |
|Donor First Name      |[Individual Contact Table](#individual-contact-table)                                                                                |
|Donor Last Name       |[Individual Contact Table](#individual-contact-table)                                                                                |
|Donor Email           |[Individual Contact Table](#individual-contact-table)<br/>[Donation Table](#donation-table)<br/>[Membership Table](#membership-table)|
|Program Name          |                                                                                                                                     |
|Reference Information |                                                                                                                                     |
|Currency Code         |                                                                                                                                     |
|Gross Amount          |[Donation Table](#donation-table)                                                                                                    |
|Total Fees            |                                                                                                                                     |
|Net Amount            |                                                                                                                                     |
|Transaction ID        |[Donation Table](#donation-table)                                                                                                    |

## Steps

Export csv from PayPal. Keep the headings, and the column order does
not matter.

Run the following code:

~~~bash
python export.py ${paypal_csv} ${export_folder}
~~~

`${paypal_csv}` and `${export_folder}` are optional and default 
to `CharityDataDownload.csv` and today's day (with the format YYYY-MM-DD) 
respectively. The `${export_folder}` folder will be created as needed.

Import contacts into CiviCRM before importing donations. Please use the
mapping prefixed with "PayPal".


## Output CSV files

- ${export_folder}/individual_contacts.csv
	- export for Import Contact with the mapping "PayPal Individuals",
	- fields follows [Individual Contact Table](#individual-contact-table)
- ${export_folder}/individual_donations.csv
	- export for Import Contact with the mapping "PayPal Individuals Donations"
	- fields follows [Donation Table](#donation-table)
- ${export_folder}/memberships.csv
	- export for Import Memberships with the mapping "PayPal Donations"
	- fields follows [Membership Table](#membership-table)

### Individual Contact Table

|CiviCRM Field         |PayPal Field     |Required|
|----------------------|-----------------|--------|
|EXTERNAL_ID           |Donor Email      |**YES** |
|FIRST_NAME            |Donor First Name |**YES** |
|LAST_NAME             |Donor Last Name  |**YES** |
|EMAIL                 |Donor Email      |**YES** |


### Donation Table

|CiviCRM Field  |PayPal Field   |Required/Value|
|---------------|-------------- |--------------|
|EXTERNAL_ID    |Donor Email    |**YES**       |
|INVOICE_NUMBER |Transaction ID |No            |
|TOTAL_AMOUNT   |Gross Amount   |**YES**       |
|DATE_RECEIVED  |Donation Date  |No            |
|FINANCIAL_TYPE |*n/a*          |`Donation`    |
|PAYMENT_METHOD |*n/a*          |`PayPal`      |


### Membership Table

|CiviCRM Field        |PayPal Field  |Required/Value|
|---------------------|--------------|--------------|
|EXTERNAL_ID          |Donor Email   |**YES**       |
|MEMBERSHIP_TYPE      |Gross Amount  |`VCN Member`  |
|MEMBERSHIP_START_DATE|Donation Date |No            |

## Notes

- the date format can be either `%Y/%m/%d` or `%Y-%m-%d`
- header line is needed for the importing PayPal csv file
