import requests
from bs4 import BeautifulSoup
import json
import argparse
import re
import os

base_url = 'https://es.scalperscompany.com'
repo_path = 'Ignaciogpasensio/Web_Scraping-ScrapAI'

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

def main(args):
    category_map = {
        'vestidos_monos': '/collections/mujer-nueva-coleccion-ropa-vestidos-y-monos-2086',
        'faldas': '/collections/mujer-nueva-coleccion-ropa-faldas-2060',
        'camisas': '/collections/mujer-nueva-coleccion-ropa-camisas-y-blusas-2048',
        'camisetas': '/collections/mujer-nueva-coleccion-ropa-camisetas-y-tops-2054',
        'tops': '/collections/mujer-nueva-coleccion-ropa-tops-2135',
        'sudaderas': '/collections/mujer-nueva-coleccion-ropa-sudaderas-2082',
        'brazers_chalecos': '/collections/mujer-nueva-coleccion-ropa-americanas-2038',
        'pantalones': '/collections/mujer-nueva-coleccion-ropa-pantalones-2072',
        'jeans': '/collections/mujer-nueva-coleccion-ropa-pantalones-vaqueros-2078',
        'bermudas_shorts': '/collections/mujer-nueva-coleccion-ropa-bermudas-shorts-2047',
        'chaquetas_trench': '/collections/mujer-nueva-coleccion-ropa-abrigos-y-chaquetas-2034',
        'jerseis_cardigan': '/collections/mujer-nueva-coleccion-ropa-jerseis-y-cardigans-2067',
        'punto': '/collections/mujer-nueva-coleccion-ropa-punto-2141',
        'total_look': '/collections/mujer-total-look-2120',
        'pijamas': '/collections/mujer-nueva-coleccion-ropa-pijamas-2081',
        'bikinis_bañadores': '/collections/mujer-nueva-coleccion-ropa-banadores-y-bikinis-2042',
        'athleisure': '/collections/mujer-adrenaline-ropa-deportiva-2098',
        'sneakers': '/collections/mujer-nueva-coleccion-calzado-sneakers-2029',
        'sandalias': '/collections/mujer-nueva-coleccion-calzado-sandalias-2028',
        'zapatos_tacon': '/collections/mujer-nueva-coleccion-calzado-zapatos-tacon-2031',
        'alpargatas_chanclas': '/collections/mujer-nueva-coleccion-calzado-alpargatas-2032',
        'zapatos_planos': '/collections/mujer-nueva-coleccion-calzado-zapatos-planos-2030',
        'bolsos_piel': '/collections/mujer-nueva-coleccion-accesorios-bolsos-y-marroquineria-piel-2012',
        'bolso_nylon': '/collections/mujer-nueva-coleccion-accesorios-bolsos-y-marroquineria-nylon-2124',
        'bandoleras': '/collections/mujer-nueva-coleccion-accesorios-bolsos-y-marroquineria-bandoleras-2006',
        'capazos': '/collections/mujer-nueva-coleccion-accesorios-bolsos-y-marroquineria-capazo-2008',
        'bolsos_rafia': '/collections/mujer-nueva-coleccion-accesorios-bolsos-y-marroquineria-rafia-2131',
        'bolsos_mini': '/collections/mujer-nueva-coleccion-accesorios-bolsos-y-marroquineria-mini-2125',
        'bolsos_hombro': '/collections/mujer-nueva-coleccion-bolsos-hombro',
        'neceseres': '/collections/mujer-nueva-coleccion-accesorios-bolsos-y-marroquineria-neceser-2011',
        'fundas_estuches': '/collections/mujer-nueva-coleccion-fundas',
        'toallas': '/collections/mujer-nueva-coleccion-accesorios-toallas-2606',
        'gorras_sombreros': '/collections/mujer-nueva-coleccion-accesorios-gorros-y-guantes-2018',
        'carteras': '/collections/mujer-nueva-coleccion-accesorios-gorros-y-guantes-2018',
        'calcetines': '/collections/mujer-nueva-coleccion-accesorios-calcetines-2014',
        'cinturones': '/collections/mujer-nueva-coleccion-accesorios-cinturones-2015',
        'bisuteria': '/collections/mujer-nueva-coleccion-accesorios-bisuteria-2005',
        'llaveros': '/collections/mujer-nueva-coleccion-accesorios-llaveros-2628',
        'gafas': '/collections/mujer-nueva-coleccion-accesorios-gafas-2017',
        'accesorios_movil': '/collections/nueva-coleccion-accesorios-accesorios-movil-0007',
        'fragancias': '/collections/mujer-nueva-coleccion-accesorios-fragancias-2016'
    }
    if args.category in category_map:
        category_url = base_url + category_map[args.category]
        products_data = scrape_products(category_url)
        products_data_two = scrape_products_two(category_url)
        products_data_dict = {product['product_id']: product for product in products_data}
        for product_two in products_data_two:
            if 'colors' in product_two and 'sizes' in product_two:
                product_id = product_two['product_id']
                if product_id in products_data_dict:
                    products_data_dict[product_id].update(product_two)
        min_price = args.min_price
        max_price = args.max_price
        if min_price is not None and max_price is not None:
            filtered_products_data = []
            for product in products_data_dict.values():
                if 'product_price_after' in product:
                    price_after = product['product_price_after']
                    if min_price <= price_after <= max_price:
                        filtered_products_data.append(product)
            products_data = filtered_products_data
        min_discount = args.min_discount
        max_discount = args.max_discount
        if min_discount is not None and max_discount is not None:
            filtered_products_data = []
            for product in products_data:
                if 'product_discount' in product:
                    discount = product['product_discount']
                    if min_discount <= discount <= max_discount:
                        filtered_products_data.append(product)
            products_data = filtered_products_data
        filtered_products_data = [product for product in products_data if 'colors' in product]

        output_file = 'search.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(filtered_products_data, f, ensure_ascii=False, indent=2)
        print(f'Successfully scraped {len(filtered_products_data)} products from category "{args.category}" in the price range {min_price}€ - {max_price}€ and discount range {min_discount}% - {max_discount}%. Data saved to {output_file}')
        try:
            os.chdir('Ignaciogpasensio/Web_Scraping-ScrapAI')  # Change directory to your repository
            subprocess.run(['git', 'pull'])  # Pull latest changes (if any)
            subprocess.run(['git', 'add', 'search.json'])
            subprocess.run(['git', 'commit', '-m', 'Update search.json'])
            subprocess.run(['git', 'push'])
            print("Successfully pushed changes to GitHub.")
    else:
        print(f'Invalid category "{args.category}". Please choose one of: faldas, vestidos_monos, sneakers, bolsos, toallas.')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Scrape product data from Scalpers website.')
    parser.add_argument('--category', choices=['vestidos_monos','faldas','camisas','camisetas','tops','sudaderas','brazers_chalecos','pantalones','jeans','bermudas_shorts',
                                               'chaquetas_trench','jerseis_cardigan','punto','total_look','pijamas','bikinis_bañadores','athleisure','sneakers',
                                               'sandalias','zapatos_tacon','alpargatas_chanclas','zapatos_planos','bolsos_piel','bolso_nylon','bandoleras','capazos'
                                               'bolsos_rafia','bolsos_mini','bolsos_hombro','neceseres','fundas_estuches','toallas','gorras_sombreros','carteras',
                                               'calcetines','cinturones','bisuteria','llaveros','gafas','accesorios_movil','fragancias'],
                        help='Category of products to scrape', required=True)
    parser.add_argument('--min_price', type=float, help='Minimum price filter')
    parser.add_argument('--max_price', type=float, help='Maximum price filter')
    parser.add_argument('--min_discount', type=int, help='Minimum discount filter')
    parser.add_argument('--max_discount', type=int, help='Maximum discount filter')
    args = parser.parse_args()
    main(args)
