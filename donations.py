#!/usr/bin/python
""" Create a CSV to import into CiviCRM from CanadaHelps output CSV.

Fields order or their availability are not an issue with this script. But *this*
*does not mean resulting csv file will import into CiviCRM successfully*.

To use this python script run:
~~~bash
python export.py ${canada_help_csv} ${export_folder}
~~~

If the script gives you a `_csv.Error: line contains NULL byte` error,
run the fllowing to remove null first.
~~~
tr -d '\000' < ${problem_file}  > ${use_file}
~~~

#Other info
- All text with "Anon" will becomes empty. This is a mean to reduces errors
- Anonoymous donation will go to the individual with "ANON" as the external id
- Anonoymous will not add into the contact import file
- If the field is not found or is "ANON", then field will be empty, except for
  total amount, which will be 0.00
- the date format can be either %Y/%m/%d '%Y-%m-%d'
"""

import csv
import sys
import datetime

# Fields to export, values are the fields in the CanadaHelps csv file
FORMAL_TITLE="DONOR TITLE"
FIRST_NAME="DONOR FIRST NAME" #REQUIRED
LAST_NAME="DONOR LAST NAME" #REQUIRED
COMPANY_NAME="DONOR COMPANY NAME"
ADDRESS="DONOR ADDRESS 1"
SUPPLEMENTAL_ADDRESS_1="DONOR ADDRESS 2"
CITY="DONOR CITY"
STATE="DONOR PROVINCE/STATE"
POSTAL_CODE="DONOR POSTAL/ZIP CODE"
COUNTRY="DONOR COUNTRY"
PHONE="DONOR PHONE NUMBER"
EMAIL="DONOR EMAIL ADDRESS" #REQUIRED

EXTERNAL_ID="DONOR EMAIL ADDRESS" #REQUIRED

INVOICE_NUMBER="TRANSACTION NUMBER"
TOTAL_AMOUNT="AMOUNT" #REQUIRED
DATE_RECEIVED="DONATION DATE"
SOURCE="DONATION SOURCE"
NOTE="MESSAGE TO CHARITY"

# Fields to export, values are the export value
FINANCIAL_TYPE = "Donation"

# Constants used in this file
IND_CONTACT_FILE = "/individual_contacts.csv"
IND_DONATION_FILE = "/individual_donations.csv"
ORG_CONTACT_FILE = "/organization_contacts.csv"
ORG_DONATION_FILE = "/organization_donations.csv"

ANON="ANON"


def export(fileName, outputFolder):
	""" Export the four files

	Arugment:
		fileName     -- (String) the input csv file path
		outputFolder -- (String) the output folder path
	"""
	ind_contacts = []
	ind_donations = []
	org_contacts = []
	org_donations =[]
	with open(fileName, 'rb') as csvFile:
		reader = csv.DictReader(csvFile)
		for row in reader:
			contact = []
			donation = []
			if row[COMPANY_NAME] == '':
				ind_contacts.append(fill_individual_contract(row))
				ind_donations.append(fill_donation(row))
			elif row[COMPANY_NAME].upper() == ANON:
				ind_donations.append(fill_donation(row, ANON))
			else:
				org_contacts.append(fill_organization_contract(row))
				org_donations.append(fill_donation(row))
	output_file(outputFolder + IND_CONTACT_FILE, ind_contacts)
	output_file(outputFolder + IND_DONATION_FILE, ind_donations)
	output_file(outputFolder + ORG_CONTACT_FILE, org_contacts)
	output_file(outputFolder + ORG_DONATION_FILE, org_donations)

def fill_individual_contract(row):
	""" Create a csv row for individual contact.

	Argument:
		row -- (Dictionary) the row extract data from
	"""
	contact = []
	contact.append(getField(row, EXTERNAL_ID))
	contact.append(getField(row, FORMAL_TITLE))
	contact.append(getField(row, FIRST_NAME))
	contact.append(getField(row, LAST_NAME))
	contact.append(getField(row, ADDRESS))
	contact.append(getField(row, SUPPLEMENTAL_ADDRESS_1))
	contact.append(getField(row, CITY))
	contact.append(getField(row, STATE))
	contact.append(getField(row, POSTAL_CODE))
	contact.append(getField(row, COUNTRY))
	contact.append(getField(row, PHONE))
	contact.append(getField(row, EMAIL))
	return contact

def fill_organization_contract(row):
	""" Create a csv row for organization contact.

	Argument:
		row -- (Dictionary) the row extract data from
	"""
	contact = []
	contact.append(getField(row, EXTERNAL_ID))
	contact.append(getField(row, COMPANY_NAME))
	contact.append(getField(row, ADDRESS))
	contact.append(getField(row, SUPPLEMENTAL_ADDRESS_1))
	contact.append(getField(row, CITY))
	contact.append(getField(row, STATE))
	contact.append(getField(row, POSTAL_CODE))
	contact.append(getField(row, COUNTRY))
	contact.append(getField(row, PHONE))
	contact.append(getField(row, EMAIL))
	return contact

def fill_donation(row, external=""):
	""" Create a csv row for donation.

	Argument:
		row -- (Dictionary) the row extract data from
	"""
	donation = []
	donation.append(getField(row, EXTERNAL_ID, external))
	donation.append(getField(row, INVOICE_NUMBER))

	amount_str = getField(row, TOTAL_AMOUNT, '0')
	amount_float = float(amount_str)
	donation.append("{:.2f}".format(amount_float))

	date_raw = getField(row, DATE_RECEIVED)
	try:
		date = datetime.datetime.strptime(date_raw, '%Y/%m/%d').strftime('%Y-%m-%d')
	except ValueError:
		datetime.datetime.strptime(date_raw, "%Y-%m-%d")
		date = date_raw
	donation.append(date)

	donation.append(getField(row, SOURCE))
	donation.append(getField(row, NOTE))
	donation.append(FINANCIAL_TYPE)
	return donation

def getField(row, field, default=""):
	if field in row:
		ans = row[field]
		if ans.upper() == ANON:
			return default
		return ans
	else:
		print(field)
		return default

def output_file(fileName, items):
	""" Output a csv file

	Argument:
		fileName -- (String) the csv file path
		items    -- (List)   list of items to export
	"""
	with open(fileName, 'wb') as csvFile:
		output = csv.writer(csvFile)
		for item in items:
			output.writerow(item)


def main(argv):
	""" The main method of this script

	This method will be called if this script is called from terminal

	Argument:
		argv -- program arguments
	"""
	if len(argv) == 2:
		export(argv[0], argv[1])
	elif len(argv) == 1:
		export(argv[0], ".")
	elif len(argv) == 0:
		export("CharityDataDownload.csv", ".")
	else:
		print("Usage: python export.py ${canada_help_csv} ${export_folder} # to store 4 files.")

if __name__ == '__main__':
	main(sys.argv[1:])
