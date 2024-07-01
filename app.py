import streamlit as st
import json

# Crear datos para el JSON
data = {'message': 'Hola Mundo!'}
file_path = './data.json'  # Ruta donde se guardará el archivo JSON

# Botón para guardar el JSON
if st.button('Guardar JSON'):
    with open(file_path, 'w') as f:
        json.dump(data, f)
    st.write(f"Archivo 'data.json' guardado en: {file_path}")

# Mostrar el contenido de data.json si existe
try:
    with open(file_path, 'r') as f:
        data = json.load(f)
        st.write("Contenido de 'data.json':")
        st.write(data)
except FileNotFoundError:
    st.write(f"No se encontró el archivo 'data.json' en {file_path}")

