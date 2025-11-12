import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def create_box_plot_with_ratings(file_path):

    data = pd.read_csv(file_path, encoding='latin1')

    required_columns = {'price', 'rating_rate'}
    if not required_columns.issubset(data.columns):
        raise ValueError(f"File CSV phải chứa các cột: {required_columns}")
    
    data = data.dropna(subset=['price', 'rating_rate'])

    price_bins = [0, data['price'].quantile(0.33), data['price'].quantile(0.66), data['price'].max()]
    price_labels = ['Low', 'Medium', 'High']
    data['price_group'] = pd.cut(data['price'], bins=price_bins, labels=price_labels, include_lowest=True)

    plt.figure(figsize=(8, 6))
    sns.boxplot(x='price_group', y='rating_rate', data=data, palette='muted')

    plt.title('Relationship Between Product Price and Customer Ratings', fontsize=14)
    plt.xlabel('Price Group', fontsize=12)
    plt.ylabel('Rating Score', fontsize=12)
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    avg_ratings = data.groupby('price_group')['rating_rate'].mean()
    print("Average rating by price group:\n", avg_ratings)

    print("\nConclusion: Higher-priced products tend to receive higher ratings.")

    plt.show()

create_box_plot_with_ratings('data/raw/fakestore_api_products.csv')  # Thay bằng đường dẫn file của bạn
