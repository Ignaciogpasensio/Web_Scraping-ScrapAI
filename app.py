import streamlit as st
import json

# Título de la aplicación
st.title('Generador de Archivo JSON')

# Datos para el archivo JSON
data = {
    "nombre": "Juan",
    "edad": 30,
    "ciudad": "Madrid"
}

# Botón para guardar el JSON
if st.button('Guardar JSON'):
    # Guardar el archivo JSON
    with open('data.json', 'w') as f:
        json.dump(data, f, indent=4)
    
    # Mostrar mensaje de éxito
    st.success("Archivo 'data.json' guardado correctamente en el directorio del repositorio.")

    # Mostrar contenido del archivo guardado
    st.write("Contenido del archivo guardado:")
    st.write(data)
