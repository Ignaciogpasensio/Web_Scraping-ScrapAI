import requests
from bs4 import BeautifulSoup
import json
import argparse

# Base URL of Scalpers website
base_url = 'https://en.gb.scalperscompany.com'

def extract_product_data(product_url):
    data_dict = {}

    # Send a GET request to the product URL
    response = requests.get(product_url)

    # Check if the request was successful
    if response.status_code == 200:
        # Initialize BeautifulSoup object with the response text
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extracting the product name
        product_name_elem = soup.find('h1', class_='ProductMeta__Title')
        if product_name_elem:
            data_dict['product_name'] = product_name_elem.text.strip()

        # Extracting the price
        price_elem = soup.find('span', class_='ProductItem__Price')
        if price_elem:
            data_dict['price'] = price_elem.text.strip()

        # Extracting product URL
        data_dict['product_url'] = product_url

        # Extracting SKU and images using the provided script section
        script_tag = soup.find('script', id='web-pixels-manager-setup')
        if script_tag:
            script_content = script_tag.contents[0]
            
            # Extract SKU
            start_index = script_content.find('"sku":"') + len('"sku":"')
            end_index = script_content.find('"', start_index)
            sku = script_content[start_index:end_index]
            data_dict['sku'] = sku

            # Extract images
            start_index = script_content.find('"src":"') + len('"src":"')
            end_index = script_content.find('"', start_index)
            image_url = script_content[start_index:end_index]
            data_dict['images'] = [image_url]

        else:
            print(f"Script tag not found for product: {product_url}")

        # Extracting cloth type (if available)
        data_dict['cloth_type'] = 'Falda'  # Assuming all are skirts as before

        # Extracting sizes using the old method
        variants_script_tag = soup.find('script', text=lambda text: text and 'var meta' in text)
        if variants_script_tag:
            try:
                start_index = variants_script_tag.string.find('var meta = ') + len('var meta = ')
                end_index = variants_script_tag.string.find('};', start_index) + 1
                json_data = variants_script_tag.string[start_index:end_index]
                meta_data = json.loads(json_data)
                product_data = meta_data.get('product', {})

                variants = product_data.get('variants', [])
                sizes = []
                for variant in variants:
                    sizes.append(variant.get('public_title', 'Not specified'))
                data_dict['sizes'] = sizes if sizes else ['Not specified']
            except json.JSONDecodeError as e:
                print(f"Error decoding variants JSON data: {e}")
        else:
            data_dict['sizes'] = ['Not specified']

        # Extracting metadata (if available)
        metadata_elem = soup.find('ul', class_='ProductMeta__DetailsList')
        if metadata_elem:
            metadata_items = metadata_elem.find_all('li')
            metadata = {}
            for item in metadata_items:
                key = item.find('span', class_='ProductMeta__Label').text.strip()
                value = item.find('span', class_='ProductMeta__Value').text.strip()
                metadata[key] = value
            data_dict['metadata'] = metadata
        else:
            data_dict['metadata'] = {}

    else:
        print(f"Failed to fetch product page '{product_url}'. Status code:", response.status_code)

    return data_dict

def scrape_products(skirts_url):
    products_data = []

    # Send a GET request to the skirts URL
    response = requests.get(skirts_url)

    # Check if the request was successful
    if response.status_code == 200:
        # Initialize BeautifulSoup object with the response text
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all product items within the specified class
        products = soup.find_all('div', class_='ProductItem')

        for product in products:
            try:
                # Extract product URL
                product_url = base_url + product.find('a')['href']

                # Extract product details
                product_data = extract_product_data(product_url)

                if product_data:
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
        output_file = 'skirts_data.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(products_data, f, ensure_ascii=False, indent=2)
        
        print(f'Successfully scraped {len(products_data)} products. Data saved to {output_file}')

if __name__ == "__main__":
    main()
