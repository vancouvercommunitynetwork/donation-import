import unittest
import csv

from donations import (
    getField,
    convert_date,
    fill_individual_contract,
    fill_organization_contract,
    fill_donation,
    fill_membership,
    normalizeInput,

    #importing constants to avoid duplication
    ANON,
    FIRST_NAME,
    LAST_NAME,
    COMPANY_NAME,
    ADDRESS,
    SUPPLEMENTAL_ADDRESS_1,
    CITY,
    STATE,
    POSTAL_CODE,
    COUNTRY,
    PHONE,
    EMAIL,
    INVOICE_NUMBER,
    TOTAL_AMOUNT,
    DATE_RECEIVED,
    DONATION_SOURCE,
    NOTE
)

class TestDonations(unittest.TestCase):
    # Test the getField function
    def test_getField_present(self):
        row = {"FieldName": "Value" }
        self.assertEqual(getField(row, "FieldName"), "Value")

    def test_getField_anon(self):
        row = {"FieldName": ANON}
        self.assertEqual(getField(row, "FieldName"), "")

    def test_getField_missing(self):
        row = {}
        self.assertEqual(getField(row, "FieldName", "DefaultValue"), "DefaultValue")

    def test_getField_no_default(self):
        row = {}
        self.assertEqual(getField(row, "FieldName"), "")

    # Test the convert_date function
    def test_convert_date_valid_format(self):
        self.assertEqual(convert_date("2025/01/01"), "2025-01-01")
        self.assertEqual(convert_date("2025-01-01"), "2025-01-01")
    
    def test_convert_date_invalid_format(self):
        with self.assertRaises(ValueError):
            convert_date("01-01-2025")
    
    def test_convert_date_empty_string(self):
        with self.assertRaises(ValueError):
            convert_date("")

    # Test the fill_individual_contract
    def test_fill_individual_contract(self):
        row = {
            FIRST_NAME: "John",
            LAST_NAME: "Doe",
            ADDRESS: "123 Johnson St",
            SUPPLEMENTAL_ADDRESS_1: "456 Johnson Ave",
            CITY: "Vancouver",
            STATE: "BC",
            POSTAL_CODE: "V1A 2N2",
            COUNTRY: "Canada",
            PHONE: "604-123-4567",
            EMAIL: "john.doe@example.com"
        }
        expected = ["john.doe@example.com", "John", "Doe", "123 Johnson St","456 Johnson Ave",
                    "Vancouver","BC","V1A 2N2","Canada","604-123-4567","john.doe@example.com"]
        self.assertEqual(fill_individual_contract(row), expected)

    def test_fill_individual_contract_missing_fields(self):
        row = {
            EMAIL: "john.doe@example.com"
        }
        expected = ["john.doe@example.com", "", "", "","","","","","","","john.doe@example.com"]
        self.assertEqual(fill_individual_contract(row), expected)

    # Test the fill organizational contract function
    def test_fill_organizational_contract(self):
        row = {
            COMPANY_NAME: "Vancouver Company",
            ADDRESS: "123 Johnson St",
            SUPPLEMENTAL_ADDRESS_1: "456 Johnson Ave",
            CITY: "Vancouver",
            STATE: "BC",
            POSTAL_CODE: "V1A 2N2",
            COUNTRY: "Canada",
            PHONE: "604-123-4567",
            EMAIL: "john.doe@example.com"
        }
        expected = ["john.doe@example.com", "Vancouver Company", "123 Johnson St","456 Johnson Ave",
                    "Vancouver","BC","V1A 2N2","Canada","604-123-4567","john.doe@example.com"]
        self.assertEqual(fill_organization_contract(row), expected)

    def test_fill_organizational_contract_missing_fields(self):
        row = {
            EMAIL: "john.doe@example.com"
        }
        expected = ["john.doe@example.com", "", "","",
                    "","","","","","john.doe@example.com"]
        self.assertEqual(fill_organization_contract(row), expected)

    #Test the fill_donation function
    def test_fill_donation(self):
        row = {
            EMAIL: "john.doe@example.com",
            INVOICE_NUMBER: "123456789123",
            TOTAL_AMOUNT: "10.5",
            DATE_RECEIVED: "2025-01-01",
            DONATION_SOURCE: "CanadaHelps",
            NOTE: "cheers"
        }
        expected = ["john.doe@example.com", "123456789123", "10.50", "2025-01-01", 
                    "CanadaHelps", "cheers", "Donation", "Credit Card"]
        self.assertEqual(fill_donation(row), expected)

    def test_fill_donation_zero_amount(self):
        row = {
            EMAIL: "john.doe@example.com",
            INVOICE_NUMBER: "123456789123",
            TOTAL_AMOUNT: "0",
            DATE_RECEIVED: "2025-01-01",
            DONATION_SOURCE: "CanadaHelps",
            NOTE: "cheers"
        }
        expected = ["john.doe@example.com", "123456789123", "0.00", "2025-01-01", 
                    "CanadaHelps", "cheers", "Donation", "Credit Card"]
        self.assertEqual(fill_donation(row), expected)

    @unittest.expectedFailure
    def test_fill_donation_missing_amount(self):
        # Case where the donation amount might be missing, this test should fail since 
        # the missing result does not resolve to a zero amount (0.00)
        row = {
            EMAIL: "john.doe@example.com",
            INVOICE_NUMBER: "123456789123",
            TOTAL_AMOUNT: "",
            DATE_RECEIVED: "2025-01-01",
            DONATION_SOURCE: "CanadaHelps",
            NOTE: "cheers"
        }
        expected = ["john.doe@example.com", "123456789123", "0.00", "2025-01-01", 
                    "CanadaHelps", "cheers", "Donation", "Credit Card"]
        self.assertEqual(fill_donation(row), expected)

    def test_fill_donation_missing_amount_raises_error(self):
        row = {
            EMAIL: "john.doe@example.com",
            INVOICE_NUMBER: "123456789123",
            TOTAL_AMOUNT: "",
            DATE_RECEIVED: "2025-01-01",
            DONATION_SOURCE: "CanadaHelps",
            NOTE: "cheers"
        }
        with self.assertRaises(ValueError):
            fill_donation(row)

    # Test the fill membership function
    def test_fill_membership(self):
        row = {
            EMAIL: "john.doe@example.com",
            DATE_RECEIVED: "2025-01-01"
        }
        expected = ["john.doe@example.com", "VCN Member", "2025-01-01"]
        self.assertEqual(fill_membership(row), expected)

    # Test the normalizeInput function
    def test_normalizeInput_standard_encoding(self):
        sample_csv = "Sample CanadaHelps Input CSV.csv" # input file encoding is utf-16-le
        normalized_input = normalizeInput(sample_csv)
        norm_str = ''.join(normalized_input)
        self.assertTrue(norm_str.isascii())      

    def test_normalizeInput_different_input_encodings(self):
        # test using the sample files with 5 different encodings
        sample_dir = "sample_donations_canadahelps"
        ansi_smp = sample_dir + "/sample_canadahelps_input_ansi.csv"
        utf8BOM_smp = sample_dir + "/sample_canadahelps_input_utf_8_BOM.csv"
        utf8_smp = sample_dir + "/sample_canadahelps_input_utf_8.csv"
        utf16be_smp = sample_dir + "/sample_canadahelps_input_utf_16_be.csv"
        utf16le_smp = sample_dir + "/sample_canadahelps_input_utf_16_le.csv"

        sample_files = [ansi_smp, utf8BOM_smp, utf8_smp, utf16be_smp, utf16le_smp]
        for sf in sample_files:
            normalized_input = normalizeInput(sf)
            norm_str = ''.join(normalized_input)
            with self.subTest(sf):
                self.assertTrue(norm_str.isascii())

if __name__ == "__main__":
    unittest.main()