import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from data_analytics import (
    analyze_category_spending,
    calculate_avg_monthly_spending,
    top_spending_category,
    plot_monthly_spending
)
from data_manager import save_csv
class TransactionManager:
    """
    Manages all the transaction data operations: viewing, editing, deleting and analyze.
    """
    def __init__(self, data):
        self.data = data
        self._date_column_verification()
        self.input_budget = {}
    def _date_column_verification(self):
        """
        Ensures that the column is in the right format
        """
        if 'Date' in self.data.columns:
            try:
                self.data['Date'] = pd.to_datetime(self.data['Date'])  # Ensure 'Date' is datetime
            except Exception as e:
                print("Error converting 'Date' column to datetime:", e)

    def view_all(self):
        """Displays all transactions."""
        print("--- All Transactions ---")
        print(self.data)

    def view_transactions_by_date(self):
        """Filters and displays transactions by date range."""
        if 'Date' not in self.data.columns:
            print("No 'Date' column found in data.")
            return

        start_date = input("Enter start date (YYYY-MM-DD): ").strip()
        end_date = input("Enter end date (YYYY-MM-DD): ").strip()

        try:
            filtered_data = self.data[
                (self.data['Date'] >= start_date) & (self.data['Date'] <= end_date)]
            if not filtered_data.empty:
                print(f"--- Transactions from {start_date} to {end_date} ---")
                print(filtered_data)
            else:
                print("No transactions found in this date range.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def add_transaction(self):
        """Adds a new transaction to the dataset."""
        try:
            new_date = input("Enter the date (YYYY-MM-DD): ").strip()
            new_category = input("Enter the category (e.g., Food, Rent): ").strip()
            new_description = input("Enter a description: ").strip()
            new_amount = input("Enter the amount: ").strip()

            new_date = pd.to_datetime(new_date) # Converting to datetime
            new_amount = float(new_amount)

            # Making it a dictionary
            new_transaction = {
                "Date": new_date,
                "Category": new_category,
                "Description": new_description,
                "Amount": new_amount,
            }

            # Appending to Dataframe "data"
            self.data = pd.concat([self.data, pd.DataFrame([new_transaction])], ignore_index=True)
            print("Transaction added successfully!")

        except ValueError as e:
            print(f"Invalid input: {e}")

    def edit_transaction(self):
        """Edits the transaction according the index of which the user wants to change"""
        try:
            user_index = int(input("Enter the index of the transaction to edit: ").strip())

            # Show all the information from that row
            current_transaction = self.data.iloc[user_index]
            print("Current Transaction Details:")
            print(current_transaction)

            # Edit the values of "Date" or keep current ones if the user presses "enter"
            edit_date = input("Enter new date (YYYY-MM-DD) or press Enter to keep current: ").strip()
            if edit_date:
                try:
                    self.data.loc[user_index, 'Date'] = pd.to_datetime(edit_date)
                except ValueError:
                    print("Invalid date format. Keeping the current value.")

            # Edit the values of "Category" or keep current ones if the user presses "enter"
            edit_category = input("Enter new category or press Enter to keep current: ").strip()
            if edit_category:
                self.data.loc[user_index, 'Category'] = edit_category

            # Edit the values "Description" or keep current ones if the user presses "enter"
            edit_description = input("Enter new description or press Enter to keep current: ").strip()
            if edit_description:
                self.data.loc[user_index, 'Description'] = edit_description

            # Edit the values "Amount" or keep current ones if the user presses "enter"
            edit_amount = input("Enter new amount or press Enter to keep current: ")
            if edit_amount:
                self.data.loc[user_index, 'Amount'] = float(edit_amount)

            print("\nTransaction updated successfully!")
            print(self.data.iloc[user_index])

        except ValueError:
            print("Invalid index.")

    def delete_transaction(self):
        """Deletes the row of a transaction"""
        try:
            # Prompt user to delete the transaction index
            del_transaction = int(input("Enter the index of the transaction to delete: ").strip())
            self.data = self.data.drop(index=self.data.index[del_transaction]).reset_index(drop=True)
            print("Transaction deleted successfully!")
            # Ensure the index exists
            if del_transaction < 0 or del_transaction >= len(self.data):
                print("Invalid index.")
                return

        except ValueError:
            print("Invalid input.")

    def analyze_spending_by_cat(self):
        """Spending for each category"""
        analyze_category_spending(self.data)

    def calculate_avg_monthly_spending(self):
        """Displays average monthly spending"""
        calculate_avg_monthly_spending(self.data)

    # New functions
    def monthly_income(self):
        """Sets monthly income"""
        try:
            # Prompt user to delete the transaction index
            income = int(input("Enter your total monthly income: ").strip())
            print(f"Your monthly income is set to: ${income}")
            # Ensure the index exists
            if income < 0:
                print("Invalid Income")
                return

        except ValueError:
            print("Invalid input.")

    def category_budget(self):
        """Sets budget by category"""
        print("--- Top Spending Categories ---")

        # Get unique categories from database
        get_cat = self.data['Category'].unique()

        # Prompt user to enter budget for each category.
        input_budget = {}
        for category in get_cat:
            while True:
                try:
                    budget = int(input(f"Enter your budget {category}: "))
                    self.input_budget[category] = budget
                    break
                except ValueError:
                    print("Invalid input. Please enter a numeric value.")
        print("Your budgets have been set:")
        # Printing each category with the budget that was set up.
        for category, budget in self.input_budget.items():
            print(f"-{category}: {budget}")

    def check_budget_status(self):
        """
         Compares the user-defined budget (input_budget) with actual spending (analyze_cat)
        and displays whether categories are within or exceed the budget.
        """
        print("--- Budget Status ---")

        # Ensure input_budget exists
        if not self.input_budget:
            print("No budgets have been set. Please run `category_budget` first.")
            return

        # compare current budget vs budgeted budget.
        analyze_cat = self.data.groupby('Category')['Amount'].sum()

        # Store the comparison results
        suggestions = []

        # Compare each category's spending with its budget
        for category, budget in self.input_budget.items():
            spent = analyze_cat.get(category, 0)  # Get actual spending; default to 0 if category is not found
            if spent > budget:
                print(f"- {category}: Spent {spent}/{budget} (Exceeded Budget)")
                suggestions.append(f"Consider reducing spending in '{category}' or adjusting the budget.")
            elif spent >= budget * 0.75: # Spending is close to budget (75% or higher)
                print(f"- {category}: Spent {spent}/{budget} (Warning: Close to budget!)")
            else:
                #Spending is within the budget
                print(f"- {category}: Spent {spent}/{budget} (Within Budget)")

        # Display suggestions
        if suggestions:
            print("\nSuggestions:")
            for suggestion in suggestions:
                print(f"- {suggestion}")
        else:
            print("\nYou are within budget for all categories. Keep up the good work!")
    def top_spending_category(self):
        """Shows top spending category"""
        top_spending_category(self.data)

    def visualize_monthly_spending_trend(self):
        """Visualize monthly spending trend"""
        # This one is in another function in another document
        plot_monthly_spending(self.data)
        # Bar Chart
        actual_spending = self.data.groupby('Category')['Amount'].sum()

        # Aligning budget with its categories
        categories = actual_spending.index  # Categories from the actual spending
        budgets = [self.input_budget.get(category, 0) for category in categories]
        spent = actual_spending.values

        # Bar Chart: Actual Spending vs Budget
        n = len(categories)
        r = np.arange(n)  # Bar positions

        plt.figure(figsize=(10, 6))
        plt.bar(r, spent, color='b', width=0.4, edgecolor='black', label='Actual Spending')
        plt.bar(r + 0.4, budgets, color='g', width=0.4, edgecolor='black', label='Budget')

        plt.xlabel("Category")
        plt.ylabel("Amount")
        plt.title("Actual Spending Vs. Budget")
        plt.xticks(r + 0.2, categories)  # Center the ticks between bars
        plt.legend()
        plt.tight_layout()
        plt.show()

        # Pie Chart: Distribution of Actual Spending
        plt.figure(figsize=(8, 8))
        plt.title("Actual Spending Distribution")
        plt.pie(
            spent,
            labels=categories,
            autopct='%1.1f%%',  # Add percentage values
            explode=[0.05] * len(categories),  # Slightly explode each slice
            startangle=140
        )
        plt.show()

    def save_to_csv(self):
        """Save transactions to a CSV file"""
        new_csv = input("Enter file name to save (e.g., 'transactions.csv'): ").strip()
        try:
            save_csv(self.data, new_csv)
            print(f"Transactions saved to {new_csv} successfully!")
        except Exception as e:
            print(f"An error occurred while saving: {e}")
