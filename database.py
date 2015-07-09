#!/usr/bin/python

import MySQLdb

# Global variable to store the database object
globalDB = 0

def connectToDB(host, username, password, databaseName):
	""" Return the database cursor object """
	global globalDB
	try:
		db = MySQLdb.connect(host, username, password, databaseName)
		dbCursor = db.cursor()
		globalDB = db
		return dbCursor
	except:
		print "Error connecting to database with the following parameters:"
		print "Host: %s" % host
		print "Username: %s" % username
		print "Database name: %s" % databaseName
		return False
	return False

def getDonorID(dbCursor, firstName, lastName, address):
	""" Return the ID# of the donor if the account exists already """
	sql = "SELECT `ID #` FROM Individuals WHERE `Last Name` = '%s' AND \
			`First Name` = '%s' AND `Street Address` = '%s';" % (lastName, firstName, address)
	getResult = dbCursor.execute(sql)

	if getResult == 1: # exact match
		#return ID number
		data = dbCursor.fetchone()
		return data[0]
	
	else: # multiple match or no match
		sql = "SELECT `ID #`, `Last Name`, `First Name`, `Street Address` \
				FROM Individuals WHERE `Last Name` = '%s'" % (lastName)
		getResult = dbCursor.execute(sql)

		# with multiple matches, display results so user can select the right account
		if getResult > 0:
			data = dbCursor.fetchall()
			counter = 1
			print "#. Last Name, First Name, Address"
			for row in data:
				print "%d. %s, %s, %s"%(counter, row[1], row[2], row[3])
				counter += 1
			print "Details from CSV file: \n %s, %s, %s" % (lastName, firstName, address)
			#raw_choice = raw_input("Input your choice (0 if none of the above): ")
			# stub - start (sublime text does not accept input)
			print "Input your choice (0 if none of the above): 2"
			raw_choice = 0
			# stub - end
			if raw_choice > 0:
				return data[raw_choice - 1][0]
			else:
				# no match from the database results
				return False
			
		# no match at all for last name
		else:
			return False

def createDonor(dbCursor, firstName, lastName, address, city, province, postalCode):
	""" Returns the ID number of the created Donor """
	sql = "INSERT INTO Individuals(`First Name`, `Last Name`, `Street Address`, \
			`City`, `Province`, `Postal Code`) VALUES ('%s','%s','%s','%s','%s','%s');" \
			% (firstName, lastName, address, city, province, postalCode)
	dbCursor.execute(sql)
	return getDonorID(dbCursor, firstName, lastName, address)

def addTransactionDetails(dbCursor, donorID, amount, date):
	""" Add the transaction details to the Money_Brought_In table """
	sql = "INSERT INTO Money_Brought_In(`ID #`, `Amount Payed`, `Date Payed`, `For`, `Cash`) \
			VALUES ('%s', %d, '%s', '%s', %d);" % (donorID, amount, date, "Donation", 0)
	try:
		dbCursor.execute(sql)
		return True
	except:
		return False

def closeDBConnection():
	""" Close the database connection using the global variable """
	global globalDB
	if globalDB == 0:
		print "No database connection yet..."
		return False
	try:
		cursor = globalDB.cursor()
		cursor.execute("Select * from Individuals")
		data = cursor.fetchall()
		print data
		globalDB.close()
	except:
		print "ERROR in closing the database..."
