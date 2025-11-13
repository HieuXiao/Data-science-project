# src/utils.py

import pandas as pd
import numpy as np


def clean_product_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Performs basic data cleaning on the product details DataFrame.

    Cleaning steps include:
    1. Dropping rows with missing essential identifiers (ID, Name).
    2. Filling missing values (NaN) in numeric columns with 0.
    3. Converting relevant columns to appropriate data types (numeric, string).

    Args:
        df (pd.DataFrame): The raw DataFrame containing product details.

    Returns:
        pd.DataFrame: The cleaned DataFrame.
    """
    print("\n[Cleaning] Starting product data cleaning...")
    df_cleaned = df.copy()

    # 1. Drop invalid records (Missing product ID or name)
    # This is the most crucial step to ensure data traceability
    df_cleaned.dropna(subset=['id', 'product_name'], inplace=True)
    initial_rows = len(df)
    current_rows = len(df_cleaned)
    print(f"  - Dropped {initial_rows - current_rows} rows (missing ID/Name). {current_rows} rows remaining.")

    # 2. Handle Missing Values (NaN)

    # List of numeric columns that need NaN treatment (fill with 0)
    numeric_cols_to_fill = [
        'price', 'list_price', 'discount', 'discount_rate',
        'review_count', 'order_count', 'stock_item_qty', 'stock_item_max_sale_qty'
    ]

    # Fill missing values (NaN) with 0 before type conversion
    df_cleaned[numeric_cols_to_fill] = df_cleaned[numeric_cols_to_fill].fillna(0)
    print("  - Filled missing values in numeric columns with 0.")

    # 3. Data Type Conversion

    # Convert numeric columns to float (or int if applicable)
    for col in numeric_cols_to_fill:
        try:
            # Use pd.to_numeric with errors='coerce' to turn non-numeric values into NaN
            # Although we filled NaN with 0, this step ensures robustness
            df_cleaned[col] = pd.to_numeric(df_cleaned[col], errors='coerce')
        except Exception as e:
            print(f"  - Warning: Could not convert column '{col}' to numeric: {e}")

    # Handle ID columns
    df_cleaned['id'] = df_cleaned['id'].astype('str')
    if 'brand_id' in df_cleaned.columns:
        df_cleaned['brand_id'] = df_cleaned['brand_id'].astype('str').fillna('unknown')

    print("[Cleaning] Product data cleaning completed.")
    return df_cleaned


def clean_comments_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Performs basic data cleaning on the product comments DataFrame.

    Cleaning steps include:
    1. Dropping rows with missing essential columns (ID, Rating, Product ID).
    2. Converting date columns to datetime format.
    3. Ensuring rating is a clean integer (filling NaN with 0).
    4. Filling missing values in string columns with an empty string.

    Args:
        df (pd.DataFrame): The raw DataFrame containing product comments.

    Returns:
        pd.DataFrame: The cleaned DataFrame.
    """
    print("\n[Cleaning] Starting comments data cleaning...")
    df_cleaned = df.copy()

    # Identify existing essential columns
    required_cols_base = ['id', 'rating']
    required_cols = [col for col in required_cols_base if col in df_cleaned.columns]

    # Handle 'product_id' column
    if 'product_id' in df_cleaned.columns:
        required_cols.append('product_id')
    else:
        # This warning indicates that the comment data cannot be linked to the product
        print("  - Warning: 'product_id' column is missing. Data will lack product linkage.")

    # 1. Drop records with missing basic information
    df_cleaned.dropna(subset=required_cols, inplace=True)

    initial_rows = len(df)
    current_rows = len(df_cleaned)
    print(f"  - Dropped {initial_rows - current_rows} rows missing basic data. {current_rows} rows remaining.")

    # 2. Data Type Conversion (Keeping your original logic)

    # Convert date columns (assuming milliseconds timestamp)
    date_cols = ['created_at', 'purchased_at']
    for col in date_cols:
        if col in df_cleaned.columns:
            # Convert Unix milliseconds to datetime
            df_cleaned[col] = pd.to_datetime(df_cleaned[col], unit='ms', errors='coerce')

    # Convert 'rating' to integer (filling NaN with 0)
    df_cleaned['rating'] = pd.to_numeric(df_cleaned['rating'], errors='coerce').fillna(0).astype(int)

    # Fill missing values in string columns with an empty string
    str_cols_to_fill = ['title', 'content', 'customer_name']
    for col in str_cols_to_fill:
        if col in df_cleaned.columns:
            df_cleaned[col] = df_cleaned[col].fillna('')

    print("[Cleaning] Comments data cleaning completed.")
    return df_cleaned

# General utility functions can be added here later (e.g., logging, I/O helpers)