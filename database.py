#!/usr/bin/python

from __future__ import print_function

import MySQLdb
import datetime
import datetime
# Global variable to store the database object
globalDB = 0
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
class DatabaseInfo:
	""" Class for the database information """
	def __init__(self, host, username, password, databaseName):
		self.host = host
		self.username = username
		self.password = password
		self.databaseName = databaseName

# Private
def __getDonorID(donorInfo):
	""" Return the ID# of the donor if the account exists already
	- Matching is done by checking if the last and first name and address
	matches the information from the database. If not, the program will
	output all of the donors that matches the last name. The user will
	then be prompted to select which of the donor he/she chooses to use
	for the transaction.
	"""
	global globalDB
	if globalDB == 0:
		print ("No database connection yet")
		return False

	dbCursor = globalDB.cursor()
	sql = "SELECT `ID #` FROM " + DONORINFO_TABLE + " WHERE `Last Name` = %s AND " + \
			"`First Name` = %s AND `Street Address` = %s;"
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
def __getTransID(donorID,donorInfo):
	global globalDB
	if globalDB == 0:
		print ("No database connection yet")
		return False
	dbCursor = globalDB.cursor()
	sql = "SELECT* FROM " + TRANSACTION_TABLE + " WHERE `Id #` = CONVERT(%s,UNSIGNED INTEGER) AND `Date Payed` = %s AND `Amount Payed` = %s AND `For` = %s;"
	getResult = dbCursor.execute(sql,(donorID, donorInfo.datePaid,donorInfo.amountPaid,'Credit Card'))
	if getResult != 0: # exact match
		#return ID number
		data = dbCursor.fetchone()
		return data[0]
	else:
		return False

def __createDonor(donorInfo):
	""" Returns the ID number of the created Donor """
	global globalDB
	if globalDB == 0:
		print ("No database connection yet...")
		return False

	dbCursor = globalDB.cursor()
	sql = "INSERT INTO " + DONORINFO_TABLE + "(`First Name`, `Last Name`, `Street Address`, " + \
			"`City`, `Province`, `Postal Code`) VALUES (%s, %s, %s, %s, %s, %s);"

	try:
		dbCursor.execute(sql, (donorInfo.firstName, donorInfo.lastName, donorInfo.address, donorInfo.city, donorInfo.province, donorInfo.postalCode))
		return __getDonorID(donorInfo)
	except:
		return False

def __addTransactionDetails(donorID, donorInfo):
	""" Add the transaction details to the Money_Brought_In table """
	global globalDB
	if globalDB == 0:
		print ("No database connection yet...")
		return False

	dbCursor = globalDB.cursor()
	# % signs in the STR_TO_DATE function must be escaped using %%, and quotes mu be escaped using \'
	sql = "INSERT INTO " + TRANSACTION_TABLE + "(`ID #`, `Amount Payed`, `Date Payed`, `For`, `Cash`) " + \
			"VALUES (%s, %s, STR_TO_DATE(%s,'%%Y-%%m-%%d %%r'), 'Credit Card', 0);"

	# Following lines used for debugging
	#print("Query is: %s",sql)
	#print("Date is "+donorInfo.datePaid)

	try:
		dbCursor.execute(sql, (donorID, donorInfo.amountPaid, donorInfo.datePaid))
		#print ("Date is "+ donorInfo.datePaid)
		return True
	except MySQLdb.Error, e:
		print ("Error %d: %s", e.args[0], e.args[1])
		return False

def __connectToDB(dbInfo):
	""" Return the database cursor object """
	global globalDB
	try:
		db = MySQLdb.connect(dbInfo.host, dbInfo.username, dbInfo.password, dbInfo.databaseName)
		dbCursor = db.cursor()
		globalDB = db
		return dbCursor
	except:
		print ("Error connecting to database with the following parameters:")
		print ("Host: %s" % dbInfo.host)
		print ("Username: %s" % dbInfo.username)
		print ("Database name: %s" % dbInfo.databaseName)
		return False
	return False

def __closeDBConnection():
	""" Close the database connection using the global variable """
	global globalDB
	if globalDB == 0:
		print ("No database connection yet...")
		return False
	try:
		cursor = globalDB.cursor()
		globalDB.close()
		globalDb = 0
	except:
		print ("ERROR in closing the database...")

# MAIN APIs
def addTransactionToDatabase(donorDetails,dbInfo):
	__connectToDB(dbInfo)

	global globalDB
	if globalDB == 0:
		print ("No database connection yet...")
		return False

	donorID = __getDonorID(donorDetails)

	if donorID == False:
		donorID = __createDonor(donorDetails)


	if __getTransID(donorID, donorDetails) == False:
		if __addTransactionDetails(donorID, donorDetails) == True:
			print ("Successful in adding transaction...")
			__closeDBConnection()
			return True
		else:
			print ("Error in adding transaction for %s %s" % (donorDetails.firstName, donorDetails.lastName))

	__closeDBConnection()
	return False
