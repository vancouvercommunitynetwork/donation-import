#!/usr/bin/python

from __future__ import print_function

import MySQLdb
import datetime

import DatabaseConnection
import pdb


# Global variable to store the database object
DONORINFO_TABLE = "Individuals"
TRANSACTION_TABLE = "Money_Brought_In"

MAX_CHAR = 30

class DonorInfo:
    """ Class for a donor information """
    def __init__(self,maxRow):
        self.transNum = "000000000"
        self.firstName = ""
        self.lastName = ""
        self.address = ""
        self.city = ""
        self.province = ""
        self.postalCode = ""
        self.amountPaid = 0
        self.datePaid = '0000-00-00 00:00:00'
        self.loginID = 'xxxx@vcn.bc.ca'
        self.webSite = ''
        self.host_by_vcn = 0
        self.phoneNumber = ''
class DatabaseAccessObject:
    """ Class for the accessing database information """
    def __init__(self, databaseConnection):
        """Memorizes the connection in an attribute"""
        self.databaseConnection = databaseConnection

    # Private
    def __getTransID(self,donorID,donorInfo):
        """ Returns a transaction ID if there is an exact match for ID,
        date and amount for a credit card"""
        # skip validation and adding to database if no transNum
        if donorInfo.transNum == None:
            return True


        connection = self.databaseConnection.getConnection()
        if connection == 0:
            print ("No database connection yet")
            return False

        dbCursor = connection.cursor()
        sql = "SELECT* FROM " + TRANSACTION_TABLE + " WHERE `Paper Receipt` = %s;"
        getResult = dbCursor.execute(sql,(donorInfo.transNum))
        if getResult != 0: # exact match
            #return ID number
            data = dbCursor.fetchone()
            return data[0]
        else:
            return False


    def __updateDonor(self,donorInfo):
        if donorInfo.phoneNumber == '' and donorInfo.webSite == '':
            return False
        connection = self.databaseConnection.getConnection()
        if connection == 0:
            print ("No database connection yet")
            return False

        dbCursor = connection.cursor()
        sql = "SELECT* FROM " + DONORINFO_TABLE + " WHERE `First Name` = %s AND `Last Name` = %s AND `Street Address` = %s AND `City` = %s AND `Province` = %s AND `Postal Code` = %s AND `URL` = %s AND `Phone (Home)` = %s AND `Host with VCN` = %s;"
        getResult = dbCursor.execute(sql,( donorInfo.firstName, donorInfo.lastName, donorInfo.address, donorInfo.city, donorInfo.province, donorInfo.postalCode, donorInfo.webSite,donorInfo.phoneNumber,donorInfo.host_by_vcn))
        if getResult == 0:
            # pdb.set_trace()
            sql = "UPDATE Individuals SET `URL`= %s, `Phone (Home)`= %s, `Host with VCN` = %s WHERE `First Name` = %s AND `Last Name` = %s AND `Street Address` = %s AND `City` = %s AND `Province` = %s AND `Postal Code` = %s "
            getResult = dbCursor.execute(sql,(donorInfo.webSite, donorInfo.phoneNumber,donorInfo.host_by_vcn, donorInfo.firstName, donorInfo.lastName[:MAX_CHAR], donorInfo.address, donorInfo.city, donorInfo.province, donorInfo.postalCode ))
            return True
        return False;



    def __getDonorID(self,donorInfo):
        """ Return the ID# of the donor if the account exists already
        - Matching is done by checking if the last and first name and address
        matches the information from the database. If not, the program will
        output all of the donors that matches the last name. The user will
        then be prompted to select which of the donor he/she chooses to use
        for the transaction.
        """
        connection = self.databaseConnection.getConnection()
        if connection == 0:
            print ("No database connection yet")
            return False

        dbCursor = connection.cursor()

        sql = "SELECT* FROM " + DONORINFO_TABLE + " WHERE `First Name` = %s AND `Last Name` = %s AND `Street Address` = %s AND `City` = %s AND `Province` = %s AND `Postal Code` = %s;"
        getResult = dbCursor.execute(sql,( donorInfo.firstName, donorInfo.lastName[:MAX_CHAR], donorInfo.address, donorInfo.city, donorInfo.province, donorInfo.postalCode))

        if getResult != 0:

            #return ID number
            data = dbCursor.fetchone()
            if self.__updateDonor(donorInfo):
                print("Donor updated")
            return data[0]
        else:
            return False
        """
        # This algorithm is to display all matching last name and will let the user input a choice
        else: # multiple match or no match
            sql = "SELECT `ID #`, `Last Name`, `First Name`, `Street Address` " + \
                "FROM " + DONORINFO_TABLE + " WHERE `Last Name` = %s"
            getResult = dbCursor.execute(sql, (donorInfo.lastName[:MAX_CHAR]))

            # with multiple matches, display results so user can select the right account
            if getResult > 0:
                data = dbCursor.fetchall()
                counter = 1
                print ("#. Last Name, First Name, Address")
                for row in data:
                    print "%d. %s, %s, %s"%(counter, row[1], row[2], row[3])
                    counter += 1
                print ("Details from CSV file: \n %s, %s, %s" % (donorInfo.lastName[:MAX_CHAR], donorInfo.firstName, donorInfo.address))

                raw_choice = raw_input("Input your choice (0 if none of the above): ")

                if raw_choice > 0:
                    return data[raw_choice - 1][0]
                else:
                    # no match from the database results
                    return False

            # no match at all for last name
            else:
                return False
        """

    def __createDonor(self,donorInfo):
        """ Returns the ID number of the created Donor """
        connection = self.databaseConnection.getConnection()
        if connection == 0:
            print ("No database connection yet")
            return False

        dbCursor = connection.cursor()



        sql = "INSERT INTO " + DONORINFO_TABLE + "(`First Name`, `Last Name`, `Street Address`, " + \
            "`City`, `Province`, `Postal Code`,`URL`,`Phone (Home)`,`Host with VCN`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s,%s);"
        dbCursor.execute(sql, (donorInfo.firstName, donorInfo.lastName[:MAX_CHAR], donorInfo.address, donorInfo.city, donorInfo.province, donorInfo.postalCode, donorInfo.webSite,donorInfo.phoneNumber,donorInfo.host_by_vcn))

        return self.__getDonorID(donorInfo)


    def __addTransactionDetails(self,donorID, donorInfo):
        """ Add the transaction details to the Money_Brought_In table """
        connection = self.databaseConnection.getConnection()
        if connection == 0:
            print ("No database connection yet")
            return False

        dbCursor = connection.cursor()

        # % signs in the STR_TO_DATE function must be escaped using %%, and quotes mu be escaped using \'
        sql = "INSERT INTO " + TRANSACTION_TABLE + "(`ID #`, `Amount Payed`, `Date Payed`, `For`, `Cash`, `Main Login Id`, `Paper Receipt`) " + \
            "VALUES (%s, %s, STR_TO_DATE(%s,'%%Y-%%m-%%d %%r'), 'Credit Card', 0, %s, %s);"

        # Following lines used for debugging
        #print("Query is: %s",sql)
        #print("Date is "+donorInfo.datePaid)

        try:
            dbCursor.execute(sql, (donorID, donorInfo.amountPaid, donorInfo.datePaid,donorInfo.loginID,donorInfo.transNum))
            #print ("Date is "+ donorInfo.datePaid)
            return True
        except MySQLdb.Error, e:
            print ("Error %d: %s", e.args[0], e.args[1])
            return False


    # MAIN APIs
    def addTransactionToDatabase(self, donorDetails):
        """Processes the donation information and creates necessary records"""
        donorID = self.__getDonorID(donorDetails)

        if donorID == False:
            donorID = self.__createDonor(donorDetails)
            print("Donor created")

        if self.__getTransID(donorID, donorDetails) == False:
            if self.__addTransactionDetails(donorID, donorDetails) == True:
                print ("Successful in adding transaction...")
                return True
            else:
                print ("Error in adding transaction for %s %s" % (donorDetails.firstName, donorDetails.lastName))

        return False
