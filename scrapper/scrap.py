import requests
from bs4 import BeautifulSoup
import json
import argparse

# Base URL of Scalpers website
base_url = 'https://en.gb.scalperscompany.com'

def scrape_product_details(product_url):
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

        # Extracting other product details
        # Example: Extracting price
        price_elem = soup.find('span', class_='ProductItem__Price')
        if price_elem:
            data_dict['price'] = price_elem.text.strip()

        # Extracting product URL
        data_dict['product_url'] = product_url

        # Extracting SKU
        sku_elem = soup.find('div', class_='ProductItem__SKU')
        if sku_elem:
            data_dict['sku'] = sku_elem.text.strip()

        # Extracting images
        images = []
        image_elems = soup.find_all('img', class_='ProductItem__Image')
        for img_elem in image_elems:
            image_url = base_url + img_elem.get('src')
            images.append(image_url)
        data_dict['images'] = images

        # Extracting metadata if available
        metadata_elems = soup.find_all('div', class_='ProductMeta__Block')
        metadata = {}
        for meta_elem in metadata_elems:
            key = meta_elem.find(class_='ProductMeta__BlockLabel').text.strip()
            value = meta_elem.find(class_='ProductMeta__BlockContent').text.strip()
            metadata[key] = value
        data_dict['metadata'] = metadata

        # Extracting sizes if available
        sizes_elem = soup.find('select', class_='ProductForm__Option')
        if sizes_elem:
            sizes = [option.text.strip() for option in sizes_elem.find_all('option')]
            data_dict['sizes'] = sizes

        # Extracting cloth type (if available)
        cloth_type_elem = soup.find('span', class_='ProductMeta__Type')
        if cloth_type_elem:
            data_dict['cloth_type'] = cloth_type_elem.text.strip()

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

                # Scrape product details
                product_data = scrape_product_details(product_url)

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
