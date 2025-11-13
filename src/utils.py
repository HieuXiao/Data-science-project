import pandas as pd
import numpy as np


def clean_product_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Performs basic data cleaning on the product details DataFrame.
    ...
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
    remaining_numeric_cols = df_cleaned.select_dtypes(include=np.number).columns.tolist()

    if 'id' in remaining_numeric_cols: remaining_numeric_cols.remove('id')

    df_cleaned[remaining_numeric_cols] = df_cleaned[remaining_numeric_cols].fillna(0)
    print("  - Filled missing values in remaining numeric columns with 0.")

    # 4. Data Type Conversion and Name Handling
    df_cleaned['id'] = df_cleaned['id'].astype('str')

    if 'brand_id' in df_cleaned.columns:
        df_cleaned['brand_id'] = df_cleaned['brand_id'].astype('str').fillna('unknown')

    if 'product_name' in df_cleaned.columns:
        df_cleaned['product_name'] = df_cleaned['product_name'].fillna('UNKNOWN_PRODUCT_' + df_cleaned[
            'id'].astype(str)).astype('str')

    print("[Cleaning] Product data cleaning completed.")
    return df_cleaned


def clean_comments_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Performs basic data cleaning on the product comments DataFrame.
    ĐÃ SỬA: Chuyển đổi created_at và purchased_at sử dụng unit='s' (giây) thay vì 'ms' (mili giây).
    """
    print("\n[Cleaning] Starting comments data cleaning...")
    df_cleaned = df.copy()

    required_cols_base = ['id', 'rating']
    required_cols = [col for col in required_cols_base if col in df_cleaned.columns]

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
            # >>> ĐIỀU CHỈNH QUAN TRỌNG: unit='s' (giây) <<<
            df_cleaned[col] = pd.to_datetime(df_cleaned[col], unit='s', errors='coerce')

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
    ...
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
    merged_df.rename(columns={'id_comment': 'comment_id'}, inplace=True)

    # Drop rows where the merge failed (comment has product_id but product info is missing)
    merged_df.dropna(subset=['product_name'], inplace=True)

    print(f"[Merge] Completed. Merged DataFrame size: {len(merged_df)} rows.")
    return merged_df