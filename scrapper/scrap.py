import requests
from bs4 import BeautifulSoup
import json

def scrape_product_details(product_url):
    response = requests.get(product_url)
    if response.status_code != 200:
        print(f"Failed to fetch product page: {product_url}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')
    data_dict = {}

    # Extracting the product name
    product_name = soup.find('h1', class_='ProductMeta__Title')
    data_dict['product_name'] = product_name.text.strip() if product_name else ''

    # Extracting the SKU
    sku = soup.find('span', class_='ProductMeta__Sku')
    data_dict['sku'] = sku.text.strip() if sku else ''

    # Extracting the price
    price = soup.find('span', class_='ProductMeta__Price')
    data_dict['price'] = price.text.strip() if price else ''

    # Extracting the available sizes
    sizes = [size.text.strip() for size in soup.select('.ProductForm__Option [type="radio"]') if size['disabled'] != 'disabled']
    data_dict['sizes'] = sizes

    # Extracting the images
    images = [img['src'] for img in soup.select('.Product__Slideshow img')]
    data_dict['images'] = images

    # Extracting the metadata (details, composition, washing care, etc.)
    details = soup.find('div', class_='ProductMeta__Description')
    data_dict['metadata'] = details.text.strip().split('\n') if details else []

    data_dict['product_url'] = product_url
    data_dict['cloth_type'] = 'skirt'  # Since we are scraping skirts

    return data_dict

def scrape_skirts():
    url = 'https://en.gb.scalperscompany.com/collections/woman-new-collection-skirts-2060'
    response = requests.get(url)
    if response.status_code != 200:
        print("Failed to fetch the skirts collection page.")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    products = []

    product_links = [a['href'] for a in soup.select('.ProductItem__ImageWrapper a')]
    for link in product_links:
        product_url = 'https://en.gb.scalperscompany.com' + link
        product_details = scrape_product_details(product_url)
        if product_details:
            products.append(product_details)

    with open('skirts.json', 'w') as f:
        json.dump(products, f, indent=4)

if __name__ == "__main__":
    scrape_skirts()
