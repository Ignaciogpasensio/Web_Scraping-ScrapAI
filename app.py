import streamlit as st
import requests
from bs4 import BeautifulSoup
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
                continue

    return products_data

def main():
    st.title("Scalpers Product Scraper")

    category_options = [
        'vestidos_monos', 'faldas', 'camisas', 'camisetas', 'tops', 'sudaderas',
        'brazers_chalecos', 'pantalones', 'jeans', 'bermudas_shorts', 'chaquetas_trench',
        'jerseis_cardigan', 'punto', 'total_look', 'pijamas', 'bikinis_bañadores',
        'athleisure', 'sneakers', 'sandalias', 'zapatos_tacon', 'alpargatas_chanclas',
        'zapatos_planos', 'bolsos_piel', 'bolso_nylon', 'bandoleras', 'capazos',
        'bolsos_rafia', 'bolsos_mini', 'bolsos_hombro', 'neceseres', 'fundas_estuches',
        'toallas', 'gorras_sombreros', 'carteras', 'joyas', 'bufandas_fulares',
        'cinturones', 'gafas', 'perfumeria', 'libros', 'novedades', 'outlet'
    ]

    selected_category = st.selectbox("Select a product category", category_options)

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
        'carteras': '/collections/mujer-nueva-coleccion-accesorios-carteras-2017',
        'joyas': '/collections/mujer-nueva-coleccion-accesorios-bisuteria-y-joyeria-2014',
        'bufandas_fulares': '/collections/mujer-nueva-coleccion-accesorios-bufandas-y-fulares-2016',
        'cinturones': '/collections/mujer-nueva-coleccion-accesorios-cinturones-2013',
        'gafas': '/collections/mujer-nueva-coleccion-accesorios-gafas-de-sol-2015',
        'perfumeria': '/collections/mujer-nueva-coleccion-perfumeria-2069',
        'libros': '/collections/mujer-nueva-coleccion-libros-2595',
        'novedades': '/collections/novedades-mujer-100001',
        'outlet': '/collections/mujer-liquidacion-2134'
    }

    category_url = base_url + category_map[selected_category]
    products_data = scrape_products(category_url)

    for product in products_data:
        st.markdown(f"## {product['product_name']}")
        st.image(product['product_image_url'], caption=product['product_name'], use_column_width=True)
        st.write(f"**Brand:** {product['product_brand']}")
        st.write(f"**Current Price:** €{product['product_price_after']}")
        st.write(f"**Previous Price:** €{product['product_price_before']}")
        st.write(f"**Discount:** {product['product_discount']}%")
        st.write(f"**Product Page URL:** [{product['product_page_url']}]({product['product_page_url']})")
        st.write("---")

if __name__ == '__main__':
    main()

