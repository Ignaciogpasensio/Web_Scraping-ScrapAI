# En scrap.py
import json
import os

def scrape_data(category):
    # Aquí va la lógica para obtener 'data'
    data = {
        'category': category,
        'items': [
            {'name': 'Item 1', 'price': '$19.99'},
            {'name': 'Item 2', 'price': '$29.99'},
            {'name': 'Item 3', 'price': '$39.99'}
        ]
    }

    # Obtener el directorio actual
    current_directory = os.getcwd()

    # Guardar los datos en un archivo JSON
    file_path = os.path.join(current_directory, 'find.json')
    with open(file_path, 'w') as f:
        json.dump(data, f)

    return file_path  # Devolver el path del archivo creado

if __name__ == '__main__':
    import sys
    category = sys.argv[1]  # Obtener la categoría del argumento de línea de comandos
    created_file_path = scrape_data(category)
    print(f"Archivo 'find.json' creado en: {created_file_path}")
