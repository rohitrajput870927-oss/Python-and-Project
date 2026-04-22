import csv
import os
from datetime import datetime
import matplotlib.pyplot as plt
from collections import defaultdict

class FinanceTracker:
    def __init__(self, filename='transactions.csv'):
        self.filename = filename
        self.transactions = []
        self.load_transactions()
    
    def load_transactions(self):
        """Load existing transactions from CSV file"""
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                reader = csv.DictReader(file)
                self.transactions = list(reader)
    
    def save_transaction(self, transaction):
        """Save a new transaction to CSV file"""
        file_exists = os.path.exists(self.filename)
        with open(self.filename, 'a', newline='') as file:
            fieldnames = ['date', 'category', 'description', 'amount', 'type']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            
            if not file_exists:
                writer.writeheader()
            writer.writerow(transaction)
        
        self.transactions.append(transaction)
    
    def add_transaction(self):
        """Add a new transaction"""
        print("\n--- Add New Transaction ---")
        date = input("Date (YYYY-MM-DD) or press Enter for today: ").strip()
        if not date:
            date = datetime.now().strftime('%Y-%m-%d')
        
        print("\nCategories: Food, Transport, Entertainment, Shopping, Bills, Salary, Other")
        category = input("Category: ").strip().capitalize()
        description = input("Description: ").strip()
        
        while True:
            try:
                amount = float(input("Amount: "))
                break
            except ValueError:
                print("Please enter a valid number!")
        
        trans_type = input("Type (income/expense): ").strip().lower()
        while trans_type not in ['income', 'expense']:
            trans_type = input("Please enter 'income' or 'expense': ").strip().lower()
        
        transaction = {
            'date': date,
            'category': category,
            'description': description,
            'amount': str(amount),
            'type': trans_type
        }
        
        self.save_transaction(transaction)
        print("✓ Transaction added successfully!")
    
    def view_transactions(self):
        """Display all transactions"""
        if not self.transactions:
            print("\nNo transactions found!")
            return
        
        print("\n" + "="*80)
        print(f"{'Date':<12} {'Category':<15} {'Description':<25} {'Amount':<10} {'Type':<10}")
        print("="*80)
        
        for t in self.transactions:
            amount_str = f"₹{float(t['amount']):,.2f}"
            print(f"{t['date']:<12} {t['category']:<15} {t['description']:<25} {amount_str:<10} {t['type']:<10}")
    
    def get_summary(self):
        """Calculate and display financial summary"""
        if not self.transactions:
            print("\nNo transactions to summarize!")
            return
        
        total_income = sum(float(t['amount']) for t in self.transactions if t['type'] == 'income')
        total_expense = sum(float(t['amount']) for t in self.transactions if t['type'] == 'expense')
        balance = total_income - total_expense
        
        print("\n" + "="*40)
        print("        FINANCIAL SUMMARY")
        print("="*40)
        print(f"Total Income:   ₹{total_income:,.2f}")
        print(f"Total Expenses: ₹{total_expense:,.2f}")
        print(f"Balance:        ₹{balance:,.2f}")
        print("="*40)
    
    def visualize_expenses(self):
        """Create pie chart of expenses by category"""
        if not self.transactions:
            print("\nNo data to visualize!")
            return
        
        expenses = [t for t in self.transactions if t['type'] == 'expense']
        if not expenses:
            print("\nNo expenses to visualize!")
            return
        
        category_totals = defaultdict(float)
        for t in expenses:
            category_totals[t['category']] += float(t['amount'])
        
        categories = list(category_totals.keys())
        amounts = list(category_totals.values())
        
        plt.figure(figsize=(10, 7))
        plt.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=90)
        plt.title('Expenses by Category', fontsize=16, fontweight='bold')
        plt.axis('equal')
        plt.tight_layout()
        plt.show()
    
    def visualize_monthly_trend(self):
        """Create bar chart of monthly income vs expenses"""
        if not self.transactions:
            print("\nNo data to visualize!")
            return
        
        monthly_income = defaultdict(float)
        monthly_expense = defaultdict(float)
        
        for t in self.transactions:
            month = t['date'][:7]  # Extract YYYY-MM
            amount = float(t['amount'])
            
            if t['type'] == 'income':
                monthly_income[month] += amount
            else:
                monthly_expense[month] += amount
        
        months = sorted(set(list(monthly_income.keys()) + list(monthly_expense.keys())))
        income_values = [monthly_income[m] for m in months]
        expense_values = [monthly_expense[m] for m in months]
        
        x = range(len(months))
        width = 0.35
        
        plt.figure(figsize=(12, 6))
        plt.bar([i - width/2 for i in x], income_values, width, label='Income', color='green', alpha=0.7)
        plt.bar([i + width/2 for i in x], expense_values, width, label='Expenses', color='red', alpha=0.7)
        
        plt.xlabel('Month', fontsize=12)
        plt.ylabel('Amount (₹)', fontsize=12)
        plt.title('Monthly Income vs Expenses', fontsize=16, fontweight='bold')
        plt.xticks(x, months, rotation=45)
        plt.legend()
        plt.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        plt.show()

def main():
    tracker = FinanceTracker()
    
    while True:
        print("\n" + "="*40)
        print("   PERSONAL FINANCE TRACKER")
        print("="*40)
        print("1. Add Transaction")
        print("2. View All Transactions")
        print("3. View Summary")
        print("4. Visualize Expenses by Category")
        print("5. Visualize Monthly Trend")
        print("6. Exit")
        print("="*40)
        
        choice = input("Enter your choice (1-6): ").strip()
        
        if choice == '1':
            tracker.add_transaction()
        elif choice == '2':
            tracker.view_transactions()
        elif choice == '3':
            tracker.get_summary()
        elif choice == '4':
            tracker.visualize_expenses()
        elif choice == '5':
            tracker.visualize_monthly_trend()
        elif choice == '6':
            print("\nThank you for using Finance Tracker! Goodbye!")
            break
        else:
            print("\n❌ Invalid choice! Please try again.")

if __name__ == "__main__":
    main()