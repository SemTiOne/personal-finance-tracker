# Personal Finance Tracker 💰

A Python-based command-line application for tracking personal finances, managing budgets, and generating insightful financial reports.

![Python](https://img.shields.io/badge/Python-3+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## Features

### 📊 Core Functionality
- Add, view, and categorize income and expenses
- Automatically categorizes transactions based on keywords
- Set budget limits for categories and get alerts
- Import transactions from bank statements or export data
- Generate pie charts, trend lines, and budget comparison charts
- View detailed financial summaries by month

### 🎯 Key Capabilities
- SQLite database for reliable data storage
- Smart transaction categorization using keyword matching
- Budget alerts when spending exceeds limits
- Multiple visualization types (pie charts, line graphs, bar charts)
- CSV import with flexible date/amount parsing
- Export data for external analysis

## Installation

### Prerequisites
- Python 3 or higher
- pip (Python package manager)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/SemTiOne/finance-tracker.git
cd finance-tracker
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python main.py
```

## Usage

### Quick Start

1. **Create Sample Data** (Option 9): Generate sample transactions to explore features
2. **View Transactions** (Option 2): See your transaction history
3. **Generate Reports** (Option 5): Create visual charts and summaries

### Adding Transactions

```
Select Option 1: Add Transaction

Date: 2026-02-01 (or press Enter for today)
Description: Grocery shopping at Whole Foods
Amount: -125.50 (negative for expense, positive for income)
Category: [Auto-suggested based on description]
```

### Importing from CSV

Prepare your CSV file with these columns:
- Date (various formats supported: YYYY-MM-DD, MM/DD/YYYY, etc.)
- Description
- Amount (positive for income, negative for expense)

```csv
Date,Description,Amount
2026-02-01,Salary - ABC Corp,3500.00
2026-02-02,Grocery Store,-125.50
2026-02-03,Gas Station,-45.00
```

Select Option 6 and provide the file path.

### Generating Reports

**Spending Pie Chart**: Visualize spending distribution by category
- Shows percentage breakdown
- Helps identify spending patterns

**Monthly Trend**: Track income vs expenses over time
- 6-month trend by default
- Shows balance trajectory

**Budget Comparison**: Compare actual spending vs budget limits
- Identifies overspending
- Visual budget performance

## Project Structure

```
finance-tracker/
├── 📄 README.md                        # Complete project documentation
├── 📄 LICENSE                          # MIT License
├── 📄 requirements.txt                 # Python dependencies (matplotlib, pandas)
├── 📄 .gitignore                       # Git exclusions
│
├── 🐍 main.py                          # Main CLI application 
│                                       # - Interactive menu system
│                                       # - User input handling
│                                       # - Feature coordination
│
├── 📁 src/                             # Core application modules
│   ├── 🐍 __init__.py                  # Package initialization
│   ├── 🐍 database.py                  # Database operations 
│   │                                   # - SQLite management
│   │                                   # - CRUD operations
│   │                                   # - Budget tracking queries
│   ├── 🐍 categorizer.py               # Auto-categorization 
│   │                                   # - Keyword-based matching
│   │                                   # - 10 default categories
│   │                                   # - 100+ keywords
│   ├── 🐍 analyzer.py                  # Data analysis 
│   │                                   # - Pandas DataFrames
│   │                                   # - Matplotlib charts
│   │                                   # - Report generation
│   └── 🐍 csv_import.py                # CSV processing 
│                                       # - Flexible date parsing
│                                       # - Currency handling
│                                       # - Sample data generator
│
├── 📁 tests/                           # Unit tests
│   └── 🧪 test_categorizer.py          # Categorization test suite (10+ tests)
│
├── 📁 docs/                            # Documentation
│   ├── 📖 GETTING_STARTED.md           # Step-by-step tutorial
│
├── 📁 .vscode/                         # VS Code configuration
│   └── ⚙️  settings.json               # Python path settings
│
├── 📁 data/                            # Database & data files (auto-created)
│   ├── 💾 finance.db                   # SQLite database
│   └── 📊 sample_transactions.csv      # Generated sample data
│
└── 📁 reports/                         # Generated outputs (auto-created)
    ├── 📊 spending_pie_*.png           # Category spending charts
    ├── 📈 trend_*.png                  # Monthly trend graphs
    ├── 📊 budget_comparison_*.png      # Budget vs actual charts
    ├── 📄 transactions_*.csv           # Exported transaction data
    └── 📄 summary_*.txt                # Text summary reports
```

### Key Features by Module

**main.py** - User Interface
- 10 interactive menu options
- Input validation & error handling
- Feature orchestration

**database.py** - Data Management
- 3 database tables
- 12+ query methods
- Automatic schema creation

**categorizer.py** - Intelligence
- Smart keyword matching
- 10 spending categories
- Extensible system

**analyzer.py** - Insights
- 3 chart types (pie, line, bar)
- Pandas data processing
- CSV export functionality

**csv_import.py** - Data Import
- Multiple date format support
- Currency symbol handling
- Batch transaction import

## Database Schema

### Transactions Table
```sql
CREATE TABLE transactions (
    id INTEGER PRIMARY KEY,
    date TEXT NOT NULL,
    description TEXT NOT NULL,
    amount REAL NOT NULL,
    category TEXT NOT NULL,
    type TEXT NOT NULL,  -- 'income' or 'expense'
    created_at TEXT
);
```

### Categories Table
```sql
CREATE TABLE categories (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    budget_limit REAL DEFAULT 0,
    type TEXT NOT NULL  -- 'income' or 'expense'
);
```

## Technical Highlights

### 1. Database Design
- Normalized schema with separate tables for transactions and categories
- Foreign key relationships for data integrity
- Indexed queries for performance

### 2. Auto-Categorization Algorithm
- Keyword-based pattern matching
- Context-aware categorization (amount + description)
- Extensible keyword dictionary

### 3. Data Analysis
- Pandas DataFrames for efficient data manipulation
- Matplotlib for professional visualizations
- Aggregation queries for summary statistics

### 4. CSV Processing
- Multiple date format support
- Currency symbol parsing
- Error handling for malformed data

## Example Use Cases

### Personal Budget Management
Track monthly expenses, set category budgets, and receive alerts when approaching limits.

### Financial Planning
Analyze spending trends over time to make informed decisions about savings and investments.

### Expense Reporting
Import bank statements, categorize transactions, and generate reports for tax purposes.

### Multi-Account Tracking
Import transactions from multiple accounts and view consolidated financial picture.

## Future Enhancements

- [ ] Web interface using Flask/Django
- [ ] Mobile app integration
- [ ] Recurring transaction support
- [ ] Goal tracking (savings goals)
- [ ] Investment portfolio tracking
- [ ] Multi-currency support
- [ ] Cloud backup/sync
- [ ] Machine learning for smarter categorization

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/SemTiOne/personal-finance-tracker/blob/main/LICENSE) file for details.

## Acknowledgments

- Built with Python 3
- Data visualization powered by Matplotlib
- Data analysis with Pandas
- Database using SQLite3

## Contact

Dane Parin - [@DParin28178](https://x.com/@DParin28178)

Project Link: [https://github.com/SemTiOne/finance-tracker](https://github.com/SemTiOne/finance-tracker)

---

**Note**: This is a portfolio project designed to demonstrate Python programming, database design, data analysis, and software architecture skills. It's suitable for personal use and can be extended with additional features.
