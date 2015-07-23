#!/usr/bin/python

import database
import csvFile

def changeCSVToDatabaseFormat(csvRecord):
	""" Change the CSV format to a more suitable format for database addition """

	donorInfo = database.DonorInfo()
	donorInfo.firstName = csvRecord.firstName
	donorInfo.lastName = csvRecord.lastName
	donorInfo.address = csvRecord.address
	donorInfo.city = csvRecord.city
	donorInfo.province = csvRecord.province
	donorInfo.postalCode = csvRecord.postalCode
	donorInfo.amountPaid = int(csvRecord.amountPaid)
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
raw_pass = raw_input("Input the password of the database: ")
raw_dbname = raw_input("Input the database name: ")
raw_csvFilename = raw_input("Input the CSV file name (Include the file extension): ")
databaseInfo = database.DatabaseInfo(raw_host,raw_user,raw_pass,raw_dbname)
executeAddTransaction(raw_csvFilename, databaseInfo)