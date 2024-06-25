import requests
from bs4 import BeautifulSoup
import json
from schema.product import ClothUnit  # Assuming ClothUnit is defined in schema/product.py

def scrape_skirts():
    url = 'https://en.gb.scalperscompany.com/collections/woman-new-collection-skirts-2060'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        skirts = []

        # Logic to scrape each skirt product
        for product in soup.find_all('div', class_='ProductItem'):
            product_data = {}

            # Extract product name
            product_name = product.find('div', class_='ProductItem__Title')
            if product_name:
                product_data['product_name'] = product_name.text.strip()

            # Extract other details as per your requirement
            # Example: SKU, images, price, sizes, cloth type, etc.
            # For demonstration, let's assume some sample data
            product_data['sku'] = 'SampleSKU123'
            product_data['images'] = ['image_url1', 'image_url2']
            product_data['price'] = '£50'
            product_data['sizes'] = ['XS', 'S', 'M', 'L']
            product_data['cloth_type'] = 'skirt'
            product_data['metadata'] = ['Sample metadata 1', 'Sample metadata 2']

            # Append product data to skirts list
            skirts.append(product_data)

        return skirts
    else:
        print(f"Failed to fetch webpage: {url}. Status code: {response.status_code}")
        return None

def save_to_json(skirts_data):
    if skirts_data:
        with open('skirts.json', 'w', encoding='utf-8') as f:
            json.dump(skirts_data, f, ensure_ascii=False, indent=4)
        print("Data saved to skirts.json")
    else:
        print("No data to save")

# Main execution
if __name__ == "__main__":
    skirts_data = scrape_skirts()
    save_to_json(skirts_data)
