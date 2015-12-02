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
