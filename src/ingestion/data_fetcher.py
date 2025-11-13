# src/ingestion/data_fetcher.py

import requests
import time
import random
import pandas as pd
from tqdm import tqdm
import os

# --- Cấu hình chung ---
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'vi-VN,vi;q=0.8,en-US;q=0.5,en;q=0.3',
    'Referer': 'https://tiki.vn/?src=header_tiki',
    'x-guest-token': '8jWSuIDBb2NGVzr6hsUZXpkP1FRin7lY',
    'Connection': 'keep-alive',
    'TE': 'Trailers',
}

COOKIES = {}  # Cập nhật nếu bị chặn


# --- Hàm tiện ích: Parser dữ liệu ---

def parser_product(json):
    """Phân tích JSON chi tiết sản phẩm thành một dict phẳng."""
    d = dict()
    d['id'] = json.get('id')
    d['sku'] = json.get('sku')
    d['short_description'] = json.get('short_description')
    d['price'] = json.get('price')
    d['list_price'] = json.get('list_price')
    d['discount'] = json.get('discount')
    d['discount_rate'] = json.get('discount_rate')
    d['review_count'] = json.get('review_count')
    d['order_count'] = json.get('order_count')
    d['product_name'] = json.get('meta_title')

    # Xử lý Brand và Stock
    brand = json.get('brand')
    d['brand_id'] = brand.get('id') if brand else None
    d['brand_name'] = brand.get('name') if brand else None

    stock = json.get('stock_item')
    d['stock_item_qty'] = stock.get('qty') if stock else None
    d['stock_item_max_sale_qty'] = stock.get('max_sale_qty') if stock else None

    return d


def comment_parser(json):
    """Phân tích JSON bình luận thành một dict phẳng."""
    d = dict()
    d['id'] = json.get('id')
    d['title'] = json.get('title')
    d['content'] = json.get('content')
    d['thank_count'] = json.get('thank_count')
    d['customer_id'] = json.get('customer_id')
    d['rating'] = json.get('rating')
    d['created_at'] = json.get('created_at')

    # Xử lý Created By
    created_by = json.get('created_by')
    d['customer_name'] = created_by.get('name') if created_by else 'Ẩn danh'
    d['purchased_at'] = created_by.get('purchased_at') if created_by else None
    d['product_id'] = json.get('product_id')

    return d


# --- Các hàm chính cho Data Ingestion ---

def fetch_product_ids(category_id='8322', max_pages=20, output_path='data/product_id_sach.csv'):
    """Lấy danh sách ID sản phẩm từ API theo danh mục."""
    print(f"Bắt đầu crawl ID sản phẩm cho Category ID: {category_id}")
    params = {
        'limit': '48',
        'include': 'sale-attrs,badges,product_links,brand,category,stock_item,advertisement',
        'aggregations': '1',
        'trackity_id': '70e316b0-96f2-dbe1-a2ed-43ff60419991',
        'category': str(category_id),
        'page': '1',
        'src': f'c{category_id}',
        'urlKey': 'nha-sach-tiki',
    }

    product_id_list = []
    for i in range(1, max_pages + 1):
        params['page'] = i
        response = requests.get('https://tiki.vn/api/v2/products', headers=HEADERS, params=params)

        if response.status_code==200:
            print(f'  -> Request page {i} success ({len(response.json().get("data"))} items)')
            for record in response.json().get('data'):
                product_id_list.append({'id': record.get('id')})
        else:
            print(f'  -> Request page {i} failed with status code: {response.status_code}. Stopping.')
            break

        time.sleep(random.uniform(3, 10))

    df = pd.DataFrame(product_id_list)
    df.to_csv(output_path, index=False)
    print(f"Hoàn tất. Đã lưu {len(df)} ID vào: {output_path}")
    return df


def fetch_product_details(input_path='data/product_id_sach.csv', output_path='data/crawled_data_sach.csv'):
    """Crawl chi tiết sản phẩm dựa trên danh sách ID đã có."""
    print(f"\nBắt đầu crawl chi tiết sản phẩm từ file ID: {input_path}")

    if not os.path.exists(input_path):
        print(f"Lỗi: Không tìm thấy file ID tại {input_path}.")
        return pd.DataFrame()

    df_id = pd.read_csv(input_path)
    p_ids = df_id.id.to_list()
    result = []

    product_params = (('platform', 'web'),)

    for pid in tqdm(p_ids, total=len(p_ids)):
        time.sleep(random.uniform(3, 5))

        url = f'https://tiki.vn/api/v2/products/{pid}'
        response = requests.get(url, headers=HEADERS, params=product_params, cookies=COOKIES)

        if response.status_code==200:
            result.append(parser_product(response.json()))
        else:
            print(f'\nCrawl data {pid} failed with status code: {response.status_code}')

    df_product = pd.DataFrame(result)
    df_product.to_csv(output_path, index=False)
    print(f"Hoàn tất. Đã lưu {len(df_product)} chi tiết sản phẩm vào: {output_path}")
    return df_product


def fetch_product_comments(input_path='data/product_id_sach.csv', max_comment_pages=5, output_path='data/comments_data_sach.csv'):
    """Crawl bình luận sản phẩm dựa trên danh sách ID đã có."""
    print(f"\nBắt đầu crawl bình luận sản phẩm từ file ID: {input_path}")

    if not os.path.exists(input_path):
        print(f"Lỗi: Không tìm thấy file ID tại {input_path}.")
        return pd.DataFrame()

    df_id = pd.read_csv(input_path)
    p_ids = df_id.id.to_list()
    result = []

    comment_params = {
        'sort': 'score|desc,id|desc,stars|all',
        'page': '1',
        'limit': '10',
        'include': 'comments'
    }

    for pid in tqdm(p_ids, total=len(p_ids)):
        comment_params['product_id'] = pid

        for i in range(1, max_comment_pages + 1):
            comment_params['page'] = i

            time.sleep(random.uniform(0.5, 1.5))

            try:
                response = requests.get('https://tiki.vn/api/v2/reviews', headers=HEADERS, params=comment_params, cookies=COOKIES)

                if response.status_code==200:
                    data = response.json()

                    if not data.get('data'):
                        break

                    for comment in data.get('data'):
                        # Thêm product_id vào comment trước khi parse
                        comment['product_id'] = pid
                        result.append(comment_parser(comment))
                else:
                    break
            except Exception as e:
                print(f'\nLỗi trong khi crawl bình luận PID {pid} trang {i}: {e}')
                break

    df_comment = pd.DataFrame(result)
    df_comment.to_csv(output_path, index=False)
    print(f"Hoàn tất. Đã lưu {len(df_comment)} bình luận vào: {output_path}")
    return df_comment
