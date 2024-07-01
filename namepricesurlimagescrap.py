import requests
from bs4 import BeautifulSoup
import json
import argparse
import re

# Base URL of Scalpers website
base_url = 'https://en.gb.scalperscompany.com'


def extract_product_data(product_url):
    data_dict = {}
    response = requests.get(product_url)
    
    if response.status_code == 200:
        # Initialize BeautifulSoup object with the response text
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the script with id 'viewed_product'
        script_tag = soup.find('script', id='viewed_product')
        if script_tag:
            script_content = script_tag.string

            # Use regex to find features
            name_match = re.search(r'Name:\s*"([^"]+)"', script_content)
            price_match = re.search(r'Price:\s*"([^"]+)"', script_content)
            compare_at_price_match = re.search(r'CompareAtPrice:\s*"([^"]+)"', script_content)
            product_id_match = re.search(r'ProductID:\s*(\d+),', script_content)
            url_match = re.search(r'URL:\s*"([^"]+)"', script_content)
            image_url_match = re.search(r'ImageURL:\s*"([^"]+)"', script_content)

            if name_match:
                product_name = name_match.group(1)
                data_dict['product_name'] = product_name

            if product_id_match:
                product_id = product_id_match.group(1)
                data_dict['product_id'] = product_id

            if price_match:
                price = price_match.group(1)
                price = float(price.replace("£", ""))
            else:
                data_dict['product_price_after'] = 0
            if compare_at_price_match:
                compare_at_price = compare_at_price_match.group(1)
                compare_at_price = float(compare_at_price.replace("£", ""))
            else:
                data_dict['product_price_after'] = 0
            discount = compare_at_price - price
            discount = "{:.2f}".format((discount * 100)/price)
            data_dict['product_price_after'] = "£" + str(price)
            data_dict['product_price_before'] = "£" + str(compare_at_price)
            data_dict['product_discount'] = "-" + str(discount) + "%"

            if url_match:
                product_url = url_match.group(1)
                data_dict['product_url'] = product_url
            else:
                data_dict['product_url'] = "URL not found"

            if image_url_match:
                product_image_url = image_url_match.group(1)
                data_dict['product_image_url'] = product_image_url

        else:
            print(f"No se encontró el script 'viewed_product' para el producto: {product_url}")

    else:
        print(f"Fallo al obtener la página del producto '{product_url}'. Código de estado:", response.status_code)

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