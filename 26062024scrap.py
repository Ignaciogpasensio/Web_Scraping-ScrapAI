import requests
from bs4 import BeautifulSoup
import json
import argparse
import re

# Base URL of Scalpers website
base_url = 'https://scalperscompany.com'

def extract_product_data(product):
    data_dict = {}

    # Extracting the product name, colors, and sizes
    data_dict["product_id"] = product.get('id')
    name = product.get('name', 'No name')

    # Using regex to extract product_name from the first variant name
    first_variant_name = product['variants'][0]['name']
    match = re.search(r'^(.*?) - ', first_variant_name)
    if match:
        product_name = match.group(1).strip()
    else:
        product_name = name.strip()

    data_dict['product_name'] = product_name

    # Extracting the rest of the data (colors, sizes, price, etc.)
    variants = product.get('variants', [])

    # Extracting the price
    price = None
    for variant in variants:
        if 'price' in variant:
            price = variant['price']
            break
    
    if price is None:
        raise ValueError(f"Invalid or missing price format for product: {name}")

    data_dict['price'] = price / 100  # Convert from cents to euros

    # Extracting product URL
    data_dict['product_url'] = f"{base_url}/products/{product.get('gid', '')}"

    # Extracting SKU and images from the first variant
    if variants:
        data_dict['sku'] = variants[0].get('sku', 'No SKU')
        data_dict['images'] = [f"https:{variants[0].get('image', {}).get('src', '')}"]
    else:
        data_dict['sku'] = 'No SKU'
        data_dict['images'] = ['']

    # Extracting cloth type (if available)
    data_dict['cloth_type'] = product.get('type', 'No type')

    # Extracting sizes from variants
    sizes = []
    for variant in variants:
        size = variant.get('public_title')
        if size:
            sizes.append(size.split('/')[1].strip())  # Extract size from the variant's public title
    data_dict['sizes'] = sizes

    # Extracting colors from variants
    colors = []
    for variant in variants:
        color = variant.get('public_title')
        if color:
            colors.append(color.split('/')[0].strip())  # Extract color from the variant's public title
    data_dict['colors'] = colors

    # Extracting metadata (if available)
    metadata = []
    if 'attributes' in product:
        for attr in product['attributes']:
            metadata.append(attr['name'])
    data_dict['metadata'] = metadata

    return data_dict

def scrape_and_save(category_url, min_price, max_price, output_file):
    products_data = []

    # Send a GET request to the category URL
    response = requests.get(category_url)

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
                        product_data = extract_product_data(product)
                        if min_price <= product_data['price'] <= max_price:
                            products_data.append(product_data)
                    except Exception as e:
                        print(f'Error processing product: {e}')
                        continue

                # Save scraped data to JSON file
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(products_data, f, ensure_ascii=False, indent=2)

                print(f'Successfully scraped {len(products_data)} products. Data saved to {output_file}')

            else:
                print("No valid JSON data found in script tag.")
        else:
            print("Product data script tag not found.")

    else:
        print(f'Failed to fetch products. Status code:', response.status_code)

def main():
    parser = argparse.ArgumentParser(description='Scrape product data from Scalpers website.')
    parser.add_argument('--category', choices=['faldas', 'favoritos', 'vestidos_monos', 'sneakers', 'bolsos', 'toallas'], help='Category of clothing to scrape', required=True)
    parser.add_argument('--min_price', type=float, help='Minimum price', default=0.0)
    parser.add_argument('--max_price', type=float, help='Maximum price', default=1000.0)
    args = parser.parse_args()

    category_map = {
        'faldas': '/collections/mujer-nueva-coleccion-ropa-faldas-2060',
        'favoritos': '/collections/mujer-favoritos-2105',
        'vestidos_monos': '/collections/mujer-nueva-coleccion-ropa-vestidos-y-monos-2086',
        'sneakers': '/collections/mujer-nueva-coleccion-calzado-sneakers-2029',
        'bolsos': '/collections/mujer-nueva-coleccion-accesorios-bolsos-y-marroquineria-piel-2012',
        'toallas': '/collections/mujer-nueva-coleccion-accesorios-toallas-2606'
    }

    category_url = f'{base_url}{category_map[args.category]}'
    output_file = 'search.json'

    # Scrape and save products
    scrape_and_save(category_url, args.min_price, args.max_price, output_file)

if __name__ == "__main__":
    main()
