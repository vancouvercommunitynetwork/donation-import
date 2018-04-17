#!/bin/usr/python

import csv
import sys

# Fields to export
FORMAL_TITLE="DONOR TITLE"
FIRST_NAME="DONOR FIRST NAME"
LAST_NAME="DONOR LAST NAME"
COMPANY_NAME="DONOR COMPANY NAME"
ADDRESS="DONOR ADDRESS 1"
SUPPLEMENTAL_ADDRESS_1="DONOR ADDRESS 2"
CITY="DONOR CITY"
STATE="DONOR PROVINCE/STATE"
POSTAL_CODE="DONOR POSTAL/ZIP CODE"
COUNTRY="DONOR COUNTRY"
PHONE="DONOR PHONE NUMBER"
EMAIL="DONOR EMAIL ADDRESS"

EXTERNAL_ID="DONOR EMAIL ADDRESS"

INVOICE_NUMBER="TRANSACTION NUMBER"
TOTAL_AMOUNT="AMOUNT"
DATE_RECEIVED="DONATION DATE"
SOURCE="DONATION SOURCE"
NOTE="MESSAGE TO CHARITY"

# the order and which fields to export
INDIVIDUAL_CONTACT=(EXTERNAL_ID, FORMAL_TITLE, FIRST_NAME, LAST_NAME, ADDRESS, SUPPLEMENTAL_ADDRESS_1, CITY, STATE, POSTAL_CODE, COUNTRY, PHONE, EMAIL)
INDIVIDUAL_DONATION=(EXTERNAL_ID, INVOICE_NUMBER, TOTAL_AMOUNT, DATE_RECEIVED, SOURCE, NOTE)
ORGANIZATION_CONTACT=(EXTERNAL_ID, COMPANY_NAME, ADDRESS, SUPPLEMENTAL_ADDRESS_1, CITY, STATE, POSTAL_CODE, COUNTRY, PHONE, EMAIL)
ORGANIZATION_DONATION=(EXTERNAL_ID, INVOICE_NUMBER, TOTAL_AMOUNT, DATE_RECEIVED, SOURCE, NOTE)

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
				ind_contacts.append(fillList(row, INDIVIDUAL_CONTACT))
				ind_donations.append(fillList(row, INDIVIDUAL_DONATION))
			else:
				org_contacts.append(fillList(row, ORGANIZATION_CONTACT))
				org_donations.append(fillList(row, ORGANIZATION_DONATION))
	outputFile(outputFolder + "/individual_contracts.csv", ind_contacts)
	outputFile(outputFolder + "/individual_donations.csv", ind_donations)
	outputFile(outputFolder + "/organization_contracts.csv", org_contacts)
	outputFile(outputFolder + "/organization_donations.csv", org_donations)

def fillList(row, keys):
	""" Create a list with the database row and list of table key

	Argument:
		row  -- (Dictionary) the row of database
		keys -- (List)       the keys to extract the data
	"""

	answer = []
	for key in keys:
		if key in row:
			answer.append(row[key])
		else:
			answer.append("")
	return answer

def outputFile(fileName, items):
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
