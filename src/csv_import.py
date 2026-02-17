"""
CSV Import module
Handles importing transactions from CSV files
"""

import csv
from datetime import datetime
from typing import List, Dict
from .categorizer import TransactionCategorizer


class CSVImporter:
    # Import transactions from CSV files
    
    def __init__(self, database):
        # Initialize with database connection
        self.db = database
        self.categorizer = TransactionCategorizer()
    
    def parse_csv(self, filepath: str, 
                  date_col: str = 'Date',
                  desc_col: str = 'Description', 
                  amount_col: str = 'Amount',
                  skip_header: bool = True) -> List[Dict]:
        """
        Parse CSV file and extract transactions
        
        Args:
            filepath: Path to CSV file
            date_col: Name of date column
            desc_col: Name of description column
            amount_col: Name of amount column
            skip_header: Whether first row is header
            
        Returns:
            List of transaction dictionaries
        """
        transactions = []
        
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f) if skip_header else csv.reader(f)
            
            for row in reader:
                if skip_header:
                    date_str = row.get(date_col, '')
                    description = row.get(desc_col, '')
                    amount_str = row.get(amount_col, '0')
                else:
                    # Assume order: Date, Description, Amount
                    date_str = row[0]
                    description = row[1]
                    amount_str = row[2]
                
                # Parse date
                try:
                    date = self._parse_date(date_str)
                except:
                    print(f"Skipping row with invalid date: {date_str}")
                    continue
                
                # Parse amount
                try:
                    amount = self._parse_amount(amount_str)
                except:
                    print(f"Skipping row with invalid amount: {amount_str}")
                    continue
                
                # Determine type and category
                trans_type = 'income' if amount > 0 else 'expense'
                amount = abs(amount)
                category = self.categorizer.get_suggested_category(
                    description, 
                    amount if trans_type == 'income' else -amount
                )
                
                transactions.append({
                    'date': date,
                    'description': description,
                    'amount': amount,
                    'category': category,
                    'type': trans_type
                })
        
        return transactions
    
    def import_transactions(self, filepath: str, 
                          date_col: str = 'Date',
                          desc_col: str = 'Description',
                          amount_col: str = 'Amount',
                          skip_header: bool = True) -> int:
        """
        Import transactions from CSV into database
        
        Args:
            filepath: Path to CSV file
            date_col: Name of date column
            desc_col: Name of description column
            amount_col: Name of amount column
            skip_header: Whether first row is header
            
        Returns:
            Number of transactions imported
        """
        transactions = self.parse_csv(filepath, date_col, desc_col, 
                                     amount_col, skip_header)
        
        count = 0
        for trans in transactions:
            try:
                self.db.add_transaction(
                    trans['date'],
                    trans['description'],
                    trans['amount'],
                    trans['category'],
                    trans['type']
                )
                count += 1
            except Exception as e:
                print(f"Error importing transaction: {e}")
        
        return count
    
    def _parse_date(self, date_str: str) -> str:
        """
        Parse date string into YYYY-MM-DD format
        Handles multiple common date formats
        """
        date_formats = [
            '%Y-%m-%d',
            '%m/%d/%Y',
            '%d/%m/%Y',
            '%Y/%m/%d',
            '%m-%d-%Y',
            '%d-%m-%Y',
            '%b %d, %Y',
            '%B %d, %Y'
        ]
        
        date_str = date_str.strip()
        
        for fmt in date_formats:
            try:
                dt = datetime.strptime(date_str, fmt)
                return dt.strftime('%Y-%m-%d')
            except ValueError:
                continue
        
        raise ValueError(f"Unable to parse date: {date_str}")
    
    def _parse_amount(self, amount_str: str) -> float:
        """
        Parse amount string into float
        Handles currency symbols, commas, parentheses for negatives
        """
        # Remove common currency symbols and whitespace
        amount_str = amount_str.strip()
        amount_str = amount_str.replace('$', '').replace('€', '')
        amount_str = amount_str.replace('£', '').replace(',', '')
        
        # Handle parentheses as negative
        if '(' in amount_str and ')' in amount_str:
            amount_str = amount_str.replace('(', '-').replace(')', '')
        
        return float(amount_str)
    
    def create_sample_csv(self, filepath: str = 'data/sample_transactions.csv'):
        # Create a sample CSV file for testing
        sample_data = [
            ['Date', 'Description', 'Amount'],
            ['2026-02-01', 'Salary - ABC Corp', '3500.00'],
            ['2026-02-02', 'Grocery Store', '-125.50'],
            ['2026-02-03', 'Gas Station', '-45.00'],
            ['2026-02-04', 'Restaurant - Dinner', '-65.30'],
            ['2026-02-05', 'Amazon Purchase', '-89.99'],
            ['2026-02-06', 'Electricity Bill', '-120.00'],
            ['2026-02-07', 'Gym Membership', '-50.00'],
            ['2026-02-08', 'Freelance Project', '500.00'],
            ['2026-02-10', 'Movie Tickets', '-32.00'],
            ['2026-02-12', 'Pharmacy', '-25.75'],
            ['2026-02-14', 'Valentine Dinner', '-95.00'],
            ['2026-02-15', 'Uber Ride', '-18.50']
        ]
        
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerows(sample_data)
        
        return filepath