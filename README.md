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
  - Install python dev:
    - sudo apt-get install python-dev
  - MySQL Install
    - Installing
      - sudo apt-get update
      - sudo apt-get install mysql-server
      - sudo mysql_install_db
  - Installing Python MySQL library
      - enter this: sudo apt-get install python-mysql.connector
      - then sudo apt-get python-mysqldb
  - After Installing the important stuff:
    - Add the database in MySQL
    - importing an .sql file:mysql -u root -p Cheese<sql_file_name.sql
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
