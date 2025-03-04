import csv
import sys

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
    sample_data_individual = ['Johnson', 'Doe', '', '1234 Johnson St', '2345 Johnson Ave', 'Burnaby', 'BC', 'V1A 2A2',
        'Canada', '555-555-5555', 'johntestdoe@gmail.com', '123456789', '1000.00', '2024-03-04', 'charity', "good luck"]
    sample_data_company = ['Albert', 'Smith', 'BestCompanyBC', '1 Smith St', '2 Smith Ave', 'Vancouver', 'BC', 'V2B 3B3',
        'USA', '604-123-4567', 'bestcompanyBC@gmail.com', '123456789', '500.00', '2024-03-05', 'company place', "cheers!"]
    
    # Creating a sample file with hardcoded data
    with open(filename, 'w', newline='', encoding='utf-16-le') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(input_field_names)
        writer.writerow(sample_data_individual)
        writer.writerow(sample_data_company)

def main(argv):	    
    # If there is no arguments provided then a sample csv will be called "sample_canada_helps_csv.csv"
    if len(argv) == 1:
         create_sample_csv(argv[0])
    elif len(argv) == 0:
         create_sample_csv("sample_canada_helps_csv.csv")

if __name__ == "__main__":
    main(sys.argv[1:])
    