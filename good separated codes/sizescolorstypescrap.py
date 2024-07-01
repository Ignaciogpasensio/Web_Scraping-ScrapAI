import requests
from bs4 import BeautifulSoup
import json
import argparse
import re

# Base URL of Scalpers website
base_url = 'https://en.gb.scalperscompany.com'


def extract_product_data(product, meta_data):
    data_dict_two = {}

    # Extracting the product ID
    product_id = product.get('id')
    product_id = str(product_id)
    data_dict_two["product_id"] = product_id

    # Extracting the rest of the data (colors, sizes, price, etc.)
    variants = product.get('variants', [])

    # Extracting cloth type (if available)
    data_dict_two['cloth_type'] = product.get('type', 'No type')

    # Extracting sizes from variants
    sizes = []
    for variant in variants:
        size = variant.get('public_title')
        if size:
            sizes.append(size.split('/')[1].strip())  # Extract size from the variant's public title
    data_dict_two['sizes'] = sizes

    # Extracting colors from variants
    colors = []
    for variant in variants:
        color = variant.get('public_title')
        if color:
            colors.append(color.split('/')[0].strip())  # Extract color from the variant's public title
    data_dict_two['colors'] = colors

    return data_dict_two


def scrape_products(skirts_url):
    products_data = []

    # Send a GET request to the skirts URL
    response = requests.get(skirts_url)

    # Check if the request was successful
    if response.status_code == 200:
        # Initialize BeautifulSoup object with the response text
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the script tag containing product data
        script_tag = soup.find('script', string=lambda text: text and 'var meta = ' in text)
        if script_tag:
            # Extract JavaScript object from script tag content
            json_data = re.search(r'var meta = ({.*});', script_tag.string)
            if json_data:
                meta_data = json.loads(json_data.group(1))
                products = meta_data.get('products', [])

                for product in products:
                    try:
                        # Extract product details
                        product_data = extract_product_data(product, meta_data)
                        products_data.append(product_data)

                    except Exception as e:
                        print(f'Error processing product: {e}')
                        continue

    else:
        print(f'Failed to fetch skirts page. Status code:', response.status_code)

    return products_data


def main():
    parser = argparse.ArgumentParser(description='Scrape product data from Scalpers website.')
    parser.add_argument('--type', choices=['skirts'], help='Type of clothing to scrape', required=True)
    args = parser.parse_args()

    if args.type == 'skirts':
        skirts_url = f'{base_url}/collections/woman-new-collection-skirts-2060'
        products_data = scrape_products(skirts_url)

        # Save scraped data to JSON file
        output_file = 'skirts_data_two.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(products_data, f, ensure_ascii=False, indent=2)
        
        print(f'Successfully scraped {len(products_data)} products. Data saved to {output_file}')

if __name__ == "__main__":
    main()
