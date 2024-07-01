import streamlit as st
import json

# Título y botón en la aplicación Streamlit
st.title('Guardar JSON en Repositorio de GitHub')
if st.button('Guardar JSON'):
    # Datos de ejemplo
    data = {'nombre': 'Juan', 'edad': 30}

    # Guardar el archivo JSON en una ruta relativa
    file_path = './data.json'
    try:
        with open(file_path, 'w') as f:
            json.dump(data, f)
        st.write(f"Archivo 'data.json' guardado en: {file_path}")
    except FileNotFoundError:
        st.write(f"Error: No se pudo encontrar el directorio o archivo en la ruta: {file_path}")
    except PermissionError:
        st.write(f"Error: Permiso denegado para escribir en la ruta: {file_path}")
    except Exception as e:
        st.write(f"Error desconocido: {str(e)}")
