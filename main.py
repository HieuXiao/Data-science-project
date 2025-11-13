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

# Import cleaning and merge functions from src/utils.py
from src.utils import clean_product_data, clean_comments_data, merge_product_and_comment_data

# >>> VISUALIZATION IMPORTS <<<
# Import implemented Visualization functions
from src.visualization.line_bar_plot import (
    create_line_bar_plot,  # Brand Stats
    create_line_bar_time_series_plot  # Time Series Trend
)


# Placeholder functions for Visualization modules (to prevent NameError before implementation)
def create_box_plot(input_path, output_path):
    """Placeholder for creating a box plot. (To be implemented in src/visualization/box_plot.py)"""
    print("\n[Visualization] Box-plot function is not yet implemented.")
    pass


def create_scatter_plot(input_path, output_path):
    """Placeholder for creating a scatter plot. (To be implemented in src/visualization/scatter_plot.py)"""
    print("\n[Visualization] Scatter Plot function is not yet implemented.")
    pass


# >>> END VISUALIZATION IMPORTS <<<


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

    # Step 1: Fetch Product IDs
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
    It includes a final step to MERGE the two cleaned datasets.
    """
    df_product = pd.DataFrame()
    df_comment = pd.DataFrame()

    # Define common file paths
    input_product_file = 'data/crawled_data_sach.csv'
    output_product_file = 'data/cleaned_product_sach.csv'
    input_comment_file = 'data/comments_data_sach.csv'
    output_comment_file = 'data/cleaned_comments_sach.csv'
    output_merged_file = 'data/merged_tiki_data.csv'

    # 1. Clean Product Details
    if os.path.exists(input_product_file):
        print(f"\n--- Starting cleaning for product details from {input_product_file} ---")
        df_raw = pd.read_csv(input_product_file)
        df_product = clean_product_data(df_raw)

        if not df_product.empty:
            df_product.to_csv(output_product_file, index=False)
            print(f"✅ Saved {len(df_product)} cleaned data rows to: {output_product_file}")
        else:
            print(f"⚠️ Skipping saving cleaned product file: DataFrame is empty (0 rows).")

    # 2. Clean Product Comments
    if os.path.exists(input_comment_file):
        print(f"\n--- Starting cleaning for product comments from {input_comment_file} ---")
        df_raw = pd.read_csv(input_comment_file)
        df_comment = clean_comments_data(df_raw)

        if not df_comment.empty:
            df_comment.to_csv(output_comment_file, index=False)
            print(f"✅ Saved {len(df_comment)} cleaned data rows to: {output_comment_file}")

    # 3. MERGE DATASETS (If both clean files are available)
    if not df_product.empty and not df_comment.empty:
        # Load the saved clean files (or use in-memory DFs if performance is critical)
        # Using the in-memory DFs here for simplicity and reduced I/O

        df_merged = merge_product_and_comment_data(df_product, df_comment)

        if not df_merged.empty:
            df_merged.to_csv(output_merged_file, index=False)
            print(f"✅ MERGE SUCCESSFUL. Saved {len(df_merged)} rows to: {output_merged_file}")
        else:
            print("⚠️ Merge resulted in an empty DataFrame. Check the data structure and keys.")
    else:
        print("\n⚠️ Cannot perform merge: One or both cleaned files are empty/missing.")


def run_visualization_plots():
    """
    Displays the Visualization submenu and handles user plot selection.
    """
    # Define input paths for Visualization
    INPUT_PRODUCT_PATH = 'data/cleaned_product_sach.csv'
    INPUT_COMMENT_PATH = 'data/cleaned_comments_sach.csv'
    INPUT_MERGED_PATH = 'data/merged_tiki_data.csv'

    # Check for required data files
    if not os.path.exists(INPUT_PRODUCT_PATH) or not os.path.exists(INPUT_COMMENT_PATH):
        print(f"\n⚠️ Error: Missing required cleaned data files. Please run Data Cleaning (Option 2) first.")
        return

    # Prioritize merged file for general plots, fallback to product file
    input_general_path = INPUT_MERGED_PATH if os.path.exists(INPUT_MERGED_PATH) else INPUT_PRODUCT_PATH

    # Ensure at least the fallback path exists for general plots
    if not os.path.exists(input_general_path):
        print(f"\n⚠️ Error: The necessary general input file ({input_general_path}) does not exist.")
        return

    while True:
        # >>> VISUALIZATION SUBMENU <<<
        print("\n----------------------------------------------")
        print("📊 SELECT VISUALIZATION PLOT 📊")
        print("----------------------------------------------")
        print("3.1. Line-Bar: Brand Stats (Count & Avg Rating)")
        print("3.1.1. Line-Bar: Rating Trend (Avg Rating by Month)")
        print("3.2. Box-plot (Distribution & Outliers)")
        print("3.3. Scatter Plot (Variable Relationships)")
        print("3.4. 🔙 Back to Main Menu")
        print("----------------------------------------------")
        # >>> END VISUALIZATION SUBMENU <<<

        vis_choice = input("Please select plot type (e.g., 3.1): ").strip()

        if vis_choice=='3.1':
            print("Creating Line-Bar Brand Stats Plot...")
            create_line_bar_plot(
                input_path=input_general_path,
                output_path='reports/linebar_brand_stats.png'
            )
            print("✅ Line-Bar Brand Stats Plot completed.")

        elif vis_choice=='3.1.1':
            print("Creating Line-Bar Rating Trend Plot...")
            create_line_bar_time_series_plot(
                input_path=INPUT_COMMENT_PATH,  # Uses COMMENT data only
                output_path='reports/linebar_rating_time_series.png'
            )
            print("✅ Line-Bar Rating Trend Plot completed.")

        elif vis_choice=='3.2':
            print("Creating Box-plot...")
            create_box_plot(input_path=input_general_path, output_path='reports/box_plot.png')

        elif vis_choice=='3.3':
            print("Creating Scatter Plot...")
            create_scatter_plot(input_path=input_general_path, output_path='reports/scatter_plot.png')

        elif vis_choice=='3.4':
            break
        else:
            print("Invalid choice. Please re-enter (e.g., 3.1 or 3.4).")


def main_menu():
    """
    Displays the main menu and handles user selection for the entire data workflow.
    It orchestrates the setup, ingestion, cleaning, and visualization stages.
    """

    setup_environment()  # Ensure directories exist

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
            run_data_cleaning()
        elif choice=='3':
            run_visualization_plots()
        elif choice=='4':
            print("Goodbye! See you again.")
            sys.exit(0)
        else:
            print("Invalid choice. Please re-enter a number from 1 to 4.")


if __name__=="__main__":
    main_menu()