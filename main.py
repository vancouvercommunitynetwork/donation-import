#!/usr/bin/python

import database
import csvFile
import getpass
from datetime import datetime
# import of module to parse configuration files
# note that the module name will change  to configparser for Python3
import ConfigParser

CONFIGURATION_FILE	= "donation_import.cfg"
DEFAULT_HOST 		= "localhost"
DEFAULT_USER 		= "root"
#stub-start
#erase this!

#stub-end
DEFAULT_DBNAME 		= "Money"
DEFAULT_CSVFILENAME = "CharityDataDownload.csv"

def readConfigurationFile(file):
	"""Reads database and csv file parameters from a given file """
	databaseSectionName = 'database';
	config = ConfigParser.ConfigParser()
	config.read('donation_import.cfg')
	host = config.get(databaseSectionName,'host')
	userName = config.get(databaseSectionName,'userName')
	password = config.get(databaseSectionName,'password')
	dbName = config.get(databaseSectionName,'dbName')

	csvFileName = config.get('csvFile','csvFileName')

	# Following l, "%H:%M %p"
	return (host,userName,password,dbName,csvFileName)


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
	donorInfo.datePaid = to_right_date_format(csvRecord.datePaid,csvRecord.timePaid)

	return donorInfo


def to_right_date_format(p_date,p_time):
	p_time = datetime.strptime(p_time, "%H:%M %p")
	new_time = p_date + ' ' + p_time.strftime("%H:%M:%S")
	return new_time


# Main function
def executeAddTransaction(csvFileName, dbInfo):

	csvObject = csvFile.openCsvFile(csvFileName)
	if csvObject == False:
		return False
	csvRecords = csvFile.getRecords(csvObject)

	for csvRecord in csvRecords:
		donorInfo = changeCSVToDatabaseFormat(csvRecord)
		database.addTransactionToDatabase(donorInfo, dbInfo)


# Call the main command

(raw_host,raw_user,raw_pass,raw_dbname,raw_csvFilename) = readConfigurationFile(CONFIGURATION_FILE)

databaseInfo = database.DatabaseInfo(raw_host,raw_user,raw_pass,raw_dbname)

executeAddTransaction(raw_csvFilename, databaseInfo)
