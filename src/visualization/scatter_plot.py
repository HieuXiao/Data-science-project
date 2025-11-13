# ================================
# 1. IMPORT THƯ VIỆN CẦN THIẾT
# ================================
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import ast   # dùng để thay eval() cho an toàn

# =========================================
# 2. ĐỌC FILE CSV (CÓ XỬ LÝ ENCODING)
# =========================================
file_path = r"fakestore_api_products.csv"

try:
    df = pd.read_csv(file_path, encoding='utf-8')
except UnicodeDecodeError:
    try:
        df = pd.read_csv(file_path, encoding='latin1')
    except:
        df = pd.read_csv(file_path, encoding='ISO-8859-1')

# ======================================================
# 3. XỬ LÝ CỘT "rating" — TÁCH rate & count RA RIÊNG
# ======================================================
# rating = "{'rate': 3.9, 'count': 120}"

if 'rating' in df.columns:

    # Sử dụng literal_eval() để chuyển string thành dictionary an toàn
    df['rating_dict'] = df['rating'].apply(lambda x: ast.literal_eval(x))

    # Tách ra 2 cột mới
    df['rating_rate'] = df['rating_dict'].apply(lambda d: d['rate'])
    df['rating_count'] = df['rating_dict'].apply(lambda d: d['count'])

    # Xoá cột rating cũ cho sạch
    df = df.drop(['rating', 'rating_dict'], axis=1)

# Chuẩn hoá tên cột
df.columns = df.columns.str.lower().str.strip()

# =========================================
# 4. IN MỘT SỐ DÒNG ĐỂ KIỂM TRA
# =========================================
print("\n=== SAMPLE DATA AFTER CLEANING ===")
print(df[['title', 'price', 'rating_rate', 'rating_count']].head())

# ==========================================================
# 5. THỐNG KÊ TỔNG QUAN — PHẦN QUAN TRỌNG CỦA PHASE 3
# ==========================================================
print("\n==============================")
print("📊 OVERVIEW STATISTICS")
print("==============================")

print(f"Tổng số sản phẩm: {len(df)}")
print(f"Giá trung bình: {df['price'].mean():.2f} $")
print(f"Rating trung bình: {df['rating_rate'].mean():.2f}")
print(f"Số lượt đánh giá trung bình: {df['rating_count'].mean():.1f}")

print("\nGiá trị nhỏ nhất & lớn nhất:")
print(f"  • Giá min: {df['price'].min()} $")
print(f"  • Giá max: {df['price'].max()} $")
print(f"  • Rating count min: {df['rating_count'].min()}")
print(f"  • Rating count max: {df['rating_count'].max()}")

print("\nThống kê mô tả chi tiết:")
print(df[['price', 'rating_rate', 'rating_count']].describe())

# ==========================================================
# 6. TẠO SCATTER PLOT: PRICE vs RATING_COUNT (Như yêu cầu)
# ==========================================================
print("\n--- Creating Scatter Plot (Price vs Market Demand) ---")

plt.figure(figsize=(10, 6))

sns.scatterplot(
    data=df,
    x='price',
    y='rating_count',
    hue='category',     # phân màu theo danh mục
    s=120,
    alpha=0.75
)

# Tiêu đề + nhãn trục
plt.title('Scatter Plot: Price vs Market Demand', fontsize=14, fontweight='bold')
plt.xlabel('Price ($)', fontsize=12)
plt.ylabel('Rating Count (Market Demand)', fontsize=12)

# Legend
plt.legend(title="Category", bbox_to_anchor=(1.05, 1), loc='upper left')

# Grid
plt.grid(True, linestyle='--', linewidth=0.6, alpha=0.5)

plt.tight_layout()
plt.show()

# =======================================
# 7. GỢI Ý GIẢI THÍCH — ĐỂ VIẾT VÀO REPORT
# =======================================
print("\n=== INSIGHT GỢI Ý CHO BÁO CÁO ===")
print("""
• Biểu đồ scatter giúp quan sát mối quan hệ giữa giá sản phẩm và nhu cầu thị trường.
• rating_count đại diện cho nhu cầu (sản phẩm được nhiều người đánh giá → nhiều người mua).
• Thường thấy:
    - Sản phẩm giá thấp → rating_count cao.
    - Sản phẩm giá cao → rating_count thấp.
• Đây là phân tích quan trọng trong Phase 3 vì thể hiện trực quan:
    X-axis: Price → yếu tố kinh tế
    Y-axis: Rating Count → hành vi người tiêu dùng
""")
