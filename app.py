# app.py
import streamlit as st
import subprocess
import json

def main():
    st.title('Web Scraping App')
    
    # Lista de categorías disponibles
    categories = ['jeans', 'shirts']
    
    # Selección de categoría por el usuario
    category = st.selectbox('Select a category', categories)
    
    if st.button('Find'):
        # Llamar a scrap.py usando subprocess
        result = subprocess.run(['python', 'scrap.py', category], capture_output=True, text=True)
        
        if result.returncode == 0:
            st.success('Data scraped successfully!')
            
            # Leer el JSON creado por scrap.py
            with open('find.json', 'r') as f:
                data = json.load(f)
                
            # Mostrar los datos al usuario
            st.json(data)
        else:
            st.error(f'Error running scrap.py: {result.stderr}')

if __name__ == '__main__':
    main()
