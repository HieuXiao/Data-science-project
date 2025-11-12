from src.visualization.box_plot import create_box_plot

def main():
    data_path = "data/raw/fakestore_api_products.csv"
    create_box_plot(data_path)

if __name__ == "__main__":
    main()
