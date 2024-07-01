import requests
from bs4 import BeautifulSoup
import json
import argparse
import re

base_url = 'https://es.scalperscompany.com'

def extract_product_data(product_url):
    data_dict = {}
    response = requests.get(product_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        script_tag = soup.find('script', id='viewed_product')
        if script_tag:
            script_content = script_tag.string
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
                price = float(price.replace("€", "").replace(",", "."))
            else:
                data_dict['product_price_after'] = 0
            if compare_at_price_match:
                compare_at_price = compare_at_price_match.group(1)
                compare_at_price = float(compare_at_price.replace("€", "").replace(",", "."))
            else:
                data_dict['product_price_before'] = 0
            discount = compare_at_price - price
            discount = "{:.2f}".format((discount * 100) / price)
            data_dict['product_price_after'] = "€" + str(price)
            data_dict['product_price_before'] = "€" + str(compare_at_price)
            data_dict['product_discount'] = "-" + str(discount) + "%"
            if url_match:
                product_url = url_match.group(1)
                data_dict['product_url'] = product_url
            else:
                data_dict['product_url'] = "URL not found"
            if image_url_match:
                product_image_url = image_url_match.group(1)
                data_dict['product_image_url'] = product_image_url
    return data_dict

def extract_product_data_two(product, meta_data):
    data_dict_two = {}
    product_id = product.get('id')
    product_id = str(product_id)
    data_dict_two["product_id"] = product_id
    variants = product.get('variants', [])
    data_dict_two['cloth_type'] = product.get('type', 'No type')
    sizes = []
    for variant in variants:
        size = variant.get('public_title')
        if size:
            sizes.append(size.split('/')[1].strip())
    data_dict_two['sizes'] = sizes
    colors = []
    for variant in variants:
        color = variant.get('public_title')
        if color:
            colors.append(color.split('/')[0].strip())
    data_dict_two['colors'] = colors
    return data_dict_two

def scrape_products(skirts_url):
    products_data = []
    response = requests.get(skirts_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        products = soup.select('a[href*="/products/"]')
        for product in products:
            try:
                product_url = base_url + product['href']
                product_data = extract_product_data(product_url)
                if product_data:
                    products_data.append(product_data)
            except Exception as e:
                continue
    return products_data

def scrape_products_two(skirts_url):
    products_data_two = []
    response = requests.get(skirts_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        script_tag = soup.find('script', string=lambda text: text and 'var meta = ' in text)
        if script_tag:
            json_data = re.search(r'var meta = ({.*});', script_tag.string)
            if json_data:
                meta_data = json.loads(json_data.group(1))
                products = meta_data.get('products', [])
                for product in products:
                    try:
                        product_data_two = extract_product_data_two(product, meta_data)
                        products_data_two.append(product_data_two)
                    except Exception as e:
                        continue
    return products_data_two

def main():
    parser = argparse.ArgumentParser(description='Scrape product data from Scalpers website.')
    parser.add_argument('--type', choices=['skirts'], help='Type of clothing to scrape', required=True)
    args = parser.parse_args()
    if args.type == 'skirts':
        skirts_url = f'{base_url}/collections/mujer-nueva-coleccion-ropa-faldas-2060'
        products_data = scrape_products(skirts_url)
        products_data_two = scrape_products_two(skirts_url)
        products_data_dict = {product['product_id']: product for product in products_data}
        for product_two in products_data_two:
            product_id = product_two['product_id']
            if product_id in products_data_dict:
                products_data_dict[product_id].update(product_two)
        products_data = list(products_data_dict.values())

        output_file = 'skirts_data.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(products_data, f, ensure_ascii=False, indent=2)
        
        print(f'Successfully scraped {len(products_data)} products. Data saved to {output_file}')

if __name__ == "__main__":
    main()