"""
Unit tests for Personal Finance Tracker
Run with: python -m pytest tests/
"""

import unittest
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.categorizer import TransactionCategorizer


class TestTransactionCategorizer(unittest.TestCase):
    # Test cases for auto-categorization
    
    def setUp(self):
        # Set up test fixtures
        self.categorizer = TransactionCategorizer()
    
    def test_food_categorization(self):
        # Test food-related transactions
        self.assertEqual(
            self.categorizer.categorize("Starbucks Coffee"),
            "Food & Dining"
        )
        self.assertEqual(
            self.categorizer.categorize("McDonald's"),
            "Food & Dining"
        )
        self.assertEqual(
            self.categorizer.categorize("Grocery store purchase"),
            "Food & Dining"
        )
    
    def test_transportation_categorization(self):
        # Test transportation-related transactions
        self.assertEqual(
            self.categorizer.categorize("Uber ride to airport"),
            "Transportation"
        )
        self.assertEqual(
            self.categorizer.categorize("Gas station fill-up"),
            "Transportation"
        )
        self.assertEqual(
            self.categorizer.categorize("Parking meter"),
            "Transportation"
        )
    
    def test_shopping_categorization(self):
        # Test shopping-related transactions
        self.assertEqual(
            self.categorizer.categorize("Amazon.com purchase"),
            "Shopping"
        )
        self.assertEqual(
            self.categorizer.categorize("Walmart"),
            "Shopping"
        )
    
    def test_bills_categorization(self):
        # Test bill-related transactions
        self.assertEqual(
            self.categorizer.categorize("Electric bill payment"),
            "Bills & Utilities"
        )
        self.assertEqual(
            self.categorizer.categorize("Internet service"),
            "Bills & Utilities"
        )
    
    def test_entertainment_categorization(self):
        # Test entertainment-related transactions
        self.assertEqual(
            self.categorizer.categorize("Movie theater tickets"),
            "Entertainment"
        )
        self.assertEqual(
            self.categorizer.categorize("Gym membership"),
            "Entertainment"
        )
    
    def test_healthcare_categorization(self):
        # Test healthcare-related transactions
        self.assertEqual(
            self.categorizer.categorize("Pharmacy prescription"),
            "Healthcare"
        )
        self.assertEqual(
            self.categorizer.categorize("Doctor visit"),
            "Healthcare"
        )
    
    def test_income_categorization(self):
        # Test income-related transactions
        result = self.categorizer.get_suggested_category("Salary payment", 3000)
        self.assertEqual(result, "Salary")
        
        result = self.categorizer.get_suggested_category("Freelance project", 500)
        self.assertEqual(result, "Freelance")
    
    def test_default_categorization(self):
        # Test default category for unknown transactions
        result = self.categorizer.categorize("Unknown transaction XYZ123")
        self.assertEqual(result, "Other Expenses")
    
    def test_case_insensitivity(self):
        # Test that categorization is case-insensitive
        self.assertEqual(
            self.categorizer.categorize("STARBUCKS COFFEE"),
            "Food & Dining"
        )
        self.assertEqual(
            self.categorizer.categorize("uber ride"),
            "Transportation"
        )
    
    def test_add_keyword(self):
        # Test adding custom keywords
        self.categorizer.add_keyword("Shopping", "mystore")
        result = self.categorizer.categorize("Purchase at MyStore")
        self.assertEqual(result, "Shopping")


if __name__ == '__main__':
    unittest.main()