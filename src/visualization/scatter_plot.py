# src/visualization/scatter_plot.py

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import numpy as np


def create_scatter_plot(input_path, output_path):
    """
    Creates a Scatter Plot to analyze the relationship between Review Length
    (character count) and the Rating Score.

    TASK (P3):
    1. Create new column: 'review_length' (character count of 'content').
    2. Plot: X = Review Length, Y = Rating.
    3. Calculate Correlation and provide analysis.

    Args:
        input_path (str): Path to the merged CSV file.
        output_path (str): Path to save the Scatter Plot image.
    """
    print(f"\n[Visualization] Starting Scatter Plot (Review Length vs. Rating) from: {input_path}")

    if not os.path.exists(input_path):
        print(f"⚠️ ERROR: File not found at path: {input_path}")
        return

    try:
        # 1. Load Data and Preprocessing
        df = pd.read_csv(input_path)

        # Fill NaN content with empty string and calculate length (character count)
        df['content'] = df['content'].fillna('')
        df['review_length'] = df['content'].apply(len)

        # Filter for valid reviews (non-zero length and valid rating)
        df_filtered = df[(df['review_length'] > 0) & (df['rating'] >= 1) & (df['rating'] <= 5)].copy()

        if df_filtered.empty:
            print("⚠️ WARNING: No reviews with content found for analysis.")
            return

        # 2. Create Scatter Plot with Regression Line
        plt.figure(figsize=(10, 6))

        # Use regplot for scatter and linear regression line.
        # Jitter (y_jitter=0.15) is added to the discrete Y-axis (Rating 1-5)
        # to show the density of overlapping points more clearly.
        sns.regplot(
            x='review_length',
            y='rating',
            data=df_filtered,
            x_jitter=0,
            y_jitter=0.15,
            scatter_kws={'alpha': 0.05, 's': 20, 'color': '#1f77b4'},
            line_kws={'color': '#d62728', 'lw': 3}
        )

        # 3. Calculate Correlation
        correlation = df_filtered['review_length'].corr(df_filtered['rating'])

        # 4. Calculate Average Length per Rating for detailed analysis
        avg_length_by_rating = df_filtered.groupby('rating')['review_length'].mean().sort_index()

        plt.title(f'Review Length vs. Rating Score (Correlation: {correlation:.4f})', fontsize=16, fontweight='bold')
        plt.xlabel('Review Length (Character Count)', fontsize=12, fontweight='bold')
        plt.ylabel('Rating Score (1-5 Stars)', fontsize=12, fontweight='bold')
        plt.yticks(ticks=[1, 2, 3, 4, 5])
        plt.ylim(0.5, 5.5)
        plt.grid(axis='y', linestyle='--', alpha=0.6)

        plt.tight_layout()
        plt.savefig(output_path, dpi=300)
        plt.close()

        print(f"✅ Scatter Plot successfully saved to: {output_path}")

        # Output analysis data
        print("\n--- Average Review Length by Rating Score ---")
        print(avg_length_by_rating.to_markdown())

    except Exception as e:
        print(f"❌ ERROR during Scatter Plot creation: {e}")