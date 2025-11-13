import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np


# --- PLACEHOLDER: Line-Bar Brand Stats Plot (Giữ lại để không gây lỗi import) ---
def create_line_bar_plot(input_path, output_path):
    """Placeholder cho mục Brand Stats, không được gọi trong menu mới."""
    print("\n[Visualization] Line-Bar Brand Stats Plot: Placeholder is currently active.")
    pass


# --- IMPLEMENTATION: Time Series Trend Plot (Mục tiêu Phụ P1) ---
def create_line_bar_time_series_plot(input_path, output_path):
    """
    Tạo biểu đồ Line-Bar kết hợp để phân tích Xu hướng Hài lòng theo Thời gian (Tháng-Năm).
    - Bar: Tổng số lượng đánh giá (Count)
    - Line: Điểm đánh giá trung bình (Avg Rating)
    """
    print(f"\n[Visualization] Bắt đầu tạo Biểu đồ Xu hướng Hài lòng theo Thời gian từ: {input_path}")

    if not os.path.exists(input_path):
        print(f"⚠️ LỖI: File không tồn tại tại đường dẫn: {input_path}")
        return

    try:
        # 1. Đọc dữ liệu
        df = pd.read_csv(input_path)

        # 2. Xử lý cột thời gian (Sử dụng cột đã được làm sạch)
        df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce')

        # Loại bỏ các hàng thiếu giá trị cần thiết
        df.dropna(subset=['created_at', 'rating'], inplace=True)

        if df.empty:
            print("⚠️ LỖI: DataFrame trống sau khi xử lý thời gian và rating.")
            return

        # 3. Nhóm dữ liệu theo Tháng-Năm (Month-Year)
        df['Month_Year'] = df['created_at'].dt.to_period('M')

        # Tính toán thống kê
        time_stats = df.groupby('Month_Year').agg(
            avg_rating=('rating', 'mean'),
            review_count=('comment_id', 'size')
        ).reset_index()

        # Chuyển Month_Year về định dạng string ('YYYY-MM') để dễ hiển thị trên trục X
        time_stats['Month_Year'] = time_stats['Month_Year'].dt.strftime('%Y-%m')

        # 4. Vẽ BIỂU ĐỒ LINE BAR
        fig, ax1 = plt.subplots(figsize=(14, 7))

        # --- Trục Y chính (Trái): Số lượng đánh giá (Bar Plot) ---
        color_bar = '#4CAF50'  # Màu xanh lá
        ax1.set_xlabel('Tháng-Năm', fontsize=12, fontweight='bold')
        ax1.set_ylabel('Tổng số lượng đánh giá (Cột)', color=color_bar, fontsize=12, fontweight='bold')
        bars = ax1.bar(time_stats['Month_Year'], time_stats['review_count'],
            color=color_bar, alpha=0.6, label='Số lượng đánh giá')
        ax1.tick_params(axis='y', labelcolor=color_bar)

        # Tối ưu hóa hiển thị nhãn trục X
        n = len(time_stats['Month_Year'])
        step = max(1, n // 10)  # Hiển thị khoảng 10 nhãn
        ax1.set_xticks(time_stats['Month_Year'][::step])
        ax1.tick_params(axis='x', rotation=45)

        # --- Trục Y phụ (Phải): Điểm đánh giá trung bình (Line Plot) ---
        ax2 = ax1.twinx()
        color_line = '#FF5722'  # Màu cam-đỏ
        ax2.set_ylabel('Điểm đánh giá Trung bình (Đường)', color=color_line, fontsize=12, fontweight='bold')
        line = ax2.plot(time_stats['Month_Year'], time_stats['avg_rating'],
            color=color_line, marker='o', linewidth=2, label='Điểm TB')
        ax2.tick_params(axis='y', labelcolor=color_line)

        # Thiết lập giới hạn trục Y phụ (Rating từ 1 đến 5)
        min_rating = time_stats['avg_rating'].min()
        ax2.set_ylim(max(1.0, min_rating - 0.1), 5.1)
        ax2.grid(True, linestyle='--', alpha=0.3)

        # Tiêu đề
        plt.title('Xu hướng Hài lòng & Số lượng đánh giá theo Thời gian', fontsize=16, fontweight='bold')

        # Gộp chú thích
        lines_labels = [bars] + line
        labels = [l.get_label() for l in lines_labels]
        ax1.legend(lines_labels, labels, loc='upper left')

        # Căn chỉnh bố cục và Lưu biểu đồ
        plt.tight_layout()
        plt.savefig(output_path, dpi=300)
        plt.close(fig)

        print(f"✅ Biểu đồ đã được lưu thành công tại: {output_path}")

        # In ra bảng thống kê
        print("\n--- Bảng Thống kê Xu hướng Hài lòng theo Thời gian (Tháng-Năm) ---")
        print(time_stats.to_markdown(index=False))

    except Exception as e:
        print(f"❌ LỖI trong quá trình tạo biểu đồ Line-Bar Time Series: {e}")