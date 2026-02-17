"""
Auto-categorization module for transactions
Uses keyword matching to automatically categorize transactions
"""

from typing import Dict, List


class TransactionCategorizer:
    # Automatically categorizes transactions based on description keywords
    
    def __init__(self):
        # Initialize with keyword mappings
        self.category_keywords = {
            'Food & Dining': [
                'restaurant', 'cafe', 'food', 'grocery', 'supermarket',
                'starbucks', 'mcdonald', 'pizza', 'burger', 'delivery',
                'uber eats', 'doordash', 'grubhub', 'dining'
            ],
            'Transportation': [
                'gas', 'fuel', 'uber', 'lyft', 'taxi', 'parking',
                'car wash', 'toll', 'metro', 'bus', 'train', 'subway',
                'vehicle', 'maintenance', 'repair'
            ],
            'Shopping': [
                'amazon', 'walmart', 'target', 'mall', 'store',
                'clothing', 'shoes', 'electronics', 'online shopping',
                'ebay', 'etsy', 'fashion', 'retail'
            ],
            'Bills & Utilities': [
                'electric', 'water', 'gas bill', 'internet', 'phone',
                'cable', 'insurance', 'rent', 'mortgage', 'utility',
                'subscription', 'netflix', 'spotify', 'hulu'
            ],
            'Entertainment': [
                'movie', 'cinema', 'theater', 'concert', 'game',
                'streaming', 'hobby', 'sports', 'gym', 'fitness',
                'recreation', 'amusement', 'ticket'
            ],
            'Healthcare': [
                'pharmacy', 'doctor', 'hospital', 'clinic', 'medical',
                'dentist', 'prescription', 'health', 'medicine',
                'therapy', 'wellness'
            ],
            'Salary': [
                'salary', 'payroll', 'wages', 'paycheck', 'employer',
                'direct deposit', 'income'
            ],
            'Freelance': [
                'freelance', 'consulting', 'contract', 'gig',
                'side job', 'project payment'
            ]
        }
    
    def categorize(self, description: str) -> str:
        """
        Categorize a transaction based on its description
        
        Args:
            description: Transaction description text
            
        Returns:
            Category name or 'Other Expenses'/'Other Income' if no match
        """
        description_lower = description.lower()
        
        # Check each category's keywords
        for category, keywords in self.category_keywords.items():
            for keyword in keywords:
                if keyword in description_lower:
                    return category
        
        # Default categories
        return 'Other Expenses'
    
    def get_suggested_category(self, description: str, amount: float) -> str:
        """
        Get suggested category with amount consideration
        
        Args:
            description: Transaction description
            amount: Transaction amount (positive for income, negative for expense)
            
        Returns:
            Suggested category name
        """
        base_category = self.categorize(description)
        
        # If it's income and not categorized as Salary/Freelance
        if amount > 0 and base_category.startswith('Other'):
            if any(word in description.lower() for word in ['salary', 'payroll', 'employer']):
                return 'Salary'
            elif any(word in description.lower() for word in ['freelance', 'consulting', 'contract']):
                return 'Freelance'
            else:
                return 'Other Income'
        
        return base_category
    
    def add_keyword(self, category: str, keyword: str):
        # Add a new keyword to a category
        if category in self.category_keywords:
            if keyword.lower() not in self.category_keywords[category]:
                self.category_keywords[category].append(keyword.lower())
        else:
            self.category_keywords[category] = [keyword.lower()]
    
    def get_category_keywords(self, category: str) -> List[str]:
        # Get all keywords for a specific category
        return self.category_keywords.get(category, [])