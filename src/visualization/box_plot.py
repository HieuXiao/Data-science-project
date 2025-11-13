# src/visualization/box_plot.py

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os


def create_box_plot(input_path, output_path, top_n=10):
    """
    Creates a Box Plot to analyze the dispersion (distribution and outliers) of 
    rating scores across the Top N brands with the highest review count.

    Args:
        input_path (str): Path to the merged CSV file.
        output_path (str): Path to save the Box Plot image.
        top_n (int): Number of top brands to analyze.
    """
    print(f"\n[Visualization] Starting Box Plot creation for Top {top_n} Brands from: {input_path}")

    if not os.path.exists(input_path):
        print(f"⚠️ ERROR: File not found at path: {input_path}")
        return

    try:
        # 1. Load Data and initial filtering
        df = pd.read_csv(input_path)

        # Ensure necessary columns are present and clean
        df.dropna(subset=['brand_name', 'rating'], inplace=True)
        df['brand_name'] = df['brand_name'].astype(str).str.strip()

        # Convert rating to numeric, coerce errors to NaN, then convert to integer after dropping NaNs
        df['rating'] = pd.to_numeric(df['rating'], errors='coerce')
        df.dropna(subset=['rating'], inplace=True)
        df['rating'] = df['rating'].astype(int)  # Rating should be discrete 1-5 integer

        # 2. Identify Top N Brands by Review Count
        brand_counts = df.groupby('brand_name')['comment_id'].size().sort_values(ascending=False)
        top_brands = brand_counts.head(top_n).index.tolist()

        # Filter the DataFrame to include only the Top N Brands
        df_filtered = df[df['brand_name'].isin(top_brands)].copy()

        if df_filtered.empty:
            print("⚠️ WARNING: Insufficient data for Top Brands to create the plot.")
            return

        # 3. Create Box Plot
        plt.figure(figsize=(14, 8))

        # Determine order based on mean rating (for better comparison on the plot)
        brand_order = df_filtered.groupby('brand_name')['rating'].mean().sort_values(ascending=False).index.tolist()

        sns.boxplot(
            x='brand_name',
            y='rating',
            data=df_filtered,
            order=brand_order,
            palette='Set2'
        )

        plt.title(f'Rating Distribution (Box Plot) for Top {top_n} Brands', fontsize=16, fontweight='bold')
        plt.xlabel('Brand (Ordered by Avg Rating)', fontsize=12, fontweight='bold')
        plt.ylabel('Rating Score (1-5 Stars)', fontsize=12, fontweight='bold')
        plt.yticks(ticks=[1, 2, 3, 4, 5])
        plt.ylim(0.5, 5.5)  # Set Y-limit to cover 1 to 5 stars cleanly
        plt.xticks(rotation=45, ha='right')
        plt.grid(axis='y', linestyle='--', alpha=0.6)

        # 4. Save Plot
        plt.tight_layout()
        plt.savefig(output_path, dpi=300)
        plt.close()

        print(f"✅ Box Plot successfully saved to: {output_path}")

        # 5. Print Statistical Analysis Summary
        analysis_data = df_filtered.groupby('brand_name')['rating'].agg(['mean', 'median', 'min', 'max',
                                                                         'std']).sort_values(by='mean', ascending=False)
        analysis_data['IQR'] = df_filtered.groupby('brand_name')[
            'rating'].apply(lambda x: x.quantile(0.75) - x.quantile(0.25))

        print("\n--- Rating Dispersion Statistics by Brand (Top 10) ---")
        print(analysis_data.to_markdown())

    except Exception as e:
        print(f"❌ ERROR during Box Plot creation: {e}")