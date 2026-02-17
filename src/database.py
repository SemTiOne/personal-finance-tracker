"""
Database module for Personal Finance Tracker
Handles all database operations using SQLite
"""

import sqlite3
from datetime import datetime
from typing import List, Tuple, Optional
import os


class FinanceDatabase:
    # Manages database operations for finance tracking
    
    def __init__(self, db_path: str = "data/finance.db"):
        # Initialize database connection
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self._create_tables()
    
    def _create_tables(self):
        # Create necessary tables if they don't exist
        
        # Transactions table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                description TEXT NOT NULL,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                type TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Categories table with budget limits
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                budget_limit REAL DEFAULT 0,
                type TEXT NOT NULL
            )
        """)
        
        # Budget alerts table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS budget_alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT NOT NULL,
                month TEXT NOT NULL,
                spent REAL NOT NULL,
                limit_amount REAL NOT NULL,
                percentage REAL NOT NULL,
                alert_date TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        self.conn.commit()
        self._initialize_default_categories()
    
    def _initialize_default_categories(self):
        # Add default categories if database is empty
        default_categories = [
            ('Food & Dining', 500, 'expense'),
            ('Transportation', 200, 'expense'),
            ('Shopping', 300, 'expense'),
            ('Bills & Utilities', 400, 'expense'),
            ('Entertainment', 150, 'expense'),
            ('Healthcare', 200, 'expense'),
            ('Other Expenses', 100, 'expense'),
            ('Salary', 0, 'income'),
            ('Freelance', 0, 'income'),
            ('Other Income', 0, 'income')
        ]
        
        for name, budget, cat_type in default_categories:
            try:
                self.cursor.execute(
                    "INSERT OR IGNORE INTO categories (name, budget_limit, type) VALUES (?, ?, ?)",
                    (name, budget, cat_type)
                )
            except sqlite3.IntegrityError:
                pass
        
        self.conn.commit()
    
    def add_transaction(self, date: str, description: str, amount: float, 
                       category: str, trans_type: str) -> int:
        # Add a new transaction
        self.cursor.execute("""
            INSERT INTO transactions (date, description, amount, category, type)
            VALUES (?, ?, ?, ?, ?)
        """, (date, description, amount, category, trans_type))
        
        self.conn.commit()
        return self.cursor.lastrowid
    
    def get_transactions(self, start_date: Optional[str] = None, 
                        end_date: Optional[str] = None,
                        category: Optional[str] = None) -> List[Tuple]:
        # Get transactions with optional filters
        query = "SELECT * FROM transactions WHERE 1=1"
        params = []
        
        if start_date:
            query += " AND date >= ?"
            params.append(start_date)
        
        if end_date:
            query += " AND date <= ?"
            params.append(end_date)
        
        if category:
            query += " AND category = ?"
            params.append(category)
        
        query += " ORDER BY date DESC"
        
        self.cursor.execute(query, params)
        return self.cursor.fetchall()
    
    def get_category_spending(self, start_date: str, end_date: str) -> List[Tuple]:
        # Get spending by category for a date range
        self.cursor.execute("""
            SELECT category, SUM(amount) as total
            FROM transactions
            WHERE type = 'expense' AND date BETWEEN ? AND ?
            GROUP BY category
            ORDER BY total DESC
        """, (start_date, end_date))
        
        return self.cursor.fetchall()
    
    def get_monthly_summary(self, year: int, month: int) -> dict:
        # Get income, expenses, and balance for a month
        start_date = f"{year}-{month:02d}-01"
        if month == 12:
            end_date = f"{year+1}-01-01"
        else:
            end_date = f"{year}-{month+1:02d}-01"
        
        self.cursor.execute("""
            SELECT type, SUM(amount) as total
            FROM transactions
            WHERE date >= ? AND date < ?
            GROUP BY type
        """, (start_date, end_date))
        
        results = dict(self.cursor.fetchall())
        income = results.get('income', 0)
        expenses = results.get('expense', 0)
        
        return {
            'income': income,
            'expenses': expenses,
            'balance': income - expenses,
            'month': f"{year}-{month:02d}"
        }
    
    def check_budget_alerts(self, year: int, month: int) -> List[dict]:
        # Check which categories exceeded budget
        start_date = f"{year}-{month:02d}-01"
        if month == 12:
            end_date = f"{year+1}-01-01"
        else:
            end_date = f"{year}-{month+1:02d}-01"
        
        self.cursor.execute("""
            SELECT 
                t.category,
                SUM(t.amount) as spent,
                c.budget_limit,
                (SUM(t.amount) / c.budget_limit * 100) as percentage
            FROM transactions t
            JOIN categories c ON t.category = c.name
            WHERE t.type = 'expense' 
                AND t.date >= ? 
                AND t.date < ?
                AND c.budget_limit > 0
            GROUP BY t.category, c.budget_limit
            HAVING spent >= c.budget_limit * 0.8
            ORDER BY percentage DESC
        """, (start_date, end_date))
        
        alerts = []
        for row in self.cursor.fetchall():
            alerts.append({
                'category': row[0],
                'spent': row[1],
                'limit': row[2],
                'percentage': row[3]
            })
        
        return alerts
    
    def get_categories(self, cat_type: Optional[str] = None) -> List[Tuple]:
        # Get all categories, optionally filtered by type
        if cat_type:
            self.cursor.execute(
                "SELECT name, budget_limit FROM categories WHERE type = ? ORDER BY name",
                (cat_type,)
            )
        else:
            self.cursor.execute("SELECT name, budget_limit, type FROM categories ORDER BY name")
        
        return self.cursor.fetchall()
    
    def update_budget_limit(self, category: str, new_limit: float):
        # Update budget limit for a category
        self.cursor.execute(
            "UPDATE categories SET budget_limit = ? WHERE name = ?",
            (new_limit, category)
        )
        self.conn.commit()
    
    def delete_transaction(self, transaction_id: int):
        # Delete a transaction by ID
        self.cursor.execute("DELETE FROM transactions WHERE id = ?", (transaction_id,))
        self.conn.commit()
    
    def close(self):
        # Close database connection
        self.conn.close()