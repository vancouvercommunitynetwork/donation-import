import unittest

from donations_pp import (
    getField,
    convert_date,
    fill_individual_contract,
    fill_donation,
    fill_membership
)

class TestDonationsPP(unittest.TestCase):
    # Test getField function
    def test_getField_present(self):
        row = {"FieldName": "Value"}
        self.assertEqual(getField(row, "FieldName"), "Value")

    def test_getField_missing(self):
        row = {}
        self.assertEqual(getField(row, "FieldName", "DefaultValue"), "DefaultValue")

    def test_getField_no_default(self):
        row = {}
        self.assertEqual(getField(row, "FieldName"), "")

    # Test convert_date function
    def test_convert_date_valid_format(self):
        self.assertEqual(convert_date("2024/01/01"), "2024-01-01")
        self.assertEqual(convert_date("2024-01-01"), "2024-01-01")

    def test_convert_date_invalid_format(self):
        with self.assertRaises(ValueError):  # Raises error for invalid format
            convert_date("01-01-2024")

    def test_convert_date_empty_string(self):
        with self.assertRaises(ValueError):
            convert_date("")

    # Test fill_individual_contract function
    def test_fill_individual_contract(self):
        row = {
            "Donor First Name": "John",
            "Donor Last Name": "Doe",
            "Donor Email": "john.doe@example.com"
        }
        expected = ["john.doe@example.com", "John", "Doe", "john.doe@example.com"]
        self.assertEqual(fill_individual_contract(row), expected)

    def test_fill_individual_contract_missing_fields(self):
        row = {
            "Donor Email": "jane.doe@example.com"
        }
        expected = ["jane.doe@example.com", "", "", "jane.doe@example.com"]
        self.assertEqual(fill_individual_contract(row), expected)

    # Test fill_donation function
    def test_fill_donation(self):
        row = {
            "Donor Email": "john.doe@example.com",
            "Transaction ID": "TXN123",
            "Gross Amount": "50",
            "Donation Date": "2024/01/01"
        }
        expected = ["john.doe@example.com", "TXN123", "50.00", "2024-01-01", "Donation", "PayPal"]
        self.assertEqual(fill_donation(row), expected)

    def test_fill_donation_zero_amount(self):
        """Test case for a $0 donation"""
        row = {
            "Donor Email": "john.doe@example.com",
            "Transaction ID": "TXN456",
            "Gross Amount": "0",
            "Donation Date": "2024/01/01"
        }
        expected = ["john.doe@example.com", "TXN456", "0.00", "2024-01-01", "Donation", "PayPal"]
        self.assertEqual(fill_donation(row), expected)

    # Test fill_membership function
    def test_fill_membership(self):
        row = {
            "Donor Email": "john.doe@example.com",
            "Donation Date": "2024/01/01"
        }
        expected = ["john.doe@example.com", "VCN Member", "2024-01-01"]
        self.assertEqual(fill_membership(row), expected)

if __name__ == "__main__":
    unittest.main()
