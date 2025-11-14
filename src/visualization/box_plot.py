# Data-science-project\src\visualization\box_plot.py

# === IMPORTS ===
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os


# === DATA PREPARATION FUNCTION (INTERNAL) ===
def _prepare_box_plot_data(input_path: str, top_n: int):
    """
    Reads the data, cleans and filters it to prepare a DataFrame containing
    only the Top N brands based on review count.

    Returns:
        pd.DataFrame or None: The filtered DataFrame, or None if data is insufficient.
    """
    try:
        # Read data and handle critical missing values
        data = pd.read_csv(input_path)
        data = data.dropna(subset=['brand_name', 'rating', 'comment_id'])

        # Data type casting and cleaning
        data['brand_name'] = data['brand_name'].astype(str).str.strip()
        data['rating'] = pd.to_numeric(data['rating'], errors='coerce')
        data = data.dropna(subset=['rating'])
        data['rating'] = data['rating'].astype(int)

        # Identify Top N brands
        brand_counts = data.groupby('brand_name')['comment_id'].size().sort_values(ascending=False)
        top_brands = brand_counts.head(top_n).index.tolist()

        # Filter the DataFrame
        data = data[data['brand_name'].isin(top_brands)].copy()

        if data.empty:
            print("⚠️ WARNING: Insufficient data for Top Brands to create the plot.")
            return None

        return data

    except FileNotFoundError:
        print(f"⚠️ ERROR: File not found during data preparation at: {input_path}")
        return None
    except Exception as e:
        print(f"❌ ERROR during data preparation for Box Plot: {e}")
        return None


# === BOX PLOT FUNCTION: RATING DISTRIBUTION BY TOP N BRANDS ===
def create_box_plot(input_path, output_path, top_n=10):
    """
    Creates a Box Plot to analyze the distribution of rating scores for the Top N Brands.
    """
    print(f"\n[Visualization] Starting Box Plot creation for Top {top_n} Brands from: {input_path}")

    # 1. PREPARE DATA
    # The File Not Found check is moved into the helper function,
    # but we keep the main check for better user feedback
    if not os.path.exists(input_path):
        print(f"⚠️ ERROR: File not found at path: {input_path}")
        return

    data = _prepare_box_plot_data(input_path, top_n)

    if data is None:
        return

    try:
        # Determine the order of box plots based on average rating (descending)
        brand_order = data.groupby('brand_name')['rating'].mean().sort_values(ascending=False).index.tolist()

        # 2. CONFIGURE AND DRAW BOX PLOT
        plt.figure(figsize=(10, 8))

        sns.boxplot(
            x='brand_name',
            y='rating',
            data=data,  # Use 'data' consistent with your style
            order=brand_order,
            palette='Set2'
        )

        # 3. FINALIZE, SAVE, AND PRINT RESULTS
        plt.title(f'Rating Distribution (Box Plot) for Top {top_n} Brands', fontsize=16, fontweight='bold')
        plt.xlabel('Brand (Ordered by Avg Rating)', fontsize=12, fontweight='bold')
        plt.ylabel('Rating Score (1-5 Stars)', fontsize=12, fontweight='bold')

        plt.yticks(ticks=[1, 2, 3, 4, 5])
        plt.ylim(0.5, 5.5)
        plt.xticks(rotation=45, ha='right')
        plt.grid(axis='y', linestyle='--', alpha=0.6)

        plt.tight_layout()
        plt.savefig(output_path, dpi=300)
        plt.close()

        print(f"✅ Box Plot successfully saved to: {output_path}")

        # Calculate summary statistics
        analysis_data = data.groupby('brand_name')['rating'].agg(['mean', 'median', 'min', 'max',
                                                                  'std']).sort_values(by='mean', ascending=False)
        analysis_data['IQR'] = data.groupby('brand_name')[
            'rating'].apply(lambda x: x.quantile(0.75) - x.quantile(0.25))

        print("\n--- Rating Dispersion Statistics by Brand (Top 10) ---")
        print(analysis_data.to_markdown())

    except Exception as e:
        print(f"❌ ERROR during Box Plot creation: {e}")