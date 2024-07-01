import streamlit as st
import json

# Título y botón en la aplicación Streamlit
st.title('Guardar JSON en Repositorio de GitHub')
if st.button('Guardar JSON'):
    # Datos de ejemplo
    data = {'nombre': 'Juan', 'edad': 30}

    # Guardar el archivo JSON en el mismo directorio
    file_path = './data.json'
    with open(file_path, 'w') as f:
        json.dump(data, f)

    st.write(f"Archivo 'data.json' guardado en: {file_path}")
