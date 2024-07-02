import requests
from bs4 import BeautifulSoup
import json
import argparse
import re
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
def scrape_products(category_url):
    products_data = []
    response = requests.get(category_url)

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
                print(f'Error scraping product: {e}')
                continue

    return products_data

def scrape_products_two(category_url):
    products_data_two = []
    response = requests.get(category_url)

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
                        print(f'Error extracting product data: {e}')
                        continue

    return products_data_two
st.markdown("""
<style>
.sidebar .sidebar-content {
    background-color: white !important;
    color: black !important;
    padding: 20px;
    border-right: 2px solid #ccc;
}

.sidebar select {
    background-color: white !important;
    color: black !important;
    border: 1px solid #ccc !important;
    border-radius: 4px;
    padding: 8px;
    font-size: 14px;
    width: 100%;
    box-shadow: none !important;
}

.sidebar .stButton {
    background-color: #007bff !important;
    color: white !important;
    border-color: #007bff !important;
    border-radius: 4px;
    padding: 10px 20px;
    font-weight: bold;
}

.sidebar .stButton:hover {
    background-color: #0056b3 !important;
    border-color: #0056b3 !important;
}

.title {
    font-family: 'Arial', sans-serif;
    font-size: 80px;
    font-weight: bold;
    color: #333333;
    text-align: center;
    margin-top: 0px;
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)
def main():
    categories = {
        'Ropa': ['vestidos_monos', 'faldas', 'camisas', 'camisetas', 'tops', 'sudaderas', 'brazers_chalecos', 'pantalones', 'jeans', 'bermudas_shorts', 'chaquetas_trench', 'jerseis_cardigan', 'punto', 'total_look', 'pijamas', 'bikinis_bañadores', 'athleisure'],
        'Calzado': ['sneakers', 'sandalias', 'zapatos_tacon', 'alpargatas_chanclas', 'zapatos_planos'],
        'Bolsos': ['bolsos_piel', 'bolso_nylon', 'bandoleras', 'capazos', 'bolsos_rafia', 'bolsos_mini', 'bolsos_hombro', 'neceseres', 'fundas_estuches'],
        'Accesorios': ['toallas', 'gorras_sombreros', 'carteras', 'calcetines', 'cinturones', 'bisuteria', 'llaveros', 'gafas', 'accesorios_movil', 'fragancias']
    }

    # Tu código existente para la barra lateral, controles y carga de datos

    # Custom title with font style and center alignment
    st.markdown('<p class="title">ScrapAI</p>', unsafe_allow_html=True)

    if st.sidebar.button('SCRAPE'):
        with st.spinner('Bichendo ofertas...'):
            run_scraping(subcategory, min_price, max_price, min_discount, max_discount)

    # Display scraped product data
    if st.sidebar.checkbox('Mostrar productos'):
        st.subheader(f'{subcategory_names[subcategory]}')
        data = load_data(subcategory)

        # Create columns for product display
        cols = st.columns(5)
        for index, product in enumerate(data):
            discount_text = f"-{product['product_discount']}%"
            image_url = product['product_image_url']
            product_page_url = product['product_page_url']
            product_name = product['product_name']
            product_brand = product['product_brand']
            cloth_type = product['cloth_type']
            product_price_before = product['product_price_before']
            product_price_after = product['product_price_after']
            product_id = product['product_id']

            cols[index % 5].image(image_url, caption=f"{discount_text} de {product_price_after} €.", use_column_width=True)
            cols[index % 5].write(f"{product_name} {product_brand} de {product_price_before} €..")

if __name__ == '__main__':
    main()
