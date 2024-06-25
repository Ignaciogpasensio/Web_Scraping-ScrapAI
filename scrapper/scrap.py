import requests
from bs4 import BeautifulSoup
import json
from schema.product import ClothUnit
import argparse

def scrape_products(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        products = []

        # Logic to scrape each product
        for product in soup.find_all('div', class_='ProductItem'):
            product_data = {}

            # Extract product name
            product_name = product.find('div', class_='ProductItem__Title')
            if product_name:
                product_data['product_name'] = product_name.text.strip()

            # Extract product URL
            product_url = product.find('a', class_='ProductItem__Image')['href']
            product_data['product_url'] = f"https://en.gb.scalperscompany.com{product_url}"

            # Extract SKU if available
            sku = product.find('span', class_='ProductItem__Meta')
            if sku:
                product_data['sku'] = sku.text.strip()

            # Extract images if available
            images = []
            for img in product.find_all('img', class_='ProductItem__Image'):
                img_src = img.get('src')
                if img_src:
                    images.append(img_src)
            product_data['images'] = images

            # Metadata (if available)
            product_data['metadata'] = []

            # Price (if available)
            price = product.find('span', class_='ProductItem__Price')
            if price:
                product_data['price'] = price.text.strip()

            # Sizes (if available)
            sizes = product.find('div', class_='ProductItem__Sizes')
            if sizes:
                product_data['sizes'] = [size.text.strip() for size in sizes.find_all('span')]

            # Cloth type (skirt, etc.)
            product_data['cloth_type'] = 'skirt'

            # Append product data to products list
            products.append(product_data)

        return products
    else:
        print(f"Failed to fetch webpage: {url}. Status code: {response.status_code}")
        return None

def save_to_json(products_data):
    if products_data:
        with open('skirts.json', 'w', encoding='utf-8') as f:
            json.dump(products_data, f, ensure_ascii=False, indent=4)
        print("Data saved to skirts.json")
    else:
        print("No data to save")

def main():
    parser = argparse.ArgumentParser(description='Scrape skirt products from Scalpers website.')
    parser.add_argument('--type', choices=['skirts'], required=True, help='Type of clothing to scrape')
    args = parser.parse_args()

    if args.type == 'skirts':
        url = 'https://en.gb.scalperscompany.com/collections/woman-new-collection-skirts-2060'
        products_data = scrape_products(url)
        save_to_json(products_data)

if __name__ == "__main__":
    main()
