# main.py

import os
import sys
# Import các hàm từ module ingestion
from src.ingestion.data_fetcher import (
    fetch_product_ids,
    fetch_product_details,
    fetch_product_comments
)


# Thêm import cho các module Visualization (sau này sẽ cần)
# from src.visualization.line_bar_plot import create_line_bar_plot
# from src.visualization.box_plot import create_box_plot
# from src.visualization.scatter_plot import create_scatter_plot

def setup_environment():
    """Tạo thư mục 'data' và 'reports' nếu chưa tồn tại."""
    if not os.path.exists('data'):
        os.makedirs('data')
        print("Đã tạo thư mục 'data/'.")
    if not os.path.exists('reports'):
        os.makedirs('reports')
        print("Đã tạo thư mục 'reports/'.")


def run_data_ingestion():
    """Thực thi toàn bộ quy trình Data Ingestion."""
    print("\n--- Bắt đầu quy trình Data Ingestion từ Tiki ---")

    # Bước 1: Lấy ID sản phẩm (Category Nhà Sách Tiki: 8322)
    df_ids = fetch_product_ids(category_id='8322', max_pages=20, output_path='data/product_id_sach.csv')

    if df_ids.empty:
        print("\nQuy trình dừng lại vì không thu thập được ID sản phẩm.")
        return

    # Bước 2: Lấy chi tiết sản phẩm
    fetch_product_details(input_path='data/product_id_sach.csv', output_path='data/crawled_data_sach.csv')

    # Bước 3: Lấy bình luận sản phẩm
    fetch_product_comments(input_path='data/product_id_sach.csv', max_comment_pages=5, output_path='data/comments_data_sach.csv')

    print("\n--- Quy trình Data Ingestion đã hoàn thành! ---")


def run_visualization_plots():
    """Hiển thị menu Visualization và xử lý lựa chọn."""

    while True:
        print("\n----------------------------------------------")
        print("📊 CHỌN BIỂU ĐỒ TRỰC QUAN HÓA 📊")
        print("----------------------------------------------")
        print("3.1. Biểu đồ Line-Bar (Line-Bar Plot)")
        print("3.2. Biểu đồ Box-plot (Phân phối & ngoại lệ)")
        print("3.3. Biểu đồ Scatter (Quan hệ giữa các biến)")
        print("3.4. 🔙 Quay lại Menu Chính")
        print("----------------------------------------------")

        vis_choice = input("Vui lòng chọn loại biểu đồ (VD: 3.1): ").strip()

        if vis_choice=='3.1':
            print("Đang tạo Biểu đồ Line-Bar...")
            # create_line_bar_plot(...)
            print("Đã gọi hàm cho Biểu đồ Line-Bar (Cần triển khai trong src/visualization/line_bar_plot.py)")
        elif vis_choice=='3.2':
            print("Đang tạo Biểu đồ Box-plot...")
            # create_box_plot(...)
            print("Đã gọi hàm cho Biểu đồ Box-plot (Cần triển khai trong src/visualization/box_plot.py)")
        elif vis_choice=='3.3':
            print("Đang tạo Biểu đồ Scatter...")
            # create_scatter_plot(...)
            print("Đã gọi hàm cho Biểu đồ Scatter (Cần triển khai trong src/visualization/scatter_plot.py)")
        elif vis_choice=='3.4':
            break
        else:
            print("Lựa chọn không hợp lệ. Vui lòng nhập lại (VD: 3.1 hoặc 3.4).")


def main_menu():
    """Hiển thị menu chính và xử lý lựa chọn của người dùng."""

    setup_environment()

    while True:
        print("\n==============================================")
        print("🚀 MENU DỰ ÁN KHOA HỌC DỮ LIỆU TIKI 🚀")
        print("==============================================")
        print("1. 📥 Crawl Data (Thu thập dữ liệu từ Tiki API)")
        print("2. 🧹 Clean Data (Làm sạch dữ liệu đã crawl) (Chưa triển khai)")
        print("3. 📊 Visualize Data (Trực quan hóa dữ liệu)")
        print("4. ❌ Thoát")
        print("==============================================")

        choice = input("Vui lòng chọn chức năng (Nhập số): ").strip()

        if choice=='1':
            run_data_ingestion()
        elif choice=='2':
            print("\nChức năng làm sạch dữ liệu đang được xây dựng. Vui lòng chọn chức năng khác.")
        elif choice=='3':
            run_visualization_plots()  # Gọi Menu phụ cho Visualization
        elif choice=='4':
            print("Tạm biệt! Hẹn gặp lại.")
            sys.exit(0)
        else:
            print("Lựa chọn không hợp lệ. Vui lòng nhập lại số từ 1 đến 4.")


if __name__=="__main__":
    main_menu()
