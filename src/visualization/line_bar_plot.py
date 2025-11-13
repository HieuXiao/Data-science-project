# ==============================
# 1. IMPORT THƯ VIỆN CẦN THIẾT
# ==============================
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# =====================================================
# 2. ĐỌC FILE CSV CHỨA DỮ LIỆU BOOKS (CÓ XỬ LÝ ENCODING)
# =====================================================
try:
    # Thử đọc file bằng mã hóa UTF-8
    books_df = pd.read_csv('/Users/nguyentien/Documents/PDS301m/books_to_scrape.csv', encoding='utf-8')
except UnicodeDecodeError:
    try:
        # Nếu lỗi, thử đọc bằng Latin-1
        books_df = pd.read_csv('/Users/nguyentien/Documents/PDS301m/books_to_scrape.csv', encoding='latin-1')
    except:
        # Cuối cùng thử bằng ISO-8859-1
        books_df = pd.read_csv('/Users/nguyentien/Documents/PDS301m/books_to_scrape.csv', encoding='ISO-8859-1')

# ========================================================
# 3. ĐỌC FILE CSV CHỨA DỮ LIỆU PRODUCTS (CÓ XỬ LÝ ENCODING)
# ========================================================
try:
    products_df = pd.read_csv('/Users/nguyentien/Documents/PDS301m/fakestore_api_products.csv', encoding='utf-8')
except UnicodeDecodeError:
    try:
        products_df = pd.read_csv('/Users/nguyentien/Documents/PDS301m/fakestore_api_products.csv', encoding='latin-1')
    except:
        products_df = pd.read_csv('/Users/nguyentien/Documents/PDS301m/fakestore_api_products.csv', encoding='ISO-8859-1')

# ==================================================
# 4. TẠO FIGURE GỒM 2 BIỂU ĐỒ (1 HÀNG, 2 CỘT SUBPLOT)
# ==================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

# ==========================================
# 5. XỬ LÝ DỮ LIỆU BOOKS VÀ VẼ BIỂU ĐỒ ax1
# ==========================================

# Tính giá trung bình theo rating (gom nhóm theo cột 'rating')
books_avg_price = books_df.groupby('rating')['price'].mean().sort_index()

# Vẽ biểu đồ đường biểu diễn giá trung bình
ax1.plot(books_avg_price.index, books_avg_price.values,
         marker='o', linewidth=2, markersize=8, color='#2E86AB', label='Giá TB')

# Vẽ thêm cột (bar chart) để minh họa trực quan
ax1.bar(books_avg_price.index, books_avg_price.values,
        alpha=0.3, color='#A23B72', label='Cột giá')

# Thiết lập tiêu đề, nhãn trục, lưới và chú thích
ax1.set_xlabel('Rating (Sao)', fontsize=12, fontweight='bold')
ax1.set_ylabel('Giá trung bình ($)', fontsize=12, fontweight='bold')
ax1.set_title('Books: Giá Trung Bình Theo Rating', fontsize=14, fontweight='bold')
ax1.grid(True, alpha=0.3, linestyle='--')
ax1.legend()

# Thiết lập trục x từ 1 đến 5 (giá trị rating)
ax1.set_xticks(range(1, 6))

# ===================================================
# 6. XỬ LÝ DỮ LIỆU PRODUCTS VÀ VẼ BIỂU ĐỒ KÉP ax2
# ===================================================

# Gom nhóm dữ liệu theo 'category' và tính thống kê
category_stats = products_df.groupby('category').agg({
    'id': 'count',      # Đếm số lượng sản phẩm mỗi danh mục
    'price': 'mean'     # Tính giá trung bình mỗi danh mục
}).round(2)             # Làm tròn 2 chữ số thập phân

# Tạo mảng vị trí trục x và bề rộng cột
x = np.arange(len(category_stats))
width = 0.35

# Tạo trục y phụ để hiển thị giá trung bình (song song với trục chính)
ax2_twin = ax2.twinx()

# Vẽ biểu đồ cột thể hiện số lượng sản phẩm
bars = ax2.bar(x - width/2, category_stats['id'], width,
               label='Số lượng SP', color='#F18F01', alpha=0.7)

# Vẽ biểu đồ đường thể hiện giá trung bình
line = ax2_twin.plot(x, category_stats['price'],
                     marker='s', linewidth=2.5, markersize=10,
                     color='#C73E1D', label='Giá TB')

# Thiết lập nhãn trục, tiêu đề và màu sắc trục
ax2.set_xlabel('Danh mục', fontsize=12, fontweight='bold')
ax2.set_ylabel('Số lượng sản phẩm', fontsize=12, fontweight='bold', color='#F18F01')
ax2_twin.set_ylabel('Giá trung bình ($)', fontsize=12, fontweight='bold', color='#C73E1D')
ax2.set_title('Products: Số Lượng & Giá TB Theo Danh Mục', fontsize=14, fontweight='bold')

# Cài đặt tên danh mục làm nhãn trục X
ax2.set_xticks(x)
ax2.set_xticklabels(category_stats.index, rotation=15, ha='right')

# Hiển thị lưới theo trục Y
ax2.grid(True, alpha=0.3, linestyle='--', axis='y')

# Hiển thị chú thích (legend) cho 2 trục
ax2.legend(loc='upper left')
ax2_twin.legend(loc='upper right')

# ===================================
# 7. TINH CHỈNH & HIỂN THỊ BIỂU ĐỒ
# ===================================
plt.tight_layout()                                   # Căn chỉnh bố cục cho gọn
plt.savefig('linebar_chart.png', dpi=300, bbox_inches='tight')  # Lưu ảnh chất lượng cao
plt.show()                                           # Hiển thị biểu đồ

# =====================================
# 8. IN CÁC THỐNG KÊ TỔNG QUAN RA MÀN HÌNH
# =====================================
print("=" * 60)
print("THỐNG KÊ DỮ LIỆU BOOKS")
print("=" * 60)
print(f"Tổng số sách: {len(books_df)}")
print(f"Giá trung bình: ${books_df['price'].mean():.2f}")
print(f"Rating trung bình: {books_df['rating'].mean():.2f}")
print("\nGiá trung bình theo Rating:")
print(books_avg_price)

print("\n" + "=" * 60)
print("THỐNG KÊ DỮ LIỆU PRODUCTS")
print("=" * 60)
print(f"Tổng số sản phẩm: {len(products_df)}")
print(f"Giá trung bình: ${products_df['price'].mean():.2f}")
print("\nThống kê theo danh mục:")
print(category_stats)
