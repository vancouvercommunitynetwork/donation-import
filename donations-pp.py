#!/usr/bin/python
""" Create a CSV to import into CiviCRM from PayPal output CSV.

Fields order or their availability are not an issue with this script. But *this*
*does not mean resulting csv file will import into CiviCRM successfully*.

To use this python script run:
~~~bash
python export.py ${paypal_csv} ${export_folder}
~~~

#Other info
- the date format seems to be %d/%m/%Y
- header line is needed for the importing PayPal csv file
"""

import os
import csv
import sys
import datetime
import tempfile

# Fields to export==============================================================
# Variable names are the name that the fields should import into

# The values here are the files in the PayPal csv file

PAYOUT_DATE="Payout Date"
DONATION_DATE="Donation Date"
FIRST_NAME="Donor First Name" #REQUIRED
LAST_NAME="Donor Last Name" #REQUIRED
EMAIL="Donor Email" #REQUIRED
PROGRAM_NAME="Program Name"
REFERENCE="Reference Information"
CURRENCY="Currency Code"
GROSS_AMOUNT="Gross Amount" #REQUIRED
TOTAL_FEES="Total Fees"
NET_AMOUNT="Net Amount"
TRANSACTION_ID="Transaction ID"

EXTERNAL_ID="Donor Email" #REQUIRED

# Values used the export value
FINANCIAL_TYPE = "Donation" #REQUIRED
PAYMENT_METHOD = "PayPal"
MEMBERSHIP_TYPE = "VCN Member"

# Constants used in this file===================================================
IND_CONTACT_FILE = "/individual_contacts.csv"
IND_DONATION_FILE = "/individual_donations.csv"
MEMBERSHIP_FILE = "/memberships.csv"

MEMBERSHIP_MIN_AMOUNT = 15

INPUT_DATE_FORMATS = ['%d/%m/%Y']
OUTPUT_DATE_FORMAT = '%Y-%m-%d'

# Main export function==========================================================

def export(fileName, outputFolder):
	""" Export the four files

	Arugment:
		fileName     -- (String) the input csv file path
		outputFolder -- (String) the output folder path
	"""
	if not(os.path.exists(outputFolder)):
		os.makedirs(outputFolder)

	# output list
	ind_contacts = []
	ind_donations = []
	memberships = []

	with open(fileName, 'rb') as ppFile: # open export file
		with tempfile.TemporaryFile() as csvFile: # open write file
			# takes the export file and do the following things:
			# - change the uncoding from utf-8 BOM to utf-8
			# - remove all the null characters
			# - save the file so the csv.DictReader can reopen it and read it
			csvFile.write(ppFile.read().decode("utf-8-sig").encode("utf-8").replace('\x00', ''))
			csvFile.seek(0)

			# exctract file into a dictionary
			reader = csv.DictReader(csvFile)
			for row in reader:
				ind_contacts.append(fill_individual_contract(row))
				ind_donations.append(fill_donation(row))
				if float(row[GROSS_AMOUNT]) >= MEMBERSHIP_MIN_AMOUNT:
					memberships.append(fill_membership(row))

	# output files
	output_file(outputFolder + IND_CONTACT_FILE, ind_contacts)
	output_file(outputFolder + IND_DONATION_FILE, ind_donations)
	output_file(outputFolder + MEMBERSHIP_FILE, memberships)

# Array filling functions ======================================================

def fill_individual_contract(row):
	""" Create a csv row for individual contact.

	Argument:
		row -- (Dictionary) the row extract data from
	Return:    (Array)      a line for the csv file
	"""
	contact = []
	contact.append(getField(row, EXTERNAL_ID))
	# name
	contact.append(getField(row, FIRST_NAME))
	contact.append(getField(row, LAST_NAME))
	# email
	contact.append(getField(row, EMAIL))
	return contact

def fill_donation(row, external=""):
	""" Create a csv row for donation.

	Argument:
		row -- (Dictionary) the row extract data from
	Return:    (Array)      a line for the csv file
	"""
	donation = []
	donation.append(getField(row, EXTERNAL_ID, external))
	donation.append(getField(row, TRANSACTION_ID))
	# amount - get number as string -> convert to float -> insert with format
	amount_str = getField(row, GROSS_AMOUNT, '0')
	amount_float = float(amount_str)
	donation.append("{:.2f}".format(amount_float))
	# date - get date as string, try different formats
	date = convert_date(getField(row, DONATION_DATE))
	donation.append(date)
	# other exporting values
	donation.append(FINANCIAL_TYPE)
	donation.append(PAYMENT_METHOD)
	return donation

def fill_membership(row):
	""" Create a csv row for membership.

	Argument:
		row -- (Dictionary) the row extract data from
	Return:    (Array)      a line for the csv file
	"""
	membership = []
	membership.append(getField(row, EXTERNAL_ID))
	membership.append(MEMBERSHIP_TYPE)
	date = convert_date(getField(row, DONATION_DATE))
	membership.append(date)
	return membership

# Other Helper Functions========================================================

def getField(row, field, default=""):
	""" Gets the field

	Argument:
		row     -- (Dictionary) the row extract data from
		field   -- (String)     the field name
		default -- (String)     the default value
	Return:        (String)     the value from the `row` dictionary
	"""
	if field in row:
		return row[field]
	else:
		print ("Missing Field: \"" + field + "\". Exporting as \"" + default + "\".")
		# print (row)
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

def today_date_folder():
	today = datetime.date.today()
	return today.strftime("%Y-%m-%d")

def convert_date(input_date_str):
	""" Convert a date string from the input file into a date string for the output file

	Argument:
		input_date_str -- (String)     the date string from the input fileName
	Return:               (String)     the date string to be used for the output file
	"""
	for input_format in INPUT_DATE_FORMATS:
		try:
			input_date = datetime.datetime.strptime(input_date_str, input_format)
			# stop if the format matched
			break
		except ValueError:
			# move on to the next format
			pass
	output_date_str = input_date.strftime(OUTPUT_DATE_FORMAT)
	return output_date_str

# Main Functions================================================================

def main(argv):
	""" The main method of this script

	This method will be called if this script is called from terminal

	Argument:
		argv -- program arguments
	"""
	if len(argv) == 2:
		export(argv[0], argv[1])
	elif len(argv) == 1:
		export(argv[0], today_date_folder())
	elif len(argv) == 0:
		export("CharityDataDownload.csv", today_date_folder())
	else:
		print("Usage: python export.py ${paypal_csv} ${export_folder} # to store 4 files.")

if __name__ == '__main__':
	# Don't run if this file is imported by another pythong script
	main(sys.argv[1:])
