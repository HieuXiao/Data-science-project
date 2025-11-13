# main.py

import os
import sys
import pandas as pd

# Import functions for data ingestion
from src.ingestion.data_fetcher import (
    fetch_product_ids,
    fetch_product_details,
    fetch_product_comments
)

# Import cleaning functions from src/utils.py
from src.utils import clean_product_data, clean_comments_data


# Add imports for Visualization modules (will be needed later)
# UNCOMMENT THESE LINES WHEN YOU IMPLEMENT THE CODE INSIDE THE CORRESPONDING FILES
# from src.visualization.line_bar_plot import create_line_bar_plot
# from src.visualization.box_plot import create_box_plot
# from src.visualization.scatter_plot import create_scatter_plot

# Placeholder functions for Visualization (Replace with actual code later)
def create_line_bar_plot(input_path, output_path):
    """Placeholder for creating a line and bar plot."""
    pass


def create_box_plot(input_path, output_path):
    """Placeholder for creating a box plot."""
    pass


def create_scatter_plot(input_path, output_path):
    """Placeholder for creating a scatter plot."""
    pass


# Placeholder function for Data Cleaning (Not strictly needed since we use run_data_cleaning)
def clean_data(input_path):
    """Placeholder for a generic data cleaning function."""
    pass


def setup_environment():
    """
    Creates 'data' and 'reports' directories if they do not exist.
    This ensures necessary file paths are ready before execution.
    """
    if not os.path.exists('data'):
        os.makedirs('data')
        print("Created directory 'data/'.")
    if not os.path.exists('reports'):
        os.makedirs('reports')
        print("Created directory 'reports/'.")


def run_data_ingestion():
    """
    Executes the entire Data Ingestion workflow from Tiki.
    This involves fetching product IDs, details, and comments.
    """
    print("\n--- Starting Data Ingestion workflow from Tiki ---")

    # Step 1: Fetch Product IDs (Tiki Bookstore Category: 8322)
    df_ids = fetch_product_ids(category_id='8322', max_pages=20, output_path='data/product_id_sach.csv')

    if df_ids.empty:
        print("\nProcess halted because no product IDs were collected.")
        return

    # Step 2: Fetch Product Details
    fetch_product_details(input_path='data/product_id_sach.csv', output_path='data/crawled_data_sach.csv')

    # Step 3: Fetch Product Comments
    fetch_product_comments(input_path='data/product_id_sach.csv', max_comment_pages=5, output_path='data/comments_data_sach.csv')

    print("\n--- Data Ingestion workflow completed! ---")


def run_data_cleaning():
    """
    Executes the data cleaning functionality for both product details and comments data.
    It checks for input files and saves the cleaned output.
    """

    # 1. Clean Product Details
    input_product_file = 'data/crawled_data_sach.csv'
    output_product_file = 'data/cleaned_product_sach.csv'

    if os.path.exists(input_product_file):
        print(f"\n--- Starting cleaning for product details from {input_product_file} ---")
        df_raw = pd.read_csv(input_product_file)
        # Call the cleaning function from src/utils.py
        df_cleaned = clean_product_data(df_raw)

        # Save the cleaning result
        if not df_cleaned.empty:
            df_cleaned.to_csv(output_product_file, index=False)
            print(f"✅ Saved {len(df_cleaned)} cleaned data rows to: {output_product_file}")
    else:
        print(f"\n⚠️ Skipping Product Details cleaning: Input file {input_product_file} not found. Please run Data Ingestion (Option 1) first.")

    # 2. Clean Product Comments
    input_comment_file = 'data/comments_data_sach.csv'
    output_comment_file = 'data/cleaned_comments_sach.csv'

    if os.path.exists(input_comment_file):
        print(f"\n--- Starting cleaning for product comments from {input_comment_file} ---")
        df_raw = pd.read_csv(input_comment_file)
        # Call the cleaning function from src/utils.py
        df_cleaned = clean_comments_data(df_raw)

        # Save the cleaning result
        if not df_cleaned.empty:
            df_cleaned.to_csv(output_comment_file, index=False)
            print(f"✅ Saved {len(df_cleaned)} cleaned data rows to: {output_comment_file}")
    else:
        print(f"\n⚠️ Skipping Comments cleaning: Input file {input_comment_file} not found. Please run Data Ingestion (Option 1) first.")


def run_visualization_plots():
    """
    Displays the Visualization submenu and handles user plot selection.
    It calls placeholder functions for plot creation.
    """
    # Define input/output paths for Visualization
    INPUT_DATA_PATH = 'data/cleaned_product_sach.csv'

    # Check if the data file exists
    if not os.path.exists(INPUT_DATA_PATH):
        print(f"\n⚠️ Error: Input data file not found: {INPUT_DATA_PATH}. Please run Data Ingestion (Option 1) first.")
        return

    while True:
        print("\n----------------------------------------------")
        print("📊 SELECT VISUALIZATION PLOT 📊")
        print("----------------------------------------------")
        print("3.1. Line-Bar Plot (Trend analysis)")
        print("3.2. Box-plot (Distribution & outliers)")
        print("3.3. Scatter Plot (Variable relationships)")
        print("3.4. 🔙 Back to Main Menu")
        print("----------------------------------------------")

        vis_choice = input("Please select plot type (e.g., 3.1): ").strip()

        if vis_choice=='3.1':
            print("Creating Line-Bar Plot...")
            # Call the actual function after implementation
            create_line_bar_plot(input_path=INPUT_DATA_PATH, output_path='reports/line_bar_plot.png')
            print("Called function for Line-Bar Plot (Needs implementation in src/visualization/line_bar_plot.py)")
        elif vis_choice=='3.2':
            print("Creating Box-plot...")
            create_box_plot(input_path=INPUT_DATA_PATH, output_path='reports/box_plot.png')
            print("Called function for Box-plot (Needs implementation in src/visualization/box_plot.py)")
        elif vis_choice=='3.3':
            print("Creating Scatter Plot...")
            create_scatter_plot(input_path=INPUT_DATA_PATH, output_path='reports/scatter_plot.png')
            print("Called function for Scatter Plot (Needs implementation in src/visualization/scatter_plot.py)")
        elif vis_choice=='3.4':
            break
        else:
            print("Invalid choice. Please re-enter (e.g., 3.1 or 3.4).")


def main_menu():
    """
    Displays the main menu and handles user selection for the entire data workflow.
    It orchestrates the setup, ingestion, cleaning, and visualization stages.
    """

    setup_environment()

    while True:
        print("\n==============================================")
        print("🚀 TIKI DATA SCIENCE PROJECT MENU 🚀")
        print("==============================================")
        print("1. 📥 Data Ingestion (Crawl data from Tiki API)")
        print("2. 🧹 Data Cleaning (Clean crawled data)")
        print("3. 📊 Data Visualization (Visualize cleaned data)")
        print("4. ❌ Exit")
        print("==============================================")

        choice = input("Please select a function (Enter number): ").strip()

        if choice=='1':
            run_data_ingestion()
        elif choice=='2':
            run_data_cleaning()  # Call Data Cleaning function
        elif choice=='3':
            run_visualization_plots()  # Call Visualization submenu
        elif choice=='4':
            print("Goodbye! See you again.")
            sys.exit(0)
        else:
            print("Invalid choice. Please re-enter a number from 1 to 4.")


if __name__=="__main__":
    main_menu()
