class PersonalFinanceApp:
    """
    The main application class that handles the user interface and menu navigation.
    It relies on a TransactionManager instance to handle transaction-related operations.
    """
    def __init__(self):
        self.transaction_manager = None

    def start_menu(self):
        """Displays the main menu and handles user input."""

        while True:
            self.print_menu_options()
            choice = input("Choose an option (0-11): ").strip()

            if choice == "0":
                self.import_csv()
            elif choice == "1":
                self.view_all_transactions()
            elif choice == "2":
                self.view_transactions_by_date_range()
            elif choice == "3":
                self.add_transaction()
            elif choice == "4":
                self.edit_transaction()
            elif choice == "5":
                self.delete_transaction()
            elif choice == "6":
                self.analyze_spending_by_category()
            elif choice == "7":
                self.calculate_avg_monthly_spending()
            elif choice == "8":
                self.show_top_spending_category()
            elif choice == "9":
                self.monthly_income()
            elif choice == "10":
                self.category_budget()
            elif choice == "11":
                self.check_budget_status()
            elif choice == "12": # This is where the old ones moved.
                self.visualize_monthly_spending_trend()
            elif choice == "13":
                self.save_transactions_to_csv()
                # check budget status
                # Visualize spending trends
            elif choice == "14":
                print("Exiting program. Goodbye!")
                break
            else:
                print("Invalid choice. Please choose a valid option.")

    def print_menu_options(self):
        """Prints menu options"""
        print("0. Import a CSV File")
        print("1. View All Transactions")
        print("2. View Transactions by Date Range")
        print("3. Add a Transaction")
        print("4. Edit a Transaction")
        print("5. Delete a Transaction")
        print("6. Analyze Spending by Category")
        print("7. Calculate Average Monthly Spending")
        print("8. Show Top Spending Category")
        # New menu implementations
        print("9. Set Monthly Income")
        print("10. Set Category Budget")
        print("11. Check Budget Status")
        # Here go all the other functions
        print("12. Visualize Monthly Spending Trend")
        print("13. Save Transactions to CSV")
        print("14. Exit")
        print("15. Test")

    def ensure_data_loaded(self):
        """Check if data is loaded before proceeding with transaction operations."""
        if self.transaction_manager is None:
            print("Please import a CSV file first.")
            return False
        return True

    def import_csv(self):
        """Handles importing the CSV file."""
        from data_manager import load_csv
        from transaction_manager import TransactionManager

        filepath = input("Enter the path to the CSV file: ").strip()
        try:
            data = load_csv(filepath)
            self.transaction_manager = TransactionManager(data)
            print("File imported successfully!")
        except Exception as e:
            print(f"An error occurred while importing CSV: {e}")

    def view_all_transactions(self):
        if self.ensure_data_loaded():
            self.transaction_manager.view_all()

    def view_transactions_by_date_range(self):
        if self.ensure_data_loaded():
            self.transaction_manager.view_transactions_by_date()

    def add_transaction(self):
        if self.ensure_data_loaded():
            self.transaction_manager.add_transaction()

    def edit_transaction(self):
        if self.ensure_data_loaded():
            self.transaction_manager.edit_transaction()

    def delete_transaction(self):
        if self.ensure_data_loaded():
            self.transaction_manager.delete_transaction()

    def analyze_spending_by_category(self):
        if self.ensure_data_loaded():
            self.transaction_manager.analyze_spending_by_category()

    def calculate_avg_monthly_spending(self):
        if self.ensure_data_loaded():
            self.transaction_manager.calculate_avg_monthly_spending()

    def show_top_spending_category(self):
        if self.ensure_data_loaded():
            self.transaction_manager.show_top_spending_category()

    # New functions
    # put new functions here . The guide its on the menu
    def monthly_income(self):
        if self.ensure_data_loaded():
            self.transaction_manager.monthly_income()

    def category_budget(self):
        if self.ensure_data_loaded():
            self.transaction_manager.category_budget()
    def check_budget_status(self):
        self.check_budget_status()
    # These are the old ones
    def visualize_monthly_spending_trend(self):
        if self.ensure_data_loaded():
            self.transaction_manager.visualize_monthly_spending_trend()

    def save_transactions_to_csv(self):
        if self.ensure_data_loaded():
            self.transaction_manager.save_to_csv()
