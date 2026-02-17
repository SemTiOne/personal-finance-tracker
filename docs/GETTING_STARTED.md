# Getting Started with Personal Finance Tracker

This guide will help you set up and start using the Personal Finance Tracker.

## Step 1: Installation

### Prerequisites Check
```bash
# Check Python version (should be 3+)
python --version

# Check pip is installed
pip --version
```

### Install Dependencies
```bash
# Navigate to project directory
cd finance-tracker

# Install required packages
pip install -r requirements.txt
```

## Step 2: First Run

### Launch the Application
```bash
python main.py
```

### Create Sample Data (Recommended for First-Time Users)
1. Select option `9` from the main menu
2. This will create sample transactions you can explore
3. Go back to main menu and try other options

## Step 3: Explore Features

### View Transactions (Option 2)
- See all your transactions
- Filter by time period
- View totals and balance

### Generate Reports (Option 5)
1. **Spending Pie Chart**: Visual breakdown of expenses
2. **Monthly Trend**: Income vs expenses over 6 months
3. **Budget Comparison**: See how you're doing against budgets
4. **Text Summary**: Detailed monthly report

### Check Budget Alerts (Option 4)
- See if you're over budget in any category
- Get warnings at 80% of budget limit

## Step 4: Add Your Own Data

### Manual Entry (Option 1)
```
Date: 2026-02-15 (or press Enter for today)
Description: Lunch at restaurant
Amount: -45.50 (negative = expense, positive = income)
Category: [Auto-suggested or select from list]
```

### Import from CSV (Option 6)
Prepare your CSV file:
```csv
Date,Description,Amount
2026-02-01,Monthly Salary,3500.00
2026-02-02,Grocery Shopping,-125.50
2026-02-03,Gas Station,-42.00
```

Then import it through the application.

## Step 5: Customize Categories

### Update Budget Limits (Option 7)
1. View all categories
2. Select "Update budget limit"
3. Enter category name
4. Enter new monthly budget amount

Example:
- Food & Dining: $500/month
- Transportation: $200/month
- Entertainment: $150/month

## Common Workflows

### Weekly Review
1. View transactions for last 7 days (Option 2)
2. Check budget alerts (Option 4)
3. Categorize any "Other" transactions

### Monthly Analysis
1. View monthly summary (Option 3)
2. Generate spending pie chart (Option 5)
3. Generate budget comparison (Option 5)
4. Export data if needed (Option 8)

### Year-End Review
1. Generate monthly trend for 12 months
2. Export full year data to CSV
3. Review spending patterns by category

## Tips for Best Results

### Transaction Descriptions
- Be descriptive: "Lunch at Panera" vs "Food"
- Include merchant names for auto-categorization
- Consistent naming helps with tracking

### Categories
- Start with default categories
- Adjust budgets based on your actual spending
- Create new keywords for frequent merchants

### Reports
- Generate reports monthly to track progress
- Save important reports for records
- Use charts to identify spending patterns

## Troubleshooting

### "Module not found" Error
```bash
pip install -r requirements.txt --upgrade
```

### Database Issues
Delete `data/finance.db` and restart (data will be lost)

### Import Problems
- Check CSV format matches: Date, Description, Amount
- Ensure dates are in recognizable format
- Amounts: use negative for expenses, positive for income

## Next Steps

1. Import your bank statements
2. Set realistic budget limits
3. Review weekly spending
4. Adjust budgets as needed
5. Track your progress monthly

## Getting Help

- Check the README.md for detailed documentation
- Review test files for usage examples
- Explore the source code in `src/` directory

Happy tracking! 💰