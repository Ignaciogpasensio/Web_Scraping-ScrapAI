import streamlit as st
import json
import subprocess

# Crear datos para el JSON
data = {'message': 'Hola Mundo!'}
file_path = './data.json'  # Ruta donde se guardará el archivo JSON localmente

# Botón para guardar el JSON
if st.button('Guardar JSON'):
    with open(file_path, 'w') as f:
        json.dump(data, f)
    st.write(f"Archivo 'data.json' guardado localmente en: {file_path}")

    # Commit y push a GitHub
    result = subprocess.run(['git', 'add', file_path], capture_output=True, text=True)
    if result.returncode == 0:
        commit_message = 'Añadir data.json desde Streamlit'
        result = subprocess.run(['git', 'commit', '-m', commit_message], capture_output=True, text=True)
        if result.returncode == 0:
            result = subprocess.run(['git', 'push'], capture_output=True, text=True)
            if result.returncode == 0:
                st.write(f"Archivo 'data.json' guardado en GitHub en: https://raw.githubusercontent.com/Ignaciogpasensio/Web_Scraping-ScrapAI/main/search.json")
            else:
                st.error(f"No se pudo hacer push a GitHub: {result.stderr.strip()}")
        else:
            st.error(f"No se pudo hacer commit: {result.stderr.strip()}")
    else:
        st.error(f"No se pudo añadir el archivo a Git: {result.stderr.strip()}")

# Mostrar el contenido de data.json si existe
try:
    with open(file_path, 'r') as f:
        data = json.load(f)
        st.write("Contenido de 'data.json':")
        st.write(data)
except FileNotFoundError:
    st.write(f"No se encontró el archivo 'data.json' en {file_path}")
