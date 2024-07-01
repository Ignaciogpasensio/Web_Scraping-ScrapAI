# scrap.py
import json

def scrape_data(category):
    # Aquí iría tu lógica de scraping
    # En este ejemplo, solo creamos un diccionario de ejemplo
    data = {
        'category': category,
        'items': [
            {'name': 'Item 1', 'price': '$19.99'},
            {'name': 'Item 2', 'price': '$29.99'},
            {'name': 'Item 3', 'price': '$39.99'}
        ]
    }
    
    # Guardar los datos en un archivo JSON
    with open('find.json', 'w') as f:
        json.dump(data, f)

if __name__ == '__main__':
    import sys
    category = sys.argv[1]  # Obtener la categoría del argumento de línea de comandos
    scrape_data(category)
