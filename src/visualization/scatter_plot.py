# Data-science-project\src\visualization\scatter_plot.py

# ================================
# 1. IMPORT THƯ VIỆN CẦN THIẾT
# ================================
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import numpy as np


# =========================================================================
# 2. HÀM TẠO BIỂU ĐỒ PHÂN TÁN: ĐỘ DÀI BÌNH LUẬN VS. ĐIỂM ĐÁNH GIÁ (RATING)
# =========================================================================
def create_scatter_plot(input_path, output_path):
    """
    Tạo biểu đồ Phân tán (Scatter Plot) để phân tích mối quan hệ giữa Độ dài Bình luận
    (số ký tự) và Điểm đánh giá (Rating Score).

    Args:
        input_path (str): Đường dẫn đến file CSV chứa dữ liệu đã hợp nhất.
        output_path (str): Đường dẫn để lưu ảnh Biểu đồ Phân tán.
    """
    print(f"\n[Visualization] Bắt đầu tạo Biểu đồ Phân tán (Độ dài Bình luận vs. Rating) từ: {input_path}")

    if not os.path.exists(input_path):
        print(f"⚠️ LỖI: Không tìm thấy file tại đường dẫn: {input_path}")
        return

    try:
        # ==========================================
        # 2.1. ĐỌC VÀ CHUẨN BỊ DỮ LIỆU
        # ==========================================
        df = pd.read_csv(input_path)

        # Đảm bảo cột nội dung (content) tồn tại và điền giá trị thiếu (NaN)
        df['content'] = df['content'].fillna('')

        # Tính toán Độ dài Bình luận (số ký tự)
        df['review_length'] = df['content'].apply(len)

        # Lọc dữ liệu: chỉ giữ lại các bình luận có nội dung và rating hợp lệ (1-5)
        df_filtered = df[(df['review_length'] > 0) & (df['rating'] >= 1) & (df['rating'] <= 5)].copy()

        if df_filtered.empty:
            print("⚠️ CẢNH BÁO: Không có bình luận có nội dung để phân tích.")
            return

        # =========================================================
        # 2.2. CẤU HÌNH VÀ VẼ SCATTER PLOT VỚI ĐƯỜNG HỒI QUY
        # =========================================================
        plt.figure(figsize=(10, 6))

        # Sử dụng sns.regplot để vẽ điểm phân tán và đường hồi quy tuyến tính
        # y_jitter=0.15 giúp làm rõ mật độ điểm do trục Y (Rating) là giá trị rời rạc
        sns.regplot(
            x='review_length',
            y='rating',
            data=df_filtered,
            x_jitter=0,
            y_jitter=0.15,
            scatter_kws={'alpha': 0.05, 's': 20, 'color': '#1f77b4'},  # Thiết lập điểm phân tán
            line_kws={'color': '#d62728', 'lw': 3}  # Thiết lập đường hồi quy
        )

        # =======================================
        # 2.3. TÍNH TOÁN VÀ THÊM THÔNG TIN PHÂN TÍCH
        # =======================================
        # Tính Hệ số tương quan Pearson
        correlation = df_filtered['review_length'].corr(df_filtered['rating'])

        # Tính Độ dài Trung bình theo Điểm Rating để báo cáo chi tiết
        avg_length_by_rating = df_filtered.groupby('rating')['review_length'].mean().sort_index()

        # =========================================
        # 2.4. TINH CHỈNH VÀ LƯU BIỂU ĐỒ
        # =========================================
        plt.title(f'Độ dài Bình luận vs. Điểm đánh giá (Tương quan: {correlation:.4f})', fontsize=16, fontweight='bold')
        plt.xlabel('Độ dài Bình luận (Số ký tự)', fontsize=12, fontweight='bold')
        plt.ylabel('Điểm đánh giá (1-5 Sao)', fontsize=12, fontweight='bold')

        # Thiết lập trục Y
        plt.yticks(ticks=[1, 2, 3, 4, 5])
        plt.ylim(0.5, 5.5)
        plt.grid(axis='y', linestyle='--', alpha=0.6)

        plt.tight_layout()
        plt.savefig(output_path, dpi=300)  # Lưu ảnh chất lượng cao
        plt.close()  # Đóng figure

        print(f"✅ Biểu đồ Phân tán đã được lưu thành công tại: {output_path}")

        # =============================================
        # 2.5. IN CÁC THỐNG KÊ TỔNG QUAN RA MÀN HÌNH
        # =============================================
        print("\n" + "=" * 60)
        print("THỐNG KÊ ĐỘ DÀI BÌNH LUẬN THEO ĐIỂM ĐÁNH GIÁ")
        print("=" * 60)
        print("Hệ số tương quan (Correlation): ", f"{correlation:.4f}")
        print("\nĐộ dài Trung bình theo Rating Score:")
        print(avg_length_by_rating.to_markdown())

    except Exception as e:
        print(f"❌ LỖI trong quá trình tạo Biểu đồ Phân tán: {e}")