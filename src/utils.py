# src/utils.py

import pandas as pd
import numpy as np


def clean_product_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Performs basic data cleaning on the product details DataFrame.

    Cleaning steps include:
    1. Dropping rows with missing essential identifiers (ID).
    2. Dropping redundant or unused columns (e.g., price_usd, is_visible).
    3. Filling missing values (NaN) in numeric columns with 0.
    4. Converting relevant columns to appropriate data types.
    5. Handling the missing 'product_name' by substituting with a placeholder.

    Args:
        df (pd.DataFrame): The raw DataFrame containing product details.

    Returns:
        pd.DataFrame: The cleaned DataFrame.
    """
    print("\n[Cleaning] Starting product data cleaning...")
    df_cleaned = df.copy()

    # 1. Drop invalid records (Only drop rows missing 'id' - the primary key)
    df_cleaned.dropna(subset=['id'], inplace=True)
    initial_rows = len(df)
    current_rows = len(df_cleaned)
    print(f"  - Dropped {initial_rows - current_rows} rows (missing ID). {current_rows} rows remaining.")

    # 2. Drop unnecessary columns
    cols_to_drop = [
        'price_usd',
        'order_count',
        'is_visible',
        'stock_item_qty',
        'stock_item_max_sale_qty'
    ]
    existing_cols_to_drop = [col for col in cols_to_drop if col in df_cleaned.columns]

    if existing_cols_to_drop:
        df_cleaned.drop(columns=existing_cols_to_drop, inplace=True)
        print(f"  - Dropped unnecessary columns: {existing_cols_to_drop}")

    # 3. Handle Missing Values (NaN) - Fill with 0 (Only for remaining numeric cols)
    # Note: We must redefine numeric cols after dropping unnecessary ones
    remaining_numeric_cols = df_cleaned.select_dtypes(include=np.number).columns.tolist()

    # Exclude ID columns if they are still numeric
    if 'id' in remaining_numeric_cols: remaining_numeric_cols.remove('id')

    # Fill remaining numeric NaNs with 0
    df_cleaned[remaining_numeric_cols] = df_cleaned[remaining_numeric_cols].fillna(0)
    print("  - Filled missing values in remaining numeric columns with 0.")

    # 4. Data Type Conversion and Name Handling
    df_cleaned['id'] = df_cleaned['id'].astype('str')

    if 'brand_id' in df_cleaned.columns:
        df_cleaned['brand_id'] = df_cleaned['brand_id'].astype('str').fillna('unknown')

    # FIX: Handle entirely missing product_name by using ID as a placeholder
    if 'product_name' in df_cleaned.columns:
        df_cleaned['product_name'] = df_cleaned['product_name'].fillna('UNKNOWN_PRODUCT_' + df_cleaned[
            'id'].astype(str)).astype('str')

    print("[Cleaning] Product data cleaning completed.")
    return df_cleaned


def clean_comments_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Performs basic data cleaning on the product comments DataFrame.

    Cleaning steps include:
    1. Dropping rows with missing essential columns (ID, Rating).
    2. Converting date columns (timestamps) to datetime format.
    3. Ensuring rating is a clean integer (filling NaN with 0).
    4. Filling missing values in string columns with an empty string.

    Args:
        df (pd.DataFrame): The raw DataFrame containing product comments.

    Returns:
        pd.DataFrame: The cleaned DataFrame.
    """
    print("\n[Cleaning] Starting comments data cleaning...")
    df_cleaned = df.copy()

    # Identify existing essential columns (ID and Rating are minimum requirements)
    required_cols_base = ['id', 'rating']
    required_cols = [col for col in required_cols_base if col in df_cleaned.columns]

    # Handle 'product_id' column for linkage (if present, include in dropna subset)
    if 'product_id' in df_cleaned.columns:
        required_cols.append('product_id')
    else:
        print("  - Warning: 'product_id' column is missing. Data will lack product linkage.")

    # 1. Drop records with missing basic information
    df_cleaned.dropna(subset=required_cols, inplace=True)

    initial_rows = len(df)
    current_rows = len(df_cleaned)
    print(f"  - Dropped {initial_rows - current_rows} rows missing basic data. {current_rows} rows remaining.")

    # 2. Data Type Conversion (Timestamps and Rating)
    date_cols = ['created_at', 'purchased_at']
    for col in date_cols:
        if col in df_cleaned.columns:
            # Convert Unix milliseconds to datetime objects
            df_cleaned[col] = pd.to_datetime(df_cleaned[col], unit='ms', errors='coerce')

    # Convert 'rating' to integer (filling NaN with 0 for safety)
    df_cleaned['rating'] = pd.to_numeric(df_cleaned['rating'], errors='coerce').fillna(0).astype(int)

    # Fill missing values in string columns with an empty string
    str_cols_to_fill = ['title', 'content', 'customer_name']
    for col in str_cols_to_fill:
        if col in df_cleaned.columns:
            df_cleaned[col] = df_cleaned[col].fillna('')

    print("[Cleaning] Comments data cleaning completed.")
    return df_cleaned


def merge_product_and_comment_data(product_df: pd.DataFrame, comment_df: pd.DataFrame) -> pd.DataFrame:
    """
    Merges cleaned product details and comments data based on Product ID.

    The resulting DataFrame links comment attributes (e.g., rating, date)
    to product attributes (e.g., price, brand_name).

    Args:
        product_df (pd.DataFrame): Cleaned product details DataFrame.
        comment_df (pd.DataFrame): Cleaned comments DataFrame.

    Returns:
        pd.DataFrame: Merged DataFrame containing product and comment attributes.
    """
    print("\n[Merge] Starting product and comment data merge...")

    # Ensure keys are string type for safe merging
    product_df['id'] = product_df['id'].astype(str)

    # Check for the product_id column in the comments data
    if 'product_id' not in comment_df.columns:
        print("  - Warning: 'product_id' column missing in comments data. Cannot merge.")
        return pd.DataFrame()

    comment_df['product_id'] = comment_df['product_id'].astype(str)

    # Perform LEFT MERGE: Keep all comments and try to match product info
    merged_df = pd.merge(
        comment_df,
        product_df,
        left_on='product_id',
        right_on='id',
        how='left',
        suffixes=('_comment', '_product')
    )

    # Rename and drop columns for clarity
    merged_df.drop(columns=['id_product'], inplace=True)
    merged_df.rename(columns={'id_comment': 'comment_id', 'product_name': 'product_name'}, inplace=True)

    # Drop rows where the merge failed (comment has product_id but product info is missing)
    merged_df.dropna(subset=['product_name'], inplace=True)

    print(f"[Merge] Completed. Merged DataFrame size: {len(merged_df)} rows.")
    return merged_df