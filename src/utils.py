# Data-science-project\src\utils.py

# === IMPORTS ===
import pandas as pd
import numpy as np


# === PRODUCT DATA CLEANING FUNCTION ===
def clean_product_data(df: pd.DataFrame):
    """
    Cleans the product details DataFrame: drops missing IDs, removes unnecessary
    columns, fills missing numeric values, and standardizes data types.
    """
    print("\n[Cleaning] Starting product data cleaning...")
    df_cleaned = df.copy()

    # 1. Handle missing critical IDs
    df_cleaned.dropna(subset=['id'], inplace=True)
    initial_rows = len(df)
    current_rows = len(df_cleaned)
    print(f"  - Dropped {initial_rows - current_rows} rows (missing ID). {current_rows} rows remaining.")

    # 2. Define and drop unnecessary columns
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

    # 3. Fill missing values in numeric columns (except 'id')
    remaining_numeric_cols = df_cleaned.select_dtypes(include=np.number).columns.tolist()

    if 'id' in remaining_numeric_cols: remaining_numeric_cols.remove('id')

    df_cleaned[remaining_numeric_cols] = df_cleaned[remaining_numeric_cols].fillna(0)
    print("  - Filled missing values in remaining numeric columns with 0.")

    # 4. Type casting and handling missing string values
    df_cleaned['id'] = df_cleaned['id'].astype('str')

    if 'brand_id' in df_cleaned.columns:
        df_cleaned['brand_id'] = df_cleaned['brand_id'].astype('str').fillna('unknown')

    if 'product_name' in df_cleaned.columns:
        # Fill missing product names with a unique identifier based on ID
        df_cleaned['product_name'] = df_cleaned['product_name'].fillna('UNKNOWN_PRODUCT_' + df_cleaned[
            'id'].astype(str)).astype('str')

    print("[Cleaning] Product data cleaning completed.")
    return df_cleaned


# === COMMENTS DATA CLEANING FUNCTION ===
def clean_comments_data(df: pd.DataFrame):
    """
    Cleans the comments DataFrame: drops rows missing critical fields (id, rating, product_id),
    converts date columns, standardizes rating type, and fills missing strings.
    """
    print("\n[Cleaning] Starting comments data cleaning...")
    df_cleaned = df.copy()

    # 1. Identify required columns for cleaning
    required_cols_base = ['id', 'rating']
    required_cols = [col for col in required_cols_base if col in df_cleaned.columns]

    if 'product_id' in df_cleaned.columns:
        required_cols.append('product_id')
    else:
        print("  - Warning: 'product_id' column is missing. Data will lack product linkage.")

    # 2. Drop rows missing critical required data
    df_cleaned.dropna(subset=required_cols, inplace=True)

    initial_rows = len(df)
    current_rows = len(df_cleaned)
    print(f"  - Dropped {initial_rows - current_rows} rows missing basic data. {current_rows} rows remaining.")

    # 3. Convert timestamp columns to datetime objects
    date_cols = ['created_at', 'purchased_at']
    for col in date_cols:
        if col in df_cleaned.columns:
            # Convert Unix timestamp (seconds) to datetime
            df_cleaned[col] = pd.to_datetime(df_cleaned[col], unit='s', errors='coerce')

    # 4. Standardize 'rating' column
    df_cleaned['rating'] = pd.to_numeric(df_cleaned['rating'], errors='coerce').fillna(0).astype(int)

    # 5. Fill missing string columns with empty string
    str_cols_to_fill = ['title', 'content', 'customer_name']
    for col in str_cols_to_fill:
        if col in df_cleaned.columns:
            df_cleaned[col] = df_cleaned[col].fillna('')

    print("[Cleaning] Comments data cleaning completed.")
    return df_cleaned


# === DATA MERGING FUNCTION ===
def merge_product_and_comment_data(product_df: pd.DataFrame, comment_df: pd.DataFrame):
    """
    Merges the cleaned product and comment DataFrames based on product ID.
    Returns the merged DataFrame (left join on product_id).
    """
    print("\n[Merge] Starting product and comment data merge...")

    # 1. Ensure keys are string type for reliable merging
    product_df['id'] = product_df['id'].astype(str)

    if 'product_id' not in comment_df.columns:
        print("  - Warning: 'product_id' column missing in comments data. Cannot merge.")
        return pd.DataFrame()

    comment_df['product_id'] = comment_df['product_id'].astype(str)

    # 2. Perform the merge
    merged_df = pd.merge(
        comment_df,
        product_df,
        left_on='product_id',
        right_on='id',
        how='left',  # Keep all comments, linking to available product info
        suffixes=('_comment', '_product')
    )

    # 3. Finalize merged structure
    merged_df.drop(columns=['id_product'], inplace=True)
    merged_df.rename(columns={'id_comment': 'comment_id', 'product_name': 'product_name'}, inplace=True)

    # Drop rows where the merge failed (i.e., comment belongs to an unknown product)
    merged_df.dropna(subset=['product_name'], inplace=True)

    print(f"[Merge] Completed. Merged DataFrame size: {len(merged_df)} rows.")
    return merged_df
