import json
import os

def main(category):
    # Supongamos que se realiza alguna operación para obtener datos
    data = {"category": category, "quantity": 10}  # Datos de ejemplo
    
    # Obtener la ruta del repositorio
    repo_path = os.getenv('GITHUB_WORKSPACE', default='/Ignaciogpasensio/Web_Scraping-ScrapAI/')
    
    # Guardar datos en find.json en la ruta del repositorio
    file_path = os.path.join(repo_path, 'find.json')
    with open(file_path, 'w') as f:
        json.dump(data, f)

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Debe proporcionar una categoría como argumento.")
        sys.exit(1)
    category = sys.argv[1]
    main(category)
