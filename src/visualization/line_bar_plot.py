# src/visualization/line_bar_plot.py

# ==============================
# 1. IMPORT NECESSARY LIBRARIES
# ==============================
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import matplotlib.dates as mdates


# =======================================================
# FUNCTION 1: BRAND STATS (Line-Bar Dual Axis)
# Purpose: Compare Product Count and Average Rating by Top Brand
# =======================================================
def create_line_bar_plot(input_path='data/merged_tiki_data.csv', output_path='reports/linebar_brand_stats.png'):
    """
    Creates a dual axis Line-Bar chart showing the number of products and
    the average rating for the Top 10 Brands.

    Args:
        input_path (str): Path to the merged data file (preferred).
        output_path (str): Path to save the output image file.
    """
    print(f"\n[Visualization] Starting Line-Bar Plot (Brand Stats) from file: {input_path}")

    if not os.path.exists(input_path):
        print(f"⚠️ Error: Input file '{input_path}' not found. Skipping plot creation.")
        return

    try:
        df = pd.read_csv(input_path, encoding='utf-8')
    except Exception as e:
        print(f"⚠️ Error reading CSV file: {e}.")
        return

    # --- Data Validation ---
    required_cols_merged = ['brand_name', 'rating', 'id', 'comment_id']
    required_cols_product = ['brand_name', 'review_count', 'id']

    # Xác định chế độ chạy (Ưu tiên Merged Data)
    is_merged = all(col in df.columns for col in required_cols_merged)

    if is_merged:
        # MERGED MODE: Dùng dữ liệu MERGED
        brand_stats = df.groupby('brand_name').agg(
            # Đếm số lượng sản phẩm DUY NHẤT có bình luận
            product_count=('id', 'nunique'),
            # Average rating của tất cả các bình luận
            avg_rating=('rating', 'mean')
        ).round(2)
        count_label = 'Unique Products with Reviews'
        line_label = 'Average Rating (Star)'
    elif all(col in df.columns for col in required_cols_product):
        # PRODUCT ONLY MODE: Chạy trên cleaned_product_sach.csv (dự phòng)
        brand_stats = df.groupby('brand_name').agg(
            product_count=('id', 'count'),
            avg_rating=('review_count', 'mean')  # Dùng review_count TB làm chỉ số đường
        ).round(2)
        count_label = 'Total Product Listings'
        line_label = 'Average Review Count'
    else:
        print("⚠️ Error: Data is missing required columns. Skipping plot creation.")
        return

    # --- Data Processing: Filter and Sort ---
    # Lọc Top 10 Brands có số lượng sản phẩm/reviews lớn nhất
    top_brands = brand_stats.sort_values(by='product_count', ascending=False).head(10)
    top_brands = top_brands.sort_values(by='avg_rating', ascending=True)  # Sắp xếp cho đường line mượt hơn

    if top_brands.empty:
        print("⚠️ Error: Insufficient Brand data for visualization.")
        return

    # ==================================================
    # 4. CREATE FIGURE AND DUAL AXIS PLOT
    # ==================================================
    fig, ax1 = plt.subplots(figsize=(14, 7))

    x = np.arange(len(top_brands))
    width = 0.6

    ax2 = ax1.twinx()  # Secondary Y-axis

    # --- Plot 1 (Primary Y-axis - Count) ---
    ax1.bar(x, top_brands['product_count'], width,
        label=count_label, color='#2E86AB', alpha=0.8)

    # --- Plot 2 (Secondary Y-axis - Avg Rating/Review Count) ---
    ax2.plot(x, top_brands['avg_rating'],
        marker='o', linewidth=3, markersize=8,
        color='#C73E1D', label=line_label)

    # ==========================================
    # 5. SET LABELS, TITLES, AND STYLING
    # ==========================================

    ax1.set_xticks(x)
    ax1.set_xticklabels(top_brands.index, rotation=30, ha='right', fontsize=10)
    ax1.set_xlabel('Brand (Top 10)', fontsize=12, fontweight='bold')

    ax1.set_ylabel(count_label, fontsize=12, fontweight='bold', color='#2E86AB')
    ax1.tick_params(axis='y', labelcolor='#2E86AB')

    ax2.set_ylabel(line_label, fontsize=12, fontweight='bold', color='#C73E1D')
    ax2.tick_params(axis='y', labelcolor='#C73E1D')

    # Đặt giới hạn trục Y cho Rating nếu là Merged data
    if is_merged:
        ax2.set_ylim(0, 5.0)

    plt.title(f'Top 10 Brand Analysis: {count_label} vs. {line_label}', fontsize=16, fontweight='bold')
    ax1.grid(True, alpha=0.3, linestyle='--', axis='y')

    # Combine legends from both axes
    lines, labels = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines + lines2, labels + labels2, loc='upper left')

    # ===================================
    # 6. SAVE AND CLEAN UP
    # ===================================
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✅ Line-Bar Plot (Brand Stats) created and saved at: {output_path}")
    plt.close(fig)


# =======================================================
# FUNCTION 2: TIME SERIES TREND ANALYSIS
# Purpose: Analyze Average Rating and Review Count Trend by Month
# =======================================================
def create_line_bar_time_series_plot(input_path='data/cleaned_comments_sach.csv', output_path='reports/linebar_rating_time_series.png'):
    """
    Creates a dual axis Line-Bar chart showing the trend of Average Rating and
    Total Review Count over time (Month-Year).

    Args:
        input_path (str): Path to the cleaned COMMENTS data file.
        output_path (str): Path to save the output image file.
    """
    print(f"\n[Visualization] Starting Line-Bar Time Series Plot from file: {input_path}")

    if not os.path.exists(input_path):
        print(f"⚠️ Error: Input file '{input_path}' not found. Skipping plot creation.")
        return

    try:
        df = pd.read_csv(input_path, encoding='utf-8')
    except Exception as e:
        print(f"⚠️ Error reading CSV file: {e}.")
        return

    # --- Data Validation ---
    if df.empty or 'created_at' not in df.columns or 'rating' not in df.columns:
        print("⚠️ Error: Data is missing required columns ('created_at', 'rating'). Skipping plot creation.")
        return

    # --- 1. Process Time Column ---
    df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce')
    df.dropna(subset=['created_at'], inplace=True)

    # --- 2. Aggregate Data by Month-Year ---
    df.set_index('created_at', inplace=True)

    # Resample by Month ('M')
    time_series_stats = df.resample('M').agg(
        avg_rating=('rating', 'mean'),  # Average Rating
        review_count=('id', 'count')  # Total Review Count (using comment ID count)
    ).round(2).dropna()

    if time_series_stats.empty:
        print("⚠️ Error: Insufficient monthly data for time series visualization.")
        return

    # ==================================================
    # 3. CREATE FIGURE AND DUAL AXIS PLOT
    # ==================================================
    fig, ax1 = plt.subplots(figsize=(14, 7))

    ax2 = ax1.twinx()  # Secondary Y-axis for Review Count

    # --- Plot 1 (Primary Y-axis - Avg Rating) ---
    ax1.plot(time_series_stats.index, time_series_stats['avg_rating'],
        marker='o', linewidth=2.5, markersize=8,
        color='#3498DB', label='Average Rating (Star)')

    # --- Plot 2 (Secondary Y-axis - Review Count) ---
    ax2.bar(time_series_stats.index, time_series_stats['review_count'],
        width=20,  # Width set for monthly intervals
        color='#27AE60', alpha=0.6, label='Total Review Count')

    # ==========================================
    # 4. SET LABELS, TITLES, AND STYLING
    # ==========================================

    # X-axis (Time)
    ax1.set_xlabel('Month-Year', fontsize=12, fontweight='bold')
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    ax1.tick_params(axis='x', rotation=45)

    # Primary Y-axis (Rating)
    ax1.set_ylabel('Average Rating', fontsize=12, fontweight='bold', color='#3498DB')
    ax1.tick_params(axis='y', labelcolor='#3498DB')
    ax1.set_ylim(time_series_stats['avg_rating'].min() - 0.1, 5.0)

    # Secondary Y-axis (Count)
    ax2.set_ylabel('Total Review Count', fontsize=12, fontweight='bold', color='#27AE60')
    ax2.tick_params(axis='y', labelcolor='#27AE60')

    # Title and Grid
    plt.title('Customer Satisfaction Trend (Avg Rating and Review Count) by Month', fontsize=16, fontweight='bold')
    ax1.grid(True, alpha=0.3, linestyle='--')

    # Combine legends
    lines, labels = ax1.get_legend_handles_labels()
    bars, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines + [bars[0]], labels + labels2, loc='upper left')

    # ===================================
    # 5. SAVE AND CLEAN UP
    # ===================================
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✅ Line-Bar Time Series Plot created and saved at: {output_path}")
    plt.close(fig)