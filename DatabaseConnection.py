from __future__ import print_function

import MySQLdb

class DatabaseConnection:
    """ Object managing the database connection """
    def __init__(self, host, username, password, databaseName):
        """Creates a connection to the database with the given parameters"""
        self.host = host
        self.username = username
        self.password = password
        self.databaseName = databaseName
        self.dbConnection = 0
        self.dbConnection = self.getConnection()

    def getConnection(self):
        """ Returns the connection to the database
        Connection will equal 0 if it cannot be created"""
        if self.dbConnection == 0:
            try:
                self.dbConnection = MySQLdb.connect(self.host, self.username, self.password, self.databaseName)
                return self.dbConnection
            except:
                print ("Error connecting to database with the following parameters:")
                print ("Host: %s" % self.host)
                print ("Username: %s" % self.username)
                print ("Database name: %s" % self.databaseName)
                return 0
        else:
            return self.dbConnection

    def closeConnection(self):
        """ Closes connection to database if it is open """
        if self.dbConnection == 0:
            print ("No database connection yet...")
            return False
        try:
            cursor = self.dbConnection.cursor()
            self.dbConnection.close()
            self.dbConnection = 0
        except:
            print ("ERROR in closing the database...")
