#!/usr/bin/python
# CSV file related functions

from __future__ import print_function
from __future__ import with_statement

import csv
import pdb
# CONSTANTS
""" Constants for CSV file """
__CSV_TRANS_NUM__ = 0
__CSV_FIRST_NAME__ = 4
__CSV_LAST_NAME__ = 5
__CSV_ADDRESS__ = 7
__CSV_CITY__ = 9
__CSV_PROVINCE__ = 10
__CSV_POSTAL_CODE__ = 11
__CSV_LOGIN_ID__ = 13
__CSV_AMOUNT_PAID__ = 17
__CSV_DATE_PAID__ = 18
__CSV_TIME_PAID__ = 19
__CSV_WEBSITE__ = 23
__CSV_HOSTBY_VCN__ = 24
__CSV_PHONE_NUMBER__ = 25
__CSV_DELIMETER__ = ','

MAX_CHAR = 30

class CSVRecord:
    """ Class for a CSV row in the record """
    def __init__(self,infoRow,maxRow):
        self.transNum = infoRow[__CSV_TRANS_NUM__][:MAX_CHAR]
        self.firstName = infoRow[__CSV_FIRST_NAME__][:MAX_CHAR]
        self.lastName = infoRow[__CSV_LAST_NAME__][:MAX_CHAR]
        self.address = infoRow[__CSV_ADDRESS__][:MAX_CHAR]
        self.city = infoRow[__CSV_CITY__][:MAX_CHAR]
        self.province = infoRow[__CSV_PROVINCE__][:MAX_CHAR]
        self.postalCode = infoRow[__CSV_POSTAL_CODE__][:MAX_CHAR]
        self.amountPaid = infoRow[__CSV_AMOUNT_PAID__][:MAX_CHAR]
        self.datePaid = infoRow[__CSV_DATE_PAID__][:MAX_CHAR]
        self.timePaid = infoRow[__CSV_TIME_PAID__][:MAX_CHAR]
        self.loginID = infoRow[__CSV_LOGIN_ID__][:MAX_CHAR]
        if maxRow >= 25:
            self.host_by_vcn = infoRow[__CSV_HOSTBY_VCN__][:MAX_CHAR]
            self.webSite = infoRow[__CSV_WEBSITE__][:MAX_CHAR]
            self.phoneNumber = infoRow[__CSV_PHONE_NUMBER__][:MAX_CHAR]
# Main APIs
def openCsvFile(filename):
    """ Return the CSV file as an iterator object """

    try:
        csvFile = open(filename, 'rb')
    except IOError:
        print ("Error in opening/reading CSV file. Check if file exists...")
        return False

    csvOutput = csv.reader(csvFile, delimiter=__CSV_DELIMETER__)

    return csvOutput


def openCsvWriter(filename):
    """ Returns a csv writer pointing to the CSV file filename"""

    try:
        outputCsvFile = open(filename, 'wb')
    except IOError:
        print ("Error in opening output CSV file.")
        return False, False

    csvOutput = csv.writer(outputCsvFile, delimiter=__CSV_DELIMETER__)

    return csvOutput,outputCsvFile

def getRecords(csvObject):
    """ Return the list of records found inside the CSV file """
    csvRecords = []
    for row in csvObject:
        csvRecords.append(CSVRecord(row))
    del csvRecords[0] #Delete the first row containing the row labels
    return csvRecords


def getRows(filename):
    """ Return the list of complete records found inside the CSV file
    and closes any file resource """

    csvRows = []

    try:
        with open(filename, 'rb') as csvFile:
            csvInput = csv.reader(csvFile, delimiter=__CSV_DELIMETER__)
            for row in csvInput:
                if row is not None:
                    csvRows.append(row)
    except IOError:
        print ("Error in opening/reading CSV file. Check if file exists...")
        return False

    return csvRows
