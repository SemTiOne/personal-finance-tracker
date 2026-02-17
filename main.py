"""
Personal Finance Tracker - Main Application
Command-line interface for managing personal finances
"""

import sys
import os
from datetime import datetime, timedelta

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.database import FinanceDatabase
from src.categorizer import TransactionCategorizer
from src.analyzer import FinanceAnalyzer
from src.csv_import import CSVImporter


class FinanceTrackerApp:
    # Main application class
    
    def __init__(self):
        # Initialize the application
        self.db = FinanceDatabase('data/finance.db')
        self.categorizer = TransactionCategorizer()
        self.analyzer = FinanceAnalyzer(self.db)
        self.csv_importer = CSVImporter(self.db)
        self.running = True
    
    def display_menu(self):
        # Display main menu
        print("\n" + "="*60)
        print("         PERSONAL FINANCE TRACKER")
        print("="*60)
        print("\n1.  Add Transaction")
        print("2.  View Transactions")
        print("3.  Delete Transaction")
        print("4.  View Monthly Summary")
        print("5.  Check Budget Alerts")
        print("6.  Generate Reports")
        print("7.  Import from CSV")
        print("8.  Manage Categories")
        print("9.  Export Data")
        print("10. Create Sample Data")
        print("0.  Exit")
        print("\n" + "-"*60)
    
    def add_transaction(self):
        # Add a new transaction manually
        print("\n--- Add Transaction ---")
        
        # Get date
        date_input = input("Date (YYYY-MM-DD) or press Enter for today: ").strip()
        if not date_input:
            date = datetime.now().strftime('%Y-%m-%d')
        else:
            date = date_input
        
        # Get description
        description = input("Description: ").strip()
        
        # Get amount
        while True:
            try:
                amount_input = input("Amount (positive for income, negative for expense): ")
                amount = float(amount_input)
                break
            except ValueError:
                print("Invalid amount. Please enter a number.")
        
        # Determine type
        if amount > 0:
            trans_type = 'income'
            categories = self.db.get_categories('income')
        else:
            trans_type = 'expense'
            amount = abs(amount)
            categories = self.db.get_categories('expense')
        
        # Suggest category
        suggested = self.categorizer.get_suggested_category(description, amount)
        
        # Display categories
        print(f"\nSuggested category: {suggested}")
        print("\nAvailable categories:")
        for i, (cat_name, _) in enumerate(categories, 1):
            print(f"  {i}. {cat_name}")
        
        # Get category choice
        cat_input = input("\nSelect category number or press Enter for suggested: ").strip()
        if cat_input:
            try:
                cat_idx = int(cat_input) - 1
                category = categories[cat_idx][0]
            except (ValueError, IndexError):
                category = suggested
        else:
            category = suggested
        
        # Add to database
        trans_id = self.db.add_transaction(date, description, amount, category, trans_type)
        print(f"\n✓ Transaction added successfully! (ID: {trans_id})")
    
    def view_transactions(self):
        # View recent transactions
        print("\n--- View Transactions ---")
        
        period = input("Period (1=Last 7 days, 2=Last 30 days, 3=This month, 4=Custom): ")
        
        today = datetime.now()
        
        if period == '1':
            start_date = (today - timedelta(days=7)).strftime('%Y-%m-%d')
            end_date = today.strftime('%Y-%m-%d')
        elif period == '2':
            start_date = (today - timedelta(days=30)).strftime('%Y-%m-%d')
            end_date = today.strftime('%Y-%m-%d')
        elif period == '3':
            start_date = today.strftime('%Y-%m-01')
            end_date = today.strftime('%Y-%m-%d')
        elif period == '4':
            start_date = input("Start date (YYYY-MM-DD): ")
            end_date = input("End date (YYYY-MM-DD): ")
        else:
            return
        
        transactions = self.db.get_transactions(start_date, end_date)
        
        if not transactions:
            print("\nNo transactions found for this period.")
            return
        
        print(f"\nTransactions from {start_date} to {end_date}:")
        print("-"*100)
        print(f"{'ID':<5} {'Date':<12} {'Description':<30} {'Amount':<12} {'Category':<20} {'Type':<10}")
        print("-"*100)
        
        total_income = 0
        total_expense = 0
        
        for trans in transactions:
            trans_id, date, desc, amount, category, trans_type, _ = trans
            
            if trans_type == 'income':
                total_income += amount
                amount_str = f"+${amount:.2f}"
            else:
                total_expense += amount
                amount_str = f"-${amount:.2f}"
            
            print(f"{trans_id:<5} {date:<12} {desc[:28]:<30} {amount_str:<12} {category:<20} {trans_type:<10}")
        
        print("-"*100)
        print(f"Total Income:  ${total_income:.2f}")
        print(f"Total Expense: ${total_expense:.2f}")
        print(f"Balance:       ${total_income - total_expense:.2f}")
    
    def delete_transaction(self):
        # Delete a transaction by ID
        print("\n--- Delete Transaction ---")
        
        # First, show recent transactions
        today = datetime.now()
        start_date = (today - timedelta(days=30)).strftime('%Y-%m-%d')
        end_date = today.strftime('%Y-%m-%d')
        
        transactions = self.db.get_transactions(start_date, end_date)
        
        if not transactions:
            print("\nNo recent transactions found.")
            return
        
        print(f"\nRecent Transactions (last 30 days):")
        print("-"*100)
        print(f"{'ID':<5} {'Date':<12} {'Description':<30} {'Amount':<12} {'Category':<20} {'Type':<10}")
        print("-"*100)
        
        for trans in transactions[:20]:  
            trans_id, date, desc, amount, category, trans_type, _ = trans
            
            if trans_type == 'income':
                amount_str = f"+${amount:.2f}"
            else:
                amount_str = f"-${amount:.2f}"
            
            print(f"{trans_id:<5} {date:<12} {desc[:28]:<30} {amount_str:<12} {category:<20} {trans_type:<10}")
        
        print("-"*100)
        
        # Get transaction ID to delete
        try:
            trans_id = input("\nEnter transaction ID to delete (or 'cancel' to go back): ").strip()
            
            if trans_id.lower() == 'cancel':
                return
            
            trans_id = int(trans_id)
            
            # Confirm deletion
            confirm = input(f"Are you sure you want to delete transaction #{trans_id}? (yes/no): ").strip().lower()
            
            if confirm in ['yes', 'y']:
                self.db.delete_transaction(trans_id)
                print(f"\n✓ Transaction #{trans_id} deleted successfully!")
            else:
                print("\nDeletion cancelled.")
        
        except ValueError:
            print("\nInvalid transaction ID. Please enter a number.")
        except Exception as e:
            print(f"\nError deleting transaction: {e}")
    
    def view_monthly_summary(self):
        # View summary for a specific month
        print("\n--- Monthly Summary ---")
        
        month_input = input("Month (YYYY-MM) or press Enter for current month: ").strip()
        
        if month_input:
            try:
                year, month = map(int, month_input.split('-'))
            except:
                print("Invalid format. Use YYYY-MM")
                return
        else:
            today = datetime.now()
            year, month = today.year, today.month
        
        summary = self.db.get_monthly_summary(year, month)
        
        print(f"\nSummary for {year}-{month:02d}:")
        print("-"*50)
        print(f"Total Income:    ${summary['income']:,.2f}")
        print(f"Total Expenses:  ${summary['expenses']:,.2f}")
        print(f"Balance:         ${summary['balance']:,.2f}")
        
        # Show spending by category
        start_date = f"{year}-{month:02d}-01"
        if month == 12:
            end_date = f"{year+1}-01-01"
        else:
            end_date = f"{year}-{month+1:02d}-01"
        
        category_data = self.db.get_category_spending(start_date, end_date)
        
        if category_data:
            print("\nSpending by Category:")
            print("-"*50)
            for category, amount in category_data:
                percentage = (amount / summary['expenses'] * 100) if summary['expenses'] > 0 else 0
                print(f"{category:<30} ${amount:>8,.2f} ({percentage:>5.1f}%)")
    
    def check_budget_alerts(self):
        # Check for budget warnings
        print("\n--- Budget Alerts ---")
        
        today = datetime.now()
        alerts = self.db.check_budget_alerts(today.year, today.month)
        
        if not alerts:
            print("\n✓ All spending is within budget limits!")
            return
        
        print(f"\nBudget Alerts for {today.year}-{today.month:02d}:")
        print("-"*70)
        
        for alert in alerts:
            status = "[!] EXCEEDED" if alert['percentage'] >= 100 else "[!] WARNING"
            print(f"\n{status} - {alert['category']}")
            print(f"  Spent:      ${alert['spent']:.2f}")
            print(f"  Budget:     ${alert['limit']:.2f}")
            print(f"  Percentage: {alert['percentage']:.1f}%")
    
    def generate_reports(self):
        # Generate visualization reports
        print("\n--- Generate Reports ---")
        print("1. Spending Pie Chart")
        print("2. Monthly Trend Chart")
        print("3. Budget Comparison Chart")
        print("4. Text Summary Report")
        
        choice = input("\nSelect report type: ")
        
        today = datetime.now()
        
        if choice == '1':
            period = input("Period (1=This month, 2=Last 30 days, 3=Custom): ")
            
            if period == '1':
                start_date = today.strftime('%Y-%m-01')
                end_date = today.strftime('%Y-%m-%d')
            elif period == '2':
                start_date = (today - timedelta(days=30)).strftime('%Y-%m-%d')
                end_date = today.strftime('%Y-%m-%d')
            else:
                start_date = input("Start date (YYYY-MM-DD): ")
                end_date = input("End date (YYYY-MM-DD): ")
            
            path = self.analyzer.plot_category_spending(start_date, end_date)
            if path:
                print(f"\n✓ Report saved: {path}")
        
        elif choice == '2':
            months = int(input("Number of months to display (default 6): ") or "6")
            path = self.analyzer.plot_monthly_trend(months)
            print(f"\n✓ Report saved: {path}")
        
        elif choice == '3':
            month_input = input("Month (YYYY-MM) or press Enter for current: ").strip()
            if month_input:
                year, month = map(int, month_input.split('-'))
            else:
                year, month = today.year, today.month
            
            path = self.analyzer.plot_budget_comparison(year, month)
            print(f"\n✓ Report saved: {path}")
        
        elif choice == '4':
            month_input = input("Month (YYYY-MM) or press Enter for current: ").strip()
            if month_input:
                year, month = map(int, month_input.split('-'))
            else:
                year, month = today.year, today.month
            
            report = self.analyzer.generate_text_report(year, month)
            print(report)
            
            save = input("Save to file? (y/n): ")
            if save.lower() == 'y':
                filename = f'reports/summary_{year}_{month:02d}.txt'
                os.makedirs('reports', exist_ok=True)
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(report)
                print(f"✓ Report saved: {filename}")
    
    def import_csv(self):
        # Import transactions from CSV
        print("\n--- Import from CSV ---")
        
        filepath = input("CSV file path: ").strip()
        
        if not os.path.exists(filepath):
            print("File not found!")
            return
        
        print("\nColumn names (press Enter for default):")
        date_col = input("Date column (default: Date): ") or "Date"
        desc_col = input("Description column (default: Description): ") or "Description"
        amount_col = input("Amount column (default: Amount): ") or "Amount"
        
        count = self.csv_importer.import_transactions(
            filepath, date_col, desc_col, amount_col
        )
        
        print(f"\n✓ Imported {count} transactions successfully!")
    
    def manage_categories(self):
        # Manage budget categories
        print("\n--- Manage Categories ---")
        
        categories = self.db.get_categories()
        
        print("\nCurrent Categories:")
        print("-"*60)
        print(f"{'Name':<30} {'Budget Limit':<15} {'Type':<10}")
        print("-"*60)
        
        for name, budget, cat_type in categories:
            budget_str = f"${budget:.2f}" if budget > 0 else "No limit"
            print(f"{name:<30} {budget_str:<15} {cat_type:<10}")
        
        print("\nActions:")
        print("1. Update budget limit")
        print("2. Back to main menu")
        
        choice = input("\nSelect action: ")
        
        if choice == '1':
            category = input("Category name: ")
            new_limit = float(input("New budget limit: "))
            self.db.update_budget_limit(category, new_limit)
            print(f"✓ Budget limit updated for {category}")
    
    def export_data(self):
        # Export transactions to CSV
        print("\n--- Export Data ---")
        
        today = datetime.now()
        start_date = input("Start date (YYYY-MM-DD): ")
        end_date = input("End date (YYYY-MM-DD) or press Enter for today: ").strip()
        
        if not end_date:
            end_date = today.strftime('%Y-%m-%d')
        
        filepath = self.analyzer.export_to_csv(start_date, end_date)
        
        if filepath:
            print(f"\n✓ Data exported: {filepath}")
    
    def create_sample_data(self):
        # Create sample transactions for demo
        print("\n--- Create Sample Data ---")
        
        # Create sample CSV
        csv_path = self.csv_importer.create_sample_csv()
        print(f"Sample CSV created: {csv_path}")
        
        # Import it
        count = self.csv_importer.import_transactions(csv_path)
        print(f"✓ Imported {count} sample transactions!")
    
    def run(self):
        # Main application loop
        print("\nWelcome to Personal Finance Tracker!")
        
        while self.running:
            self.display_menu()
            
            choice = input("Select an option: ").strip()
            
            try:
                if choice == '1':
                    self.add_transaction()
                elif choice == '2':
                    self.view_transactions()
                elif choice == '3':
                    self.delete_transaction()
                elif choice == '4':
                    self.view_monthly_summary()
                elif choice == '5':
                    self.check_budget_alerts()
                elif choice == '6':
                    self.generate_reports()
                elif choice == '7':
                    self.import_csv()
                elif choice == '8':
                    self.manage_categories()
                elif choice == '9':
                    self.export_data()
                elif choice == '10':
                    self.create_sample_data()
                elif choice == '0':
                    self.running = False
                    print("\nGoodbye! Stay financially healthy! 💰")
                else:
                    print("\nInvalid option. Please try again.")
            
            except KeyboardInterrupt:
                print("\n\nInterrupted by user.")
                self.running = False
            except Exception as e:
                print(f"\nError: {e}")
                import traceback
                traceback.print_exc()
        
        # Clean up
        self.db.close()


if __name__ == '__main__':
    app = FinanceTrackerApp()
    app.run()