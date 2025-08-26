# Donation Import from ConnectionPoint

This script requires Python 3.

## Input CSV file

The CSV file must have the following:

|CP Field              |Required For                                                                                                                         |
|----------------------|-------------------------------------------------------------------------------------------------------------------------------------|
|Date                  |[Donation Table](#donation-table)<br/>[Membership Table](#membership-table)                                                          |
|Contribution amount   |[Donation Table](#donation-table)                                                                                                    |
|Total amount          |                                                                                                                                     |
|Net amount            |                                                                                                                                     |
|Currency              |                                                                                                                                     |
|Payment status        |                                                                                                                                     |
|Transaction ID        |[Donation Table](#donation-table)                                                                                                    |
|Processed by          |                                                                                                                                     |
|Contact email         |[Individual Contact Table](#individual-contact-table)<br/>[Donation Table](#donation-table)<br/>[Membership Table](#membership-table)|
|First name            |[Individual Contact Table](#individual-contact-table)                                                                                |
|Last name             |[Individual Contact Table](#individual-contact-table)                                                                                |
|Message               |[Donation Table](#donation-table)                                                                                                    |
|Show name             |                                                                                                                                     |
|Show amount           |                                                                                                                                     |
|Subscribe to updates  |                                                                                                                                     |

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
	- export for Import Contact with the mapping "FundRazr Individuals",
	- fields follows [Individual Contact Table](#individual-contact-table)
- ${export_folder}/individual_donations.csv
	- export for Import Contact with the mapping "FundRazr Individuals Donations"
	- fields follows [Donation Table](#donation-table)
- ${export_folder}/memberships.csv
	- export for Import Memberships with the mapping "FundRazr Donations"
	- fields follows [Membership Table](#membership-table)

### Individual Contact Table

|CiviCRM Field         |CP Field      |Required|
|----------------------|--------------|--------|
|EXTERNAL_ID           |Contact email |**YES** |
|FIRST_NAME            |First name    |**YES** |
|LAST_NAME             |Last name     |**YES** |
|EMAIL                 |Contact email |**YES** |


### Donation Table

|CiviCRM Field  |CP Field            |Required/Value    |
|---------------|--------------------|------------------|
|EXTERNAL_ID    |Contact email       |**YES**           |
|INVOICE_NUMBER |Transaction ID      |No                |
|TOTAL_AMOUNT   |Contribution amount |**YES**           |
|DATE_RECEIVED  |Date                |No                |
|NOTE           |Message             |No                |
|FINANCIAL_TYPE |*n/a*               |`Donation`        |
|PAYMENT_METHOD |*n/a*               |`ConnectionPoint` |


### Membership Table

|CiviCRM Field         |CP Field          |Required/Value|
|----------------------|------------------|--------------|
|EXTERNAL_ID           |Contact email     |**YES**       |
|MEMBERSHIP_TYPE       |*n/a*             |`VCN Member`  |
|MEMBERSHIP_START_DATE |Date              |No            |

## Notes

- TODO: determine the date format
- header line is needed for the importing CP csv file
