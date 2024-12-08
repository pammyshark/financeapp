import pandas as pd
import matplotlib.pyplot as plt

class Document:
    def __init__(self):
        self.filepath = None # As we don't have the file yet
        self.functions_instance = None  # Placeholder for Functions instance

    def start_menu(self):
        """Starts the menu"""
        print("=== Personal Finance Tracker ===")

        while True:
            print("0. Import a CSV File")
            print("1. View All Transactions")
            print("2. View Transactions by Date Range")
            print("3. Add a Transaction")
            print("4. Edit a Transaction")
            print("5. Delete a Transaction")
            print("6. Analyze Spending by Category")
            print("7. Calculate Average Monthly Spending")
            print("8. Show Top Spending Category")
            print("9. Visualize Monthly Spending Trend")
            print("10. Save Transactions to CSV")
            print("11. Exit")

            choice = input("Choose an option (0-11): ").strip()

            if choice == "0":
                self.import_csv() # Goes to the import csv place
            elif choice == "1":
                if self.functions_instance:
                    self.functions_instance.view_all()
                else:
                    print("Please import a CSV file first.")
            elif choice == "2":
                if self.functions_instance:
                    self.functions_instance.view_transactions_by_date()
                else:
                    print("Please import a CSV file first.")
            elif choice == "3":
                if self.functions_instance:
                    self.functions_instance.add_transaction()
                    # Is putting full date but works
                else:
                    print("Please import a CSV file first.")
            elif choice == "4":
                if self.functions_instance:
                    self.functions_instance.edit_transaction()
                else:
                    print("Please import a CSV file first.")
            elif choice == "5":
                if self.functions_instance:
                    self.functions_instance.delete_transaction()
                else:
                    print("Please import a CSV file first.")
            elif choice == "6":
                if self.functions_instance:
                    self.functions_instance.analyze()
                else:
                    print("Please import a CSV file first.")
            elif choice == "7":
                if self.functions_instance:
                    self.functions_instance.avg_month()
            elif choice == "8":
                if self.functions_instance:
                    self.functions_instance.top_cat()
            elif choice == "9":
                if self.functions_instance:
                    self.functions_instance.viz_month()
            elif choice == "10":
                if self.functions_instance:
                    self.functions_instance.save_csv()
            elif choice == "11":
                print("Exiting program. Goodbye!")
                break
            else:
                print("Invalid choice. Please choose a valid option.")

    def import_csv(self):
        """Handles importing the CSV file."""
        filepath = input("Write the name of the CSV file: ").strip()
        try:
            data = pd.read_csv(filepath)
            self.functions_instance = Functions(data)
            print("File imported successfully!")
        except Exception as e:
            print(f"An error occurred: {e}")


class Functions:
    def __init__(self, data):
        self.data = data  # Store the DataFrame

    def view_all(self):
        """Displays all transactions."""
        print("--- All Transactions ---")
        print(self.data)

    def view_transactions_by_date(self):
        """Filters and displays transactions by date range."""
        try:
            self.data['Date'] = pd.to_datetime(self.data['Date'])  # Ensure 'Date' is datetime
            start_date = input("Enter start date (YYYY-MM-DD): ").strip()
            end_date = input("Enter end date (YYYY-MM-DD): ").strip()

            filtered_data = self.data[
                (self.data['Date'] >= start_date) & (self.data['Date'] <= end_date)
                ]
            if not filtered_data.empty: # I don't understand this "if not"
                print(f"--- Transactions from {start_date} to {end_date} ---")
                print(filtered_data)
            else:
                print("No transactions found in this date range.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def add_transaction(self):
        """Adds a transaction"""
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

    def analyze(self):
        """Speding for each category"""
        print("--- Total Spending by Category ---")
        analyze_cat = self.data.groupby(['Category']).sum()
        print(analyze_cat)

    def avg_month(self):
        """Average Monthly Spending"""
        print("--- Average Monthly Spending ---")
        avg_monthly = self.data.groupby(pd.PeriodIndex(self.data['Date'], freq="M"))['Amount'].mean()
        print(avg_monthly)


    def top_cat(self):
        """Displays the top spending category"""
        print("--- Top Spending Category ---")

        analyze_cat = self.data.groupby('Category')['Amount'].sum()

        # Finding category with the highest spending
        top_category = analyze_cat.idxmax()  # Get the category with the highest sum with idxmax
        top_spending = analyze_cat.max()  # Get the corresponding total spending

        # Display the result
        print(f"{top_category} with a total spending of {top_spending:.2f}.")

    def viz_month(self):
        """Visualize monthly spending trend"""
        self.data['Date'] = pd.to_datetime(self.data['Date'])
        self.data['YearMonth'] = self.data['Date'].dt.to_period('M')
        monthly_spending = self.data.groupby('YearMonth')['Amount'].sum()

        # Plotting
        plt.figure(figsize=(10, 6))
        plt.plot(monthly_spending.index.astype(str), monthly_spending.values, marker='o', linestyle='-', color='b')
        plt.title('Monthly Spending', fontsize=16)
        plt.xlabel('Month (Year-Month)', fontsize=14)
        plt.ylabel('Total Spending', fontsize=14)
        plt.xticks(rotation=45)
        plt.grid(alpha=0.5)
        plt.tight_layout()
        plt.show()

    def save_csv(self):
        """Save csv"""
        new_csv = input("Enter file name to save (e.g., 'transactions.csv'): ").strip()
        self.data.to_csv(new_csv, index=False)
        print("Transactions saved to my_transactions.csv successfully!")


# Starting the program
if __name__ == "__main__":
    doc = Document()
    doc.start_menu()
