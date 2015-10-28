#!/usr/bin/python

import database
import csvFile
import getpass

DEFAULT_HOST 		= "localhost"
DEFAULT_USER 		= "ralph"
#stub-start
#erase this!
DEFAULT_PASS 		= "helloWorld_1!"
#stub-end
DEFAULT_DBNAME 		= "Money"
DEFAULT_CSVFILENAME = "CharityDataDownload.csv"

def changeCSVToDatabaseFormat(csvRecord):
	""" Change the CSV format to a more suitable format for database addition """

	donorInfo = database.DonorInfo()
	donorInfo.firstName = csvRecord.firstName
	donorInfo.lastName = csvRecord.lastName
	donorInfo.address = csvRecord.address
	donorInfo.city = csvRecord.city
	donorInfo.province = csvRecord.province
	donorInfo.postalCode = csvRecord.postalCode
	donorInfo.amountPaid = float(csvRecord.amountPaid)
	donorInfo.datePaid = csvRecord.datePaid

	return donorInfo

# Main method
def executeAddTransaction(csvFileName, dbInfo):

	csvObject = csvFile.openCsvFile(csvFileName)
	if csvObject == False:
		return False
	csvRecords = csvFile.getRecords(csvObject)

	for csvRecord in csvRecords:
		donorInfo = changeCSVToDatabaseFormat(csvRecord)
		database.addTransactionToDatabase(donorInfo, dbInfo)

# Call the main command
raw_host = raw_input("Input the host name of the database (e.g. <IP Address of the server>): ")
raw_user = raw_input("Input the username of the database (e.g. root): ")
raw_pass = getpass.getpass("Input the password of the database: ")
raw_dbname = raw_input("Input the database name: ")
raw_csvFilename = raw_input("Input the CSV file name (Include the file extension): ")

#Default Input of values
if raw_host == "":
	raw_host = DEFAULT_HOST
if raw_user == "":
	raw_user = DEFAULT_USER
if raw_pass == "":
	raw_pass = DEFAULT_PASS
if raw_dbname == "":
	raw_dbname = DEFAULT_DBNAME
if raw_csvFilename == "":
	raw_csvFilename = DEFAULT_CSVFILENAME

databaseInfo = database.DatabaseInfo(raw_host,raw_user,raw_pass,raw_dbname)
executeAddTransaction(raw_csvFilename, databaseInfo)
