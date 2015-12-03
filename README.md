# donation-import

## Used with python 2.7.6 and MySQL 5.6.28 - standard

### History of Changes Since 1-12-2015 (DD-MM-YYYY format)
- Issues Fixed
  - Duplicated entries related to same csv file
  - Time not able to insert correctly

- Added Features
  - Finding Transaction That existed in database (see getTransID in database.py)
  - Saving Donator's LoginID with accordance with their email (see getLoginID in main.py)
    - if LoginID is vcn mail then will record their id
    - if not vcn mail then LoginID will become the donator's email
    - if ANON will become 000
  - Saving Transaction ID (as Paper Receipt)
## Getting Started
- These install instruction tested with ubuntu 14.04 LTS - Results may vary
  - Install python dev via apt-get install python-dev
  - MySQL Install
    - If you want to purge your current sql version:
      - apt-get remove --purge mysql-server mysql-client mysql-common
      - apt-get autoremove
      - apt-get autoclean
    - Installing
      - apt-get update
      - apt-get install mysql-server-5.6
      - mysql_install_db
  - Installing Python MySQL library
      - Download the zip package via here: http://sourceforge.net/projects/mysql-python/
      - Go to where MySQL-python-1.2.4b4.tar.gz located and type these commands:
        - gunzip MySQL-python-1.2.4b4.tar.gz
        - tar -xvf MySQL-python-1.2.4b4.tar.gz
        - tar -xvf MySQL-python-1.2.4b4.tar
        - cd MySQL-python-1.2.4b4
        - python setup.py build
        - python setup.py install
  - After Installing the important stuff:
    - Add the database in MySQL
    - enter this: mysql -u root -p (mostly will ask for password)
    - in MySQL commands
      - create database Cheese - for creating database with name Cheese
      - use Cheese (will switch to database Cheese)
      - Copy and paste these commands:```
      CREATE TABLE Individuals(
        `Id #` int(11) NOT NULL auto_increment,
        `First Name` varchar(50) default NULL,
        `Last Name` varchar(50) default NULL,
        `Street Address` varchar(50) default NULL,
        `City` varchar(50) default NULL,
        `Province` varchar(50) default NULL,
        `Postal Code` varchar(20) default NULL,
        `Phone (Home)` varchar(30) default NULL,
        `Phone (Work)` varchar(30) default NULL,
        `Phone (Fax)` varchar(30) default NULL,
        `Company` tinyint(1) default NULL,
        `comment` varchar(255) default NULL,
        PRIMARY KEY  (`Id #`),
        KEY `LastName` (`Last Name`)
        ) ENGINE=MyISAM AUTO_INCREMENT=15230 DEFAULT CHARSET=latin1;

        CREATE TABLE Money_Brought_In(
          `Receipt #` int(11) NOT NULL auto_increment,
          `Id #` int(11) default NULL,
          `Amount Payed` double default NULL,
          `Date Payed` datetime default NULL,
          `For` varchar(50) default NULL,
          `Cash` tinyint(1) default NULL,
          `Receipt Given` tinyint(1) default NULL,
          `Main Login Id` varchar(50) NOT NULL default '000',
          `Login Id #2` varchar(50) default NULL,
          `Login Id #3` varchar(50) default NULL,
          `Login Id #4` varchar(50) default NULL,
          `Paper Receipt` varchar(50) default NULL,
          PRIMARY KEY  (`Receipt #`)
          ) ENGINE=MyISAM AUTO_INCREMENT=32392 DEFAULT CHARSET=latin1;
      ```
      - type exit to quit MySql Console
    - in donation_imort.cfg, change these parameters to fix your mysql settings
      - userName=root
      - password=password
      - dbName=Cheese
    - To change the testing csv file
      - csvFileName=csv_name_here.csv (csv_name_here = your csv file name)
    - To launch the program just type: python main.py
      - If there's a line 'Successful in adding transaction...' you have added all non-duplicate entries successfully
      - If there are no outputs that's mean you use a already imported csv file
      - If there are errors: either code error or something wrong with your config
        - If 'No database connection yet...' appears something wrong with your MySQL config in donation_imort.cfg
        - If 'Error in opening/reading CSV file. Check if file exists...' appears. Something wrong with your csv file config in  in donation_imort.cfg
