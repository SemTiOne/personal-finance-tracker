"""
Analytics and visualization module
Generates reports and charts from transaction data
"""

import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Tuple, Optional
import os


class FinanceAnalyzer:
    # Analyzes and visualizes financial data
    
    def __init__(self, database):
        # Initialize with database connection
        self.db = database
    
    def generate_spending_report(self, start_date: str, end_date: str) -> pd.DataFrame:
        """
        Generate detailed spending report for date range
        
        Args:
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            
        Returns:
            DataFrame with spending analysis
        """
        transactions = self.db.get_transactions(start_date, end_date)
        
        if not transactions:
            return pd.DataFrame()
        
        df = pd.DataFrame(transactions, columns=[
            'id', 'date', 'description', 'amount', 'category', 'type', 'created_at'
        ])
        
        return df
    
    def plot_category_spending(self, start_date: str, end_date: str, 
                              save_path: str = None) -> str:
        """
        Create pie chart of spending by category
        
        Args:
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            save_path: Path to save the chart
            
        Returns:
            Path to saved chart
        """
        category_data = self.db.get_category_spending(start_date, end_date)
        
        if not category_data:
            print("No spending data available for this period")
            return None
        
        categories = [row[0] for row in category_data]
        amounts = [row[1] for row in category_data]
        
        plt.figure(figsize=(10, 8))
        colors = plt.cm.Set3(range(len(categories)))
        
        plt.pie(amounts, labels=categories, autopct='%1.1f%%',
                startangle=90, colors=colors)
        plt.title(f'Spending by Category\n{start_date} to {end_date}')
        plt.axis('equal')
        
        if not save_path:
            save_path = f'reports/spending_pie_{start_date}_to_{end_date}.png'
        
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return save_path
    
    def plot_monthly_trend(self, months: int = 6, save_path: str = None) -> str:
        """
        Create line chart showing income vs expenses over time
        
        Args:
            months: Number of months to display
            save_path: Path to save the chart
            
        Returns:
            Path to saved chart
        """
        today = datetime.now()
        monthly_data = []
        
        for i in range(months):
            month_date = today - timedelta(days=30*i)
            summary = self.db.get_monthly_summary(month_date.year, month_date.month)
            monthly_data.append(summary)
        
        monthly_data.reverse()
        
        months_labels = [data['month'] for data in monthly_data]
        income = [data['income'] for data in monthly_data]
        expenses = [data['expenses'] for data in monthly_data]
        balance = [data['balance'] for data in monthly_data]
        
        plt.figure(figsize=(12, 6))
        
        x = range(len(months_labels))
        plt.plot(x, income, marker='o', label='Income', linewidth=2, color='green')
        plt.plot(x, expenses, marker='s', label='Expenses', linewidth=2, color='red')
        plt.plot(x, balance, marker='^', label='Balance', linewidth=2, color='blue')
        
        plt.xlabel('Month')
        plt.ylabel('Amount ($)')
        plt.title(f'Financial Trend - Last {months} Months')
        plt.xticks(x, months_labels, rotation=45)
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        if not save_path:
            save_path = f'reports/trend_{months}months.png'
        
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return save_path
    
    def plot_budget_comparison(self, year: int, month: int, 
                              save_path: str = None) -> str:
        """
        Create bar chart comparing spending vs budget limits
        
        Args:
            year: Year
            month: Month (1-12)
            save_path: Path to save the chart
            
        Returns:
            Path to saved chart
        """
        start_date = f"{year}-{month:02d}-01"
        if month == 12:
            end_date = f"{year+1}-01-01"
        else:
            end_date = f"{year}-{month+1:02d}-01"
        
        category_data = self.db.get_category_spending(start_date, end_date)
        categories_with_budget = self.db.get_categories('expense')
        
        budget_dict = {cat[0]: cat[1] for cat in categories_with_budget if cat[1] > 0}
        spending_dict = {cat[0]: cat[1] for cat in category_data}
        
        categories = list(budget_dict.keys())
        budgets = [budget_dict[cat] for cat in categories]
        spending = [spending_dict.get(cat, 0) for cat in categories]
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        x = range(len(categories))
        width = 0.35
        
        bars1 = ax.bar([i - width/2 for i in x], budgets, width, 
                       label='Budget', color='lightblue')
        bars2 = ax.bar([i + width/2 for i in x], spending, width, 
                       label='Actual Spending', color='coral')
        
        ax.set_xlabel('Category')
        ax.set_ylabel('Amount ($)')
        ax.set_title(f'Budget vs Actual Spending - {year}-{month:02d}')
        ax.set_xticks(x)
        ax.set_xticklabels(categories, rotation=45, ha='right')
        ax.legend()
        ax.grid(True, alpha=0.3, axis='y')
        
        # Add value labels on bars
        for bar in bars1 + bars2:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'${height:.0f}',
                   ha='center', va='bottom', fontsize=8)
        
        plt.tight_layout()
        
        if not save_path:
            save_path = f'reports/budget_comparison_{year}_{month:02d}.png'
        
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return save_path
    
    def generate_text_report(self, year: int, month: int) -> str:
        """
        Generate text summary report
        
        Args:
            year: Year
            month: Month (1-12)
            
        Returns:
            Formatted text report
        """
        summary = self.db.get_monthly_summary(year, month)
        alerts = self.db.check_budget_alerts(year, month)
        
        report = f"""
{'='*60}
MONTHLY FINANCIAL REPORT - {year}-{month:02d}
{'='*60}

SUMMARY:
--------
Total Income:    ${summary['income']:,.2f}
Total Expenses:  ${summary['expenses']:,.2f}
Balance:         ${summary['balance']:,.2f}

"""
        
        if alerts:
            report += "BUDGET ALERTS:\n"
            report += "-" * 60 + "\n"
            for alert in alerts:
                status = "[!] EXCEEDED" if alert['percentage'] >= 100 else "[!] WARNING"
                report += f"{status} - {alert['category']}\n"
                report += f"  Spent: ${alert['spent']:.2f} / Budget: ${alert['limit']:.2f} "
                report += f"({alert['percentage']:.1f}%)\n\n"
        else:
            report += "[OK] All spending within budget limits\n\n"
        
        # Top spending categories
        start_date = f"{year}-{month:02d}-01"
        if month == 12:
            end_date = f"{year+1}-01-01"
        else:
            end_date = f"{year}-{month+1:02d}-01"
        
        category_data = self.db.get_category_spending(start_date, end_date)
        
        if category_data:
            report += "TOP SPENDING CATEGORIES:\n"
            report += "-" * 60 + "\n"
            for i, (category, amount) in enumerate(category_data[:5], 1):
                percentage = (amount / summary['expenses'] * 100) if summary['expenses'] > 0 else 0
                report += f"{i}. {category}: ${amount:.2f} ({percentage:.1f}%)\n"
        
        report += "\n" + "="*60 + "\n"
        
        return report
    
    def export_to_csv(self, start_date: str, end_date: str, 
                     filename: str = None) -> str:
        """
        Export transactions to CSV file
        
        Args:
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            filename: Output filename
            
        Returns:
            Path to exported file
        """
        df = self.generate_spending_report(start_date, end_date)
        
        if df.empty:
            print("No data to export")
            return None
        
        if not filename:
            filename = f'reports/transactions_{start_date}_to_{end_date}.csv'
        
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        df.to_csv(filename, index=False)
        
        return filename