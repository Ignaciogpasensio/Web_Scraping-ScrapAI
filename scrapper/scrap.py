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

        # Extracting other product details (price, image, description, etc.)
        # Example: Extracting price
        price_elem = soup.find('span', class_='ProductItem__Price')
        if price_elem:
            data_dict['price'] = price_elem.text.strip()

        # Example: Extracting image URL
        image_elem = soup.find('img', class_='ProductItem__Image')
        if image_elem:
            data_dict['image_url'] = base_url + image_elem.get('src')

        # Add more extraction logic for other product details as needed

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
