#!/usr/bin/python
# CSV file related functions

from __future__ import print_function
from __future__ import with_statement

import csv

# CONSTANTS
""" Constants for CSV file """
__CSV_FIRST_NAME__ = 4
__CSV_LAST_NAME__ = 5
__CSV_ADDRESS__ = 7
__CSV_CITY__ = 9
__CSV_PROVINCE__ = 10
__CSV_POSTAL_CODE__ = 11
__CSV_AMOUNT_PAID__ = 17
__CSV_DATE_PAID__ = 18
__CSV_DELIMETER__ = ','

class CSVRecord:
   """ Class for a CSV row in the record """
   def __init__(self,infoRow):
      self.firstName = infoRow[__CSV_FIRST_NAME__]
      self.lastName = infoRow[__CSV_LAST_NAME__]
      self.address = infoRow[__CSV_ADDRESS__]
      self.city = infoRow[__CSV_CITY__]
      self.province = infoRow[__CSV_PROVINCE__]
      self.postalCode = infoRow[__CSV_POSTAL_CODE__]
      self.amountPaid = infoRow[__CSV_AMOUNT_PAID__]
      self.datePaid = infoRow[__CSV_DATE_PAID__]

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
                csvRows.append(row)
    except IOError:
        print ("Error in opening/reading CSV file. Check if file exists...")
        return False

    return csvRows
