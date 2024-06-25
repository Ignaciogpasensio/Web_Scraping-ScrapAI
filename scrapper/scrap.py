import requests
from bs4 import BeautifulSoup
import json
from schema.product import ClothUnit
import argparse

# URL base del sitio web de Scalpers
base_url = 'https://en.gb.scalperscompany.com'
skirts_url = f'{base_url}/collections/woman-new-collection-skirts-2060'

def scrape_skirts():
    # Lista para almacenar los datos de todas las faldas
    skirts_data = []

    # Realizar la solicitud GET a la URL de las faldas
    response = requests.get(skirts_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Encontrar todos los productos de la colección de faldas
        products = soup.find_all('div', class_='ProductItem__Info')

        for product in products:
            # Obtener el nombre del producto
            product_name = product.find('h2', class_='ProductItem__Title').text.strip()

            # Construir la URL completa del producto
            product_url = base_url + product.find('a', class_='ProductItem__ImageWrapper')['href']

            # Obtener el SKU del producto desde los metadatos (si está disponible)
            sku = product.find('span', class_='ProductItem__Sku').text.strip()

            # Obtener el precio del producto
            price = product.find('span', class_='ProductItem__Price').text.strip()

            # Crear una lista vacía para las imágenes
            images = []

            # Obtener todas las imágenes del producto
            product_images = product.find_all('img', class_='ProductItem__Image')
            for img in product_images:
                if img.has_attr('data-src'):
                    images.append(base_url + img['data-src'])

            # Crear un diccionario con los datos del producto
            product_data = {
                'product_name': product_name,
                'product_url': product_url,
                'sku': sku,
                'price': price,
                'images': images,
                'sizes': [],  # Agregar tamaños si se encuentran en la página
                'metadata': []  # Agregar metadatos relevantes si se encuentran en la página
            }

            # Agregar los datos del producto a la lista de faldas
            skirts_data.append(product_data)

    else:
        print(f'Failed to fetch skirts page. Status code: {response.status_code}')

    return skirts_data

def main():
    parser = argparse.ArgumentParser(description='Scrape skirts data from Scalpers website.')
    parser.add_argument('--type', choices=['skirts'], help='Type of clothing to scrape', required=True)
    args = parser.parse_args()

    if args.type == 'skirts':
        skirts_data = scrape_skirts()

        # Imprimir los datos de las faldas en formato JSON
        print(json.dumps(skirts_data, indent=2))

if __name__ == "__main__":
    main()
