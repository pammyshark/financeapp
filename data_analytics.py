import pandas as pd
import matplotlib.pyplot as plt


def analyze_category_spending(data):
    """Prints total spending by category"""
    print("--- Total Spending by Category ---")
    analyze_cat = data.groupby(['Category']).sum()
    print(analyze_cat)

def calculate_avg_monthly_spending(data):
    """Prints average monthly spending"""
    print("--- Average Monthly Spending ---")
    avg_monthly = data.groupby(pd.PeriodIndex(data['Date'], freq="M"))['Amount'].mean()
    print(avg_monthly)

def top_spending_category(data):
    """Shows the category with the highest spent"""
    print("--- Top Spending Category ---")

    analyze_cat = data.groupby('Category')['Amount'].sum()

    # Finding category with the highest spending
    top_category = analyze_cat.idxmax()  # Get the category with the highest sum with idxmax
    top_spending = analyze_cat.max()  # Get the corresponding total spending

    # Display the result
    print(f"{top_category} with a total spending of {top_spending:.2f}.")

def plot_monthly_spending(data):
    """Visualize monthly spending trend"""
    data['Date'] = pd.to_datetime(data['Date'])
    data['YearMonth'] = data['Date'].dt.to_period('M')
    monthly_spending = data.groupby('YearMonth')['Amount'].sum()

    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(monthly_spending.index.astype(str), monthly_spending.values, marker='o', linestyle='-', color='b')
    plt.title('Monthly Spending', fontsize=16)
    plt.xlabel('Month (Year-Month)', fontsize=14)
    plt.ylabel('Amount', fontsize=14)
    plt.xticks(rotation=45)
    plt.grid(alpha=0.5)
    plt.tight_layout()
    plt.show()
