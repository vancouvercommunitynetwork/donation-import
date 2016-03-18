#!/usr/bin/python

from DatabaseConnection import DatabaseConnection
import database
import csvFile
#import getpass

from datetime import datetime

# import of module to parse configuration files
# note that the module name will change  to configparser for Python3
import ConfigParser

CONFIGURATION_FILE    = "donation_import.cfg"
DEFAULT_HOST         = "localhost"
DEFAULT_USER         = "root"
#stub-start
#erase this!
DEFAULT_PASS         = "password"
#stub-end
DEFAULT_DBNAME         = "Money"
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
    csvErrorFileName = config.get('csvFile','csvErrorFileName')

    # Following line is only used for debugging
    #print(",".join((host,userName,password,dbName,csvFileName)))

    return (host,userName,password,dbName,csvFileName,csvErrorFileName)


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
    donorInfo.loginID = getLoginID(csvRecord.loginID)
    donorInfo.transNum = csvRecord.transNum

    return donorInfo

def getLoginID(p_loginID):
    if p_loginID[-10:] == '@vcn.bc.ca':
        new_p_loginID = p_loginID[:-10]
        return new_p_loginID
    elif p_loginID == 'ANON':
        return '000'

    return p_loginID


def to_right_date_format(p_date,p_time):
    p_date = p_date.split()[0]
    p_date = p_date.split('/')
    p_date.reverse()
    p_date = "-".join(p_date)
    p_time = datetime.strptime(p_time.split()[1], "%H:%M:%S")

    new_time = p_date + ' ' + p_time.strftime("%H:%M:%S")
    return new_time

# Main function
def executeAddTransaction(csvFileName, DAO, csvOutputWriter):
    """Processes content of csvFileName row by row
    and uses DAO object to perform database updates
    Records that cannot be processed are output to csvOutputWriter"""

    # read all the rows from the input CSV file into an iterable
    csvRows = csvFile.getRows(csvFileName)

    if not(csvRows) or not(csvOutputWriter) :
        print("input or output CSV file cannot be opened.\nProcessing stopped.")
        return
    #csvObject = csvFile.openCsvFile(csvFileName)
    #if csvObject == False:
    #    return False
    #csvRecords = csvFile.getRecords(csvObject)

    for i, csvRow in enumerate(csvRows):
        if(i>0):
            try:
                csvRecord = csvFile.CSVRecord(csvRow)
                donorInfo = changeCSVToDatabaseFormat(csvRecord)
                DAO.addTransactionToDatabase(donorInfo)
            except ValueError as e:
                csvOutputWriter.writerow(csvRow)
                print("Conversion Error:\n{0}\nwhen dealing with record:{1}".format(e, csvRow))
            except KeyboardInterrupt as e:
                csvOutputWriter.writerow(csvRow)
                print("Operation interrupted by operator while dealing with record:{1}".format(csvRow))
                raise # we re-raise keyboard interruption to allow interruption of the program
            except Exception as e:
                csvOutputWriter.writerow(csvRow)
                print("Program met Exception: {0} when dealing with record {1}".format(e, csvRow))
        else: #i=0
            # the first rows contains the headers, which we just copy
            # to the output CSV file
            csvOutputWriter.writerow(csvRow)


# Call the main command

# Read the configuration file
(raw_host,raw_user,raw_pass,raw_dbname,raw_csvFilename,csvErrorFileName) = readConfigurationFile(CONFIGURATION_FILE)
# Establish the database connection
databaseConnection = DatabaseConnection(raw_host,raw_user,raw_pass,raw_dbname)
#Create a database Access Object that will use the database connection
databaseAccessObject = database.DatabaseAccessObject(databaseConnection)
# Open output CSV file
csvOutputWriter,csvOutputFile = csvFile.openCsvWriter(csvErrorFileName)
# Process the transactions
executeAddTransaction(raw_csvFilename, databaseAccessObject, csvOutputWriter)
#Close the database connection
databaseConnection.closeConnection()
# close the output file
if csvOutputFile:
    csvOutputFile.close()
