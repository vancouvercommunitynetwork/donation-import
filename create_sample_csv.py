import csv
import sys
import donations

# These fields are the expected fields from an input CanadaHelps CSV file
# copied from donations.py to maintain consistency

FIRST_NAME="DONOR FIRST NAME" #REQUIRED
LAST_NAME="DONOR LAST NAME" #REQUIRED
COMPANY_NAME="DONOR COMPANY NAME"
ADDRESS="DONOR ADDRESS 1"
ADDRESS_2 ="DONOR ADDRESS 2"
CITY="DONOR CITY"
STATE="DONOR PROVINCE/STATE"
POSTAL_CODE="DONOR POSTAL/ZIP CODE"
COUNTRY="DONOR COUNTRY"
PHONE="DONOR PHONE NUMBER"
EMAIL="DONOR EMAIL ADDRESS" #REQUIRED

INVOICE_NUMBER="TRANSACTION NUMBER"
TOTAL_AMOUNT="AMOUNT" #REQUIRED
DATE_RECEIVED="DONATION DATE"
DONATION_SOURCE="DONATION SOURCE"
NOTE="MESSAGE TO CHARITY"

INPUT_DATE_FORMATS = ['%Y/%m/%d', '%Y-%m-%d']

def create_sample_csv(filename):
    """ Create a csv file with sample data

	Argument:
		filename -- (String) the csv file path
	"""

    input_field_names = [FIRST_NAME, LAST_NAME, COMPANY_NAME, ADDRESS, ADDRESS_2, CITY, STATE, POSTAL_CODE, 
        COUNTRY, PHONE, EMAIL, INVOICE_NUMBER, TOTAL_AMOUNT, DATE_RECEIVED, DONATION_SOURCE, NOTE]

    # Sample hard coded data for both individual and company to test exporting
    
    data = [
        ['Julian','Rogers','','1088 Cambie St','','Vancouver','British Columbia','V6B 6J5','Canada','604-721-9356',
         'rogers@hotmail.com','123456789123','50','2025-01-14','Canadian Red Cross','donating to a worthy cause'],
         ['Richard','Bennett','','555 Columbia Street','502 Columbia Street','New Westminster','British Columbia','V3L 1B2','Canada',
          '604-525-5411','rbennett@gmail.com','308561985234','25.45','2024/12/15','World Vision Canada','cheers!'],
         ['Matthew','Ward','AlbertaCompany','899 Centre Street SW','35 Crowfoot Terrace NW #35','Calgary','Alberta','T2G 1B8','Canada',
          '403-264-8990','mattw_co@gmail.com','639286019723','90.5','2025/02/11','','sending money to help those in need'],
         ['Abigail','Hughes','OntarioCompany','2041 Winston Park Dr','','Oakville','Ontario','L6H 6P5','Canada','289-813-2239',
          'abih_co@gmail.com','184619263841','110','2025-02-20','','donating to help someone out :)']
    ]
    
    # Creating a sample file with hardcoded data
    with open(filename, 'w', newline='', encoding='utf-16-le') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(input_field_names)
        writer.writerows(data)

def main(argv):	    

    # If header field names are not correctly named then any information in that column will be blank on export.

    # If there is no arguments provided then a sample csv will be called "sample_canada_helps_csv.csv"
    if len(argv) == 1:
         create_sample_csv(argv[0])
    elif len(argv) == 0:
         create_sample_csv("Sample CanadaHelps Input CSV.csv")

    donations.export("Sample CanadaHelps Input CSV.csv", "test")
    

if __name__ == "__main__":
    main(sys.argv[1:])
    