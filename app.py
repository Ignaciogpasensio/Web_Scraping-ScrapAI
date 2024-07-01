import streamlit as st
import requests
from bs4 import BeautifulSoup
import json
import argparse
import re
import subprocess

base_url = 'https://es.scalperscompany.com'

# Function to extract product data from the product URL
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
            brand_match = re.search(r'Brand:\s*"([^"]+)"', script_content)
            url_match = re.search(r'    URL:\s*"([^"]+)"', script_content)
            image_match = re.search(r'ImageURL:\s*"([^"]+)"', script_content)

            if name_match:
                product_name = name_match.group(1)
                data_dict['product_name'] = product_name

            if product_id_match:
                product_id = product_id_match.group(1)
                data_dict['product_id'] = product_id

            if price_match:
                price = price_match.group(1)
                price = float(price.replace("€", "").replace(",", "."))
                data_dict['product_price_after'] = price

            if compare_at_price_match:
                compare_at_price = compare_at_price_match.group(1)
                compare_at_price = float(compare_at_price.replace("€", "").replace(",", "."))
                data_dict['product_price_before'] = compare_at_price

                discount = compare_at_price - price
                discount_percentage = (discount / compare_at_price) * 100
                discount_percentage = int(round(discount_percentage))
                data_dict['product_discount'] = discount_percentage

            if brand_match:
                product_brand = brand_match.group(1)
                data_dict['product_brand'] = product_brand

            if url_match:
                product_page_url = url_match.group(1)
                data_dict['product_page_url'] = product_page_url
            else:
                data_dict['product_page_url'] = "URL not found"

            if image_match:
                product_image_url = image_match.group(1)
                data_dict['product_image_url'] = product_image_url

    return data_dict

# Function to extract product data from the script tag
def extract_product_data_two(product, meta_data):
    data_dict_two = {}

    product_id = product.get('id')
    product_id = str(product_id)
    data_dict_two["product_id"] = product_id

    variants = product.get('variants', [])

    data_dict_two['cloth_type'] = product.get('type', 'No type')

    sizes = set()
    for variant in variants:
        size = variant.get('public_title')
        if size:
            sizes.add(size.split('/')[1].strip())
    data_dict_two['sizes'] = list(sizes)

    colors = set()
    for variant in variants:
        color = variant.get('public_title')
        if color:
            colors.add(color.split('/')[0].strip())
    data_dict_two['colors'] = list(colors)

    return data_dict_two

# Function to scrape products from the category URL
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

# Function to scrape products using meta data
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

# Function to run scrap.py with arguments
def run_scraping(category, min_price, max_price, min_discount, max_discount):
    command = ['python', 'app.py', '--category', category]

    if min_price is not None:
        command.extend(['--min_price', str(min_price)])
    if max_price is not None:
        command.extend(['--max_price', str(max_price)])
    if min_discount is not None:
        command.extend(['--min_discount', str(min_discount)])
    if max_discount is not None:
        command.extend(['--max_discount', str(max_discount)])

    subprocess.run(command)

# Function to load and format JSON data
def load_data(category):
    filename = f'search.json'
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Iterate through products and format sizes and colors
    for product in data:
        product['sizes'] = '/'.join(product['sizes'])
        product['colors'] = '/'.join(product['colors'])

    return data

# Mapping dictionary for subcategory display names
subcategory_names = {
    'vestidos_monos': 'Vestidos & Monos',
    'faldas': 'Faldas',
    'camisas': 'Camisas',
    'camisetas': 'Camisetas',
    'tops': 'Tops',
    'sudaderas': 'Sudaderas',
    'brazers_chalecos': 'Brazers & Chalecos',
    'pantalones': 'Pantalones',
    'jeans': 'Jeans',
    'bermudas_shorts': 'Bermudas & Shorts',
    'chaquetas_trench': 'Chaquetas & Trenchs',
    'jerseis_cardigan': 'Jerséis y Cárdigans',
    'punto': 'Punto',
    'total_look': 'Total Look',
    'pijamas': 'Pijamas',
    'bikinis_bañadores': 'Bikinis & Bañadores',
    'athleisure': 'Athleisure',
    'sneakers': 'Sneakers',
    'sandalias': 'Sandalias',
    'zapatos_tacon': 'Zapatos de Tacón',
    'alpargatas_chanclas': 'Alpargatas & Chanclas',
    'zapatos_planos': 'Zapatos Planos',
    'bolsos_piel': 'Bolsos de Piel',
    'bolso_nylon': 'Bolsos de Nylon',
    'bandoleras': 'Bandoleras',
    'capazos': 'Capazos',
    'bolsos_rafia': 'Bolsos de Rafia',
    'bolsos_mini': 'Bolsos Mini',
    'bolsos_hombro': 'Bolsos de Hombro',
    'neceseres': 'Neceseres',
    'fundas_estuches': 'Fundas & Estuches',
    'toallas': 'Toallas',
    'gorras_sombreros': 'Gorras y Sombreros',
    'carteras': 'Carteras',
    'calcetines': 'Calcetines',
    'cinturones': 'Cinturones',
    'bisuteria': 'Bisutería',
    'llaveros': 'Llaveros',
    'gafas': 'Gafas',
    'accesorios_movil': 'Accesorios para Móvil',
    'fragancias': 'Fragancias'
}

# Streamlit app
def main():
    categories = {
        'Ropa': ['vestidos_monos', 'faldas', 'camisas', 'camisetas', 'tops', 'sudaderas', 'brazers_chalecos', 'pantalones', 'jeans', 'bermudas_shorts', 'chaquetas_trench', 'jerseis_cardigan', 'punto', 'total_look', 'pijamas', 'bikinis_bañadores', 'athleisure'],
        'Calzado': ['sneakers', 'sandalias', 'zapatos_tacon', 'alpargatas_chanclas', 'zapatos_planos'],
        'Bolsos': ['bolsos_piel', 'bolso_nylon', 'bandoleras', 'capazos', 'bolsos_rafia', 'bolsos_mini', 'bolsos_hombro', 'neceseres', 'fundas_estuches'],
        'Complementos': ['toallas', 'gorras_sombreros', 'carteras', 'calcetines', 'cinturones', 'bisuteria', 'llaveros', 'gafas', 'accesorios_movil', 'fragancias']
    }

    st.title('Scraping de productos de Scalpers')
    category = st.sidebar.selectbox('Seleccione la categoría', list(categories.keys()))

    subcategory_key = st.sidebar.selectbox('Seleccione la subcategoría', categories[category])

    skirts_url = f'https://es.scalperscompany.com/collections/{subcategory_key}'
    st.write(f'URL de la categoría seleccionada: {skirts_url}')

    min_price = st.sidebar.number_input('Precio mínimo', value=0)
    max_price = st.sidebar.number_input('Precio máximo', value=9999)
    min_discount = st.sidebar.number_input('Descuento mínimo', value=0)
    max_discount = st.sidebar.number_input('Descuento máximo', value=100)

    if st.sidebar.button('Ejecutar scraping'):
        run_scraping(subcategory_key, min_price, max_price, min_discount, max_discount)
        st.success('Scraping completado!')

    if st.sidebar.checkbox('Ver productos'):
        data = load_data(subcategory_key)
        st.write(f'Datos cargados correctamente de la subcategoría {subcategory_names.get(subcategory_key, subcategory_key)}:')
        st.write(data)

if __name__ == "__main__":
    main()

