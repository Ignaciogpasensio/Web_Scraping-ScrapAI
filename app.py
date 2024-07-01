import streamlit as st
import json
import os

# Título y selección de nombre para el archivo JSON
st.title('Aplicación para Guardar JSON en Repositorio')
json_name = st.text_input('Nombre del archivo JSON (sin la extensión .json):')

# Botón para guardar el JSON
if st.button('Guardar JSON'):
    data = {"message": "Hola, este es un JSON de ejemplo."}  # Datos de ejemplo
    
    # Obtener el directorio del repositorio
    repo_path = os.getenv('GITHUB_WORKSPACE', '/Ignaciogpasensio/Web_Scraping-ScrapAI/')
    
    # Guardar el archivo JSON en el directorio del repositorio
    file_path = os.path.join(repo_path, f'{json_name}.json')
    with open(file_path, 'w') as f:
        json.dump(data, f)
    
    st.success(f'Archivo {json_name}.json guardado en el repositorio.')
