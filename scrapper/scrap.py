import requests
from bs4 import BeautifulSoup
import json

def scrape_skirts():
    url = 'https://en.gb.scalperscompany.com/collections/woman-new-collection-skirts-2060'
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        skirts = []

        # Write code here to extract data for each skirt product
        # Example code for extracting product names:
        product_divs = soup.find_all('div', class_='product-item')
        for product_div in product_divs:
            product_name = product_div.find('h5', class_='product-name').text.strip()
            # Extract other information (price, images, sizes, etc.)

            # Append data to skirts list
            skirts.append({
                'product_name': product_name,
                # Add more fields as per your requirements
            })

        # Save data to JSON file
        with open('skirts.json', 'w') as f:
            json.dump(skirts, f, indent=4)

if __name__ == "__main__":
    scrape_skirts()
