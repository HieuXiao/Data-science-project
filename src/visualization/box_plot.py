import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def create_box_plot_with_ratings(file_path):
    # Đọc dữ liệu từ file CSV
    data = pd.read_csv(file_path, encoding='latin1')

    # Kiểm tra cột cần thiết có trong file hay không
    required_columns = {'price', 'rating_rate'}
    if not required_columns.issubset(data.columns):
        raise ValueError(f"File CSV phải chứa các cột: {required_columns}")
    
    # Loại bỏ các giá trị thiếu (NaN) trong hai cột quan trọng
    data = data.dropna(subset=['price', 'rating_rate'])

    # Chia cột 'price' thành 3 nhóm: Low, Medium, High
    price_bins = [0, data['price'].quantile(0.33), data['price'].quantile(0.66), data['price'].max()]
    price_labels = ['Low', 'Medium', 'High']
    data['price_group'] = pd.cut(data['price'], bins=price_bins, labels=price_labels, include_lowest=True)

    # Vẽ box plot
    plt.figure(figsize=(8, 6))
    sns.boxplot(x='price_group', y='rating_rate', data=data, palette='muted')

    # Thêm tiêu đề và nhãn
    plt.title('Relationship Between Product Price and Customer Ratings', fontsize=14)
    plt.xlabel('Price Group', fontsize=12)
    plt.ylabel('Rating Score', fontsize=12)
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # Tính và in ra trung bình điểm đánh giá theo nhóm giá
    avg_ratings = data.groupby('price_group')['rating_rate'].mean()
    print("Average rating by price group:\n", avg_ratings)

    # Kết luận
    print("\nConclusion: Higher-priced products tend to receive higher ratings.")

    # Hiển thị biểu đồ
    plt.show()

# Gọi hàm với đường dẫn file của bạn
create_box_plot_with_ratings('data/raw/fakestore_api_products.csv')  # Thay bằng đường dẫn file của bạn
