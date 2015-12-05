#!/usr/bin/python

from __future__ import print_function

import MySQLdb
import DatabaseConnection


# Global variable to store the database object
DONORINFO_TABLE = "Individuals"
TRANSACTION_TABLE = "Money_Brought_In"

class DonorInfo:
    """ Class for a donor information """
    def __init__(self):
        self.firstName = ""
        self.lastName = ""
        self.address = ""
        self.city = ""
        self.province = ""
        self.postalCode = ""
        self.amountPaid = 0
        self.datePaid = '0000-00-00 00:00:00'

class DatabaseAccessObject:
    """ Class for the accessing database information """
    def __init__(self, databaseConnection):
        """Memorizes the connection in an attribute"""
        self.databaseConnection = databaseConnection

    # Private
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
        sql = "SELECT `ID #` FROM " + DONORINFO_TABLE + " WHERE `Last Name` = %s AND `First Name` = %s AND `Street Address` = %s;"
        getResult = dbCursor.execute(sql,(donorInfo.lastName, donorInfo.firstName, donorInfo.address))

        if getResult == 1: # exact match
            #return ID number
            data = dbCursor.fetchone()
            return data[0]
        else:
            return False
        """
        # This algorithm is to display all matching last name and will let the user input a choice
        else: # multiple match or no match
            sql = "SELECT `ID #`, `Last Name`, `First Name`, `Street Address` " + \
                "FROM " + DONORINFO_TABLE + " WHERE `Last Name` = %s"
            getResult = dbCursor.execute(sql, (donorInfo.lastName))

            # with multiple matches, display results so user can select the right account
            if getResult > 0:
                data = dbCursor.fetchall()
                counter = 1
                print ("#. Last Name, First Name, Address")
                for row in data:
                    print "%d. %s, %s, %s"%(counter, row[1], row[2], row[3])
                    counter += 1
                print ("Details from CSV file: \n %s, %s, %s" % (donorInfo.lastName, donorInfo.firstName, donorInfo.address))

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
            "`City`, `Province`, `Postal Code`) VALUES (%s, %s, %s, %s, %s, %s);"
        dbCursor.execute(sql, (donorInfo.firstName, donorInfo.lastName, donorInfo.address, donorInfo.city, donorInfo.province, donorInfo.postalCode))

        return self.__getDonorID(donorInfo)


    def __addTransactionDetails(self,donorID, donorInfo):
        """ Add the transaction details to the Money_Brought_In table """
        connection = self.databaseConnection.getConnection()
        if connection == 0:
            print ("No database connection yet")
            return False

        dbCursor = connection.cursor()

        # % signs in the STR_TO_DATE function must be escaped using %%, and quotes mu be escaped using \' 
        sql = "INSERT INTO " + TRANSACTION_TABLE + "(`ID #`, `Amount Payed`, `Date Payed`, `For`, `Cash`) " + \
            "VALUES (%s, %s, STR_TO_DATE(%s,\'%%m/%%d/%%Y\'), 'Donation', 0);"
    
        # Following lines used for debugging
        #print("Query is: %s",sql)
        #print("Date is "+donorInfo.datePaid)

        try:
            #dbCursor.execute(sql, (donorID, donorInfo.amountPaid, donorInfo.datePaid))
            dbCursor.execute(sql, (donorID, donorInfo.amountPaid, donorInfo.datePaid.strftime('%m/%d/%Y')))
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

        if self.__addTransactionDetails(donorID, donorDetails) == True:
            print ("Successful in adding transaction...")
            return True
        else:
            print ("Error in adding transaction for %s %s" % (donorDetails.firstName, donorDetails.lastName))

        return False
