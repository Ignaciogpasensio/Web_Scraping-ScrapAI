import requests
from bs4 import BeautifulSoup
import json

def scrape_skirts():
    url = 'https://en.gb.scalperscompany.com/collections/woman-new-collection-skirts-2060'
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        skirts = []

        product_divs = soup.find_all('div', class_='product-item')

        for product_div in product_divs:
            product_name = product_div.find('h5', class_='product-name').text.strip()
            product_url = 'https://en.gb.scalperscompany.com' + product_div.find('a', class_='product-link')['href']
            sku = product_div.find('div', class_='product-sku').text.strip()
            images = [img['src'] for img in product_div.select('img.product-image')]
            price = product_div.find('span', class_='product-price').text.strip()
            sizes = [size.text.strip() for size in product_div.find_all('span', class_='product-size')]
            cloth_type = "skirt"  # Assuming all products are skirts based on the URL

            # Additional metadata extraction can be added here if needed

            skirts.append({
                'product_name': product_name,
                'product_url': product_url,
                'sku': sku,
                'images': images,
                'price': price,
                'sizes': sizes,
                'cloth_type': cloth_type
            })

        # Save data to JSON file
        with open('skirts.json', 'w') as f:
            json.dump(skirts, f, indent=4)
    else:
        print(f"Failed to fetch webpage. Status code: {response.status_code}")

if __name__ == "__main__":
    scrape_skirts()

