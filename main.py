#!/usr/bin/python

import database
import csvFile

HOST = "localhost"
USERNAME = "root"
PASSWORD = ""
DATABASE = "Test"
CSV_FILENAME = "CharityDataDownload.csv"

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
def executeAddTransaction(csvFileName):
	csvObject = csvFile.openCsvFile("CharityDataDownload.csv")
	csvRecords = csvFile.getRecords(csvObject)

	database.connectToDB(HOST, USERNAME, PASSWORD, DATABASE)

	for csvRecord in csvRecords:
		donorInfo = changeCSVToDatabaseFormat(csvRecord)
		database.addTransactionToDatabase(donorInfo)

	database.closeDBConnection()

# Call the main command
executeAddTransaction(CSV_FILENAME)