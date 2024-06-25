import requests
import json
import re
from schema.product import ClothUnit
import argparse

# Base URL of Scalpers website
base_url = 'https://en.gb.scalperscompany.com'
skirts_url = f'{base_url}/collections/woman-new-collection-skirts-2060'

def scrape_skirts():
    skirts_data = []

    # Fetch the HTML content of the skirts URL
    response = requests.get(skirts_url)
    if response.status_code == 200:
        # Extract JSON-LD structured data using regular expressions
        pattern = r'<script type="application/ld\+json">(.*?)</script>'
        json_ld_data = re.findall(pattern, response.text, re.DOTALL)

        for json_data in json_ld_data:
            try:
                product_info = json.loads(json_data)

                # Extract relevant fields from JSON-LD data
                product_url = product_info.get('url', '')
                product_name = product_info.get('name', '')
                sku = ''  # Extract SKU if available
                price = product_info.get('offers', {}).get('price', '')
                images = [product_info.get('image', {}).get('url', '')]
                metadata = [product_info.get('description', '')]

                # Create ClothUnit instance
                cloth_unit = ClothUnit(
                    product_url=product_url,
                    sku=sku,
                    product_name=product_name,
                    images=images,
                    metadata=metadata,
                    price=price,
                    sizes=[],  # You can add logic to extract sizes if available
                    cloth_type='skirt'  # Assuming all are skirts based on URL
                )

                skirts_data.append(cloth_unit.dict())

            except json.JSONDecodeError as e:
                print(f'Error decoding JSON: {e}')
                continue

    else:
        print(f'Failed to fetch skirts page. Status code: {response.status_code}')

    return skirts_data

def main():
    parser = argparse.ArgumentParser(description='Scrape skirts data from Scalpers website.')
    parser.add_argument('--type', choices=['skirts'], help='Type of clothing to scrape', required=True)
    args = parser.parse_args()

    if args.type == 'skirts':
        skirts_data = scrape_skirts()

        # Print skirts data in JSON format
        print(json.dumps(skirts_data, indent=2))

if __name__ == "__main__":
    main()
