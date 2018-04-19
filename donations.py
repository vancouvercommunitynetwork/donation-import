#!/bin/usr/python
""" Create a CSV to import into CiviCRM from CanadaHelps output CSV.

Fields order or their existances are not an issue with this script. But this
does not mean resulting csv file will import into CiviCRM successfully.
"""

import csv
import sys
import datetime

# Fields to export
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
			if row[COMPANY_NAME] == '' or row[COMPANY_NAME] == 'Anon':
				ind_contacts.append(fill_individual_contract(row))
				ind_donations.append(fill_donation(row))
			else:
				org_contacts.append(fill_organization_contract(row))
				org_donations.append(fill_donation(row))
	output_file(outputFolder + "/individual_contracts.csv", ind_contacts)
	output_file(outputFolder + "/individual_donations.csv", ind_donations)
	output_file(outputFolder + "/organization_contracts.csv", org_contacts)
	output_file(outputFolder + "/organization_donations.csv", org_donations)

def fill_individual_contract(row):
	""" Create a csv row for individual contact.

	Argument:
		row -- (Dictionary) the row extract data from
	"""
	contact = []
	contact.append(row[EXTERNAL_ID])
	contact.append(row[FORMAL_TITLE])
	contact.append(row[FIRST_NAME])
	contact.append(row[LAST_NAME])
	contact.append(row[ADDRESS])
	contact.append(row[SUPPLEMENTAL_ADDRESS_1])
	contact.append(row[CITY])
	contact.append(row[STATE])
	contact.append(row[POSTAL_CODE])
	contact.append(row[COUNTRY])
	contact.append(row[PHONE])
	contact.append(row[EMAIL])
	return contact

def fill_organization_contract(row):
	""" Create a csv row for organization contact.

	Argument:
		row -- (Dictionary) the row extract data from
	"""
	contact = []
	contact.append(row[EXTERNAL_ID])
	contact.append(row[COMPANY_NAME])
	contact.append(row[ADDRESS])
	contact.append(row[SUPPLEMENTAL_ADDRESS_1])
	contact.append(row[CITY])
	contact.append(row[STATE])
	contact.append(row[POSTAL_CODE])
	contact.append(row[COUNTRY])
	contact.append(row[PHONE])
	contact.append(row[EMAIL])
	return contact

def fill_donation(row):
	""" Create a csv row for donation.

	Argument:
		row -- (Dictionary) the row extract data from
	"""
	donation = []
	donation.append(row[EXTERNAL_ID])
	donation.append(row[INVOICE_NUMBER])
	donation.append(row[TOTAL_AMOUNT])
	date = datetime.datetime.strptime(row[DATE_RECEIVED], '%Y/%m/%d').strftime('%Y-%m-%d')
	donation.append(date)
	donation.append(row[SOURCE])
	donation.append(row[NOTE])
	donation.append("Donation")
	return donation

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
	else:
		print("Usage: python export.py ${canada_help_csv} ${import_folder} # to store 4 files.")

if __name__ == '__main__':
	main(sys.argv[1:])
