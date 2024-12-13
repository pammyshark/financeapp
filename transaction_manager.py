import pandas as pd
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

    def top_spending_category(self):
        """Shows top spending category"""
        top_spending_category(self.data)

    def visualize_monthly_spending_trend(self):
        """Visualize monthly spending trend"""
        plot_monthly_spending(self.data)

    def save_to_csv(self):
        """Save transactions to a CSV file"""
        new_csv = input("Enter file name to save (e.g., 'transactions.csv'): ").strip()
        try:
            save_csv(self.data, new_csv)
            print(f"Transactions saved to {new_csv} successfully!")
        except Exception as e:
            print(f"An error occurred while saving: {e}")

