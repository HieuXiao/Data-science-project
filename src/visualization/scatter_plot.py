# ================================
# 1. IMPORT THƯ VIỆN CẦN THIẾT
# ================================
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# =========================================
# 2. ĐỌC FILE CSV (CÓ XỬ LÝ ENCODING)
# =========================================
file_path = r"fakestore_api_products.csv"

try:
    # Thử đọc bằng UTF-8
    df = pd.read_csv(file_path, encoding='utf-8')
except UnicodeDecodeError:
    try:
        # Nếu lỗi, dùng Latin-1
        df = pd.read_csv(file_path, encoding='latin1')
    except:
        # Cuối cùng thử ISO-8859-1
        df = pd.read_csv(file_path, encoding='ISO-8859-1')

# ======================================================================
# 3. XỬ LÝ CỘT "rating" — CHUYỂN JSON THÀNH 2 CỘT: rate & count
# ======================================================================
# rating trong file có dạng:  "{'rate': 3.9, 'count': 120}"

if 'rating' in df.columns:

    # Tách rating thành rating_rate và rating_count
    df['rating_rate'] = df['rating'].apply(lambda x: eval(x)['rate'])
    df['rating_count'] = df['rating'].apply(lambda x: eval(x)['count'])

    # Xóa cột rating gốc vì không còn cần thiết
    df = df.drop('rating', axis=1)

# Chuẩn hóa tên cột về dạng chữ thường + loại bỏ khoảng trắng
df.columns = df.columns.str.lower().str.strip()

# =========================================
# 4. IN MỘT SỐ DÒNG ĐỂ KIỂM TRA DỮ LIỆU
# =========================================
print("\n=== SAMPLE DATA AFTER CLEANING ===")
print(df[['title', 'price', 'rating_rate', 'rating_count']].head())

# ==========================================================
# 5. TẠO SCATTER PLOT: PRICE vs RATING_COUNT (DEMAND)
# ==========================================================
# Theo tài liệu phase 3:
# Scatter plot dùng để tìm mối quan hệ giữa 2 biến số liên tục.
# Ở đây: 
#    - price: giá sản phẩm 
#    - rating_count: số lượt đánh giá (nhu cầu thị trường)

print("\n--- Creating Scatter Plot (Price vs Market Demand) ---")

plt.figure(figsize=(10, 6))

sns.scatterplot(
    data=df,
    x='price',
    y='rating_count',
    hue='category',     # phân loại theo danh mục
    s=120,              # kích thước điểm
    alpha=0.75          # độ trong suốt giúp nhìn rõ điểm chồng lấp
)

# ==================================================
# 6. CÀI ĐẶT TRỤC, TIÊU ĐỀ, CHÚ THÍCH, GRID
# ==================================================
plt.title('Scatter Plot: Price vs Market Demand', fontsize=14, fontweight='bold')
plt.xlabel('Price ($)', fontsize=12)
plt.ylabel('Rating Count (Market Demand)', fontsize=12)

plt.legend(title="Category", bbox_to_anchor=(1.05, 1), loc='upper left')

# Thêm đường lưới để biểu đồ dễ đọc hơn
plt.grid(True, linestyle='--', linewidth=0.6, alpha=0.5)

# Hiển thị biểu đồ
plt.tight_layout()
plt.show()

# =======================================
# 7. GIẢI THÍCH Ý NGHĨA (GỢI Ý REPORT)
# =======================================
print("\n=== INSIGHT GỢI Ý (DÙNG CHO PHẦN REPORT) ===")
print("""
- Scatter Plot này giúp kiểm tra mối quan hệ giữa giá và nhu cầu thị trường.
- rating_count đại diện cho “nhu cầu” → sản phẩm được đánh giá nhiều hơn = nhiều người quan tâm hơn.
- Quan sát nhanh thường thấy:
    + Sản phẩm giá rẻ → rating_count cao (nhu cầu lớn).
    + Sản phẩm giá cao → rating_count thấp (nhu cầu thấp).
- Đây là dạng phân tích rất quan trọng trong Phase 3:
    • Price = biến độc lập.
    • Rating count = biến phản ánh hành vi thị trường.
""")
