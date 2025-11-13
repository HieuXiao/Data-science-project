# Data-science-project\main.py

# === IMPORTS ===
import os
import sys
import pandas as pd
from src.ingestion.data_fetcher import (
    fetch_product_ids,
    fetch_product_details,
    fetch_product_comments
)
from src.utils import clean_product_data, clean_comments_data, merge_product_and_comment_data
from src.visualization.line_bar_plot import (
    create_line_bar_plot,
    create_line_bar_time_series_plot
)
from src.visualization.box_plot import create_box_plot
from src.visualization.scatter_plot import create_scatter_plot

# === CONSTANTS: FILE PATHS ===
# Define all input/output file paths here for centralized management.

# --- INGESTION PATHS ---
PRODUCT_IDS_PATH = 'data/product_id_sach.csv'
RAW_PRODUCT_PATH = 'data/crawled_data_sach.csv'
RAW_COMMENTS_PATH = 'data/comments_data_sach.csv'

# --- CLEANING PATHS ---
CLEANED_PRODUCT_PATH = 'data/cleaned_product_sach.csv'
CLEANED_COMMENTS_PATH = 'data/cleaned_comments_sach.csv'
MERGED_DATA_PATH = 'data/merged_tiki_data.csv'

# --- REPORT PATHS ---
REPORT_PATH = 'reports/'


# === ENVIRONMENT SETUP FUNCTION ===
def setup_environment():
    """Checks for and creates 'data/' and 'reports/' directories if they do not exist."""
    if not os.path.exists('data'):
        os.makedirs('data')
        print("Created directory 'data/'.")
    if not os.path.exists('reports'):
        os.makedirs('reports')
        print("Created directory 'reports/'.")


# === DATA INGESTION FUNCTION ===
def run_data_ingestion():
    """Executes the data fetching pipeline: IDs, Product Details, and Comments."""
    print("\n--- Starting Data Ingestion workflow from Tiki ---")

    # 3.1. Fetch Product IDs
    df_ids = fetch_product_ids(
        category_id='8322',
        max_pages=20,
        output_path=PRODUCT_IDS_PATH
    )

    if df_ids.empty:
        print("\nProcess halted because no product IDs were collected.")
        return

    # 3.2. Fetch Product Details
    fetch_product_details(
        input_path=PRODUCT_IDS_PATH,
        output_path=RAW_PRODUCT_PATH
    )

    # 3.3. Fetch Product Comments
    fetch_product_comments(
        input_path=PRODUCT_IDS_PATH,
        max_comment_pages=5,
        output_path=RAW_COMMENTS_PATH
    )

    print("\n--- Data Ingestion workflow completed! ---")


# === DATA CLEANING AND MERGING FUNCTION ===
def run_data_cleaning():
    """
    Cleans the raw product and comment data, then merges the two cleaned datasets.
    """
    df_product = pd.DataFrame()
    df_comment = pd.DataFrame()

    # --- Clean Product Data ---
    if os.path.exists(RAW_PRODUCT_PATH):
        print(f"\n--- Starting cleaning for product details from {RAW_PRODUCT_PATH} ---")
        df_raw = pd.read_csv(RAW_PRODUCT_PATH)
        df_product = clean_product_data(df_raw)

        if not df_product.empty:
            df_product.to_csv(CLEANED_PRODUCT_PATH, index=False)
            print(f"✅ Saved {len(df_product)} cleaned data rows to: {CLEANED_PRODUCT_PATH}")
        else:
            print(f"⚠️ Skipping saving cleaned product file: DataFrame is empty (0 rows).")
    else:
        print(f"⚠️ Raw product file not found at: {RAW_PRODUCT_PATH}. Skipping cleaning.")

    # --- Clean Comments Data ---
    if os.path.exists(RAW_COMMENTS_PATH):
        print(f"\n--- Starting cleaning for product comments from {RAW_COMMENTS_PATH} ---")
        df_raw = pd.read_csv(RAW_COMMENTS_PATH)
        df_comment = clean_comments_data(df_raw)

        if not df_comment.empty:
            df_comment.to_csv(CLEANED_COMMENTS_PATH, index=False)
            print(f"✅ Saved {len(df_comment)} cleaned data rows to: {CLEANED_COMMENTS_PATH}")
        else:
            print(f"⚠️ Skipping saving cleaned comments file: DataFrame is empty (0 rows).")
    else:
        print(f"⚠️ Raw comments file not found at: {RAW_COMMENTS_PATH}. Skipping cleaning.")

    # --- Merge Data ---
    if not df_product.empty and not df_comment.empty:
        df_merged = merge_product_and_comment_data(df_product, df_comment)

        if not df_merged.empty:
            df_merged.to_csv(MERGED_DATA_PATH, index=False)
            print(f"✅ MERGE SUCCESSFUL. Saved {len(df_merged)} rows to: {MERGED_DATA_PATH}")
        else:
            print("⚠️ Merge resulted in an empty DataFrame. Check the data structure and keys.")
    else:
        print("\n⚠️ Cannot perform merge: One or both cleaned files are empty/missing.")


# === DATA VISUALIZATION FUNCTION ===
def run_visualization_plots():
    """Displays the visualization menu and creates the selected plots."""

    # Check for required cleaned data files
    if (not os.path.exists(CLEANED_PRODUCT_PATH) or
            not os.path.exists(CLEANED_COMMENTS_PATH) or
            not os.path.exists(MERGED_DATA_PATH)):
        print(f"\n⚠️ Error: Missing required cleaned or merged data files. Please run Data Cleaning (Option 2) first.")
        return

    while True:
        print("\n----------------------------------------------")
        print(" SELECT VISUALIZATION PLOT ")
        print("----------------------------------------------")
        print("3.1. Line-Bar: Rating Trend (Avg Rating by Month)")
        print("3.2. Box-plot: Rating Distribution by Brand (Top 10)")
        print("3.3. Scatter-plot: Review Length vs. Rating (P3)")
        print("3.4. 🔙 Back to Main Menu")
        print("----------------------------------------------")

        vis_choice = input("Please select plot type (e.g., 3.1): ").strip()

        if vis_choice=='3.1':
            print("Creating Line-Bar Rating Trend Plot...")
            create_line_bar_time_series_plot(
                input_path=MERGED_DATA_PATH,
                output_path=os.path.join(REPORT_PATH, 'linebar_rating_time_series.png')
            )
            print("Line-Bar Rating Trend Plot completed.")

        elif vis_choice=='3.2':
            print("Creating Box Plot (Rating Distribution by Brand)...")
            create_box_plot(
                input_path=MERGED_DATA_PATH,
                output_path=os.path.join(REPORT_PATH, 'boxplot_rating_by_brand.png')
            )
            print("Box Plot completed.")

        elif vis_choice=='3.3':
            print("Creating Scatter Plot (Review Length vs. Rating)...")
            create_scatter_plot(
                input_path=MERGED_DATA_PATH,
                output_path=os.path.join(REPORT_PATH, 'scatterplot_review_length_vs_rating.png')
            )
            print("Scatter Plot completed.")

        elif vis_choice=='3.4':
            break
        else:
            print("Invalid choice. Please re-enter (e.g., 3.1 or 3.4).")


# === MAIN MENU FUNCTION ===
def main_menu():
    """Displays and handles the main project functionality choices."""
    setup_environment()

    while True:
        print("\n==============================================")
        print(" TIKI DATA SCIENCE PROJECT MENU ")
        print("==============================================")
        print("1. Data Ingestion (Crawl data from Tiki API)")
        print("2. Data Cleaning (Clean crawled data)")
        print("3. Data Visualization (Visualize cleaned data)")
        print("0. Exit")
        print("==============================================")

        choice = input("Please select a function (Enter number): ").strip()

        if choice=='1':
            run_data_ingestion()
        elif choice=='2':
            run_data_cleaning()
        elif choice=='3':
            run_visualization_plots()
        elif choice=='0':
            print("Goodbye! See you again.")
            sys.exit(0)
        else:
            print("Invalid choice. Please re-enter a number from 1 to 3.")


# === PROGRAM ENTRY POINT ===
if __name__=="__main__":
    main_menu()