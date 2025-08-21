# Donation Import from ConnectionPoint

This script requires Python 3.

## Input CSV file

TODO: We need to find out what columns the file has, but it should at least have the following:

|CP Field              |Required For                                                                                                                         |
|----------------------|-------------------------------------------------------------------------------------------------------------------------------------|
|Date                  |[Donation Table](#donation-table)<br/>[Membership Table](#membership-table)                                                          |
|Contributor name      |[Individual Contact Table](#individual-contact-table), need special handling for first/last names                                    |
|Contributor email     |[Individual Contact Table](#individual-contact-table)<br/>[Donation Table](#donation-table)<br/>[Membership Table](#membership-table)|
|Total amount          |[Donation Table](#donation-table)                                                                                                    |
|Net amount            |                                                                                                                                     |
|Transaction ID        |[Donation Table](#donation-table)                                                                                                    |

## Steps

Export csv from ConnectionPoint. Keep the headings, and the column order does
not matter.

Run the following code:

~~~bash
python donations_cp.py ${cp_csv} ${export_folder}
~~~

`${cp_csv}` and `${export_folder}` are optional and default 
to `CharityDataDownload.csv` and today's day (with the format YYYY-MM-DD) 
respectively. The `${export_folder}` folder will be created as needed.

Import contacts into CiviCRM before importing donations. Please use the
mapping prefixed with "ConnectionPoint".


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

|CiviCRM Field         |CP Field               |Required                    |
|----------------------|-----------------------|----------------------------|
|EXTERNAL_ID           |Contributor email      |**YES**                     |
|FIRST_NAME            |Contributor name       |**YES**, extract first name |
|LAST_NAME             |Contributor name       |**YES**, extract last name  |
|EMAIL                 |Contributor email      |**YES**                     |


### Donation Table

|CiviCRM Field  |CP Field          |Required/Value    |
|---------------|------------------|------------------|
|EXTERNAL_ID    |Contributor email |**YES**           |
|INVOICE_NUMBER |Transaction ID    |No                |
|TOTAL_AMOUNT   |Total amount      |**YES**           |
|DATE_RECEIVED  |Date              |No                |
|FINANCIAL_TYPE |*n/a*             |`Donation`        |
|PAYMENT_METHOD |*n/a*             |`ConnectionPoint` |


### Membership Table

|CiviCRM Field        |CP Field          |Required/Value|
|---------------------|------------------|--------------|
|EXTERNAL_ID          |Contributor email |**YES**       |
|MEMBERSHIP_TYPE      |*n/a*             |`VCN Member`  |
|MEMBERSHIP_START_DATE|Date              |No            |

## Notes

- TODO: determine the date format
- header line is needed for the importing CP csv file
