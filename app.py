import streamlit as st
import subprocess
import json
import os

# Título y selección de categoría
st.title('Aplicación de Selección de Categoría')
category = st.selectbox('Selecciona una categoría', ['jeans', 'shirts'])

# Botón para llamar a scrap.py
if st.button('Find'):
    # Llamada a scrap.py
    st.write(f"Ejecutando scrap.py para la categoría: {category}")
    
    # Ejecutar scrap.py y obtener el path del archivo creado
    result = subprocess.run(['python', 'scrap.py', category], capture_output=True, text=True)
    file_path = result.stdout.strip()  # Obtener el path del archivo creado
    
    # Mostrar el path en Streamlit
    st.write(f"Intentando leer 'find.json' desde: {file_path}")
    
    # Mostrar contenido de find.json si existe
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
            st.write("Contenido de 'find.json':")
            st.write(data)
    except FileNotFoundError:
        st.write(f"No se encontró el archivo 'find.json' en {file_path}")
