# app.py

import streamlit as st
import json
import subprocess

def run_find_script(category):
    # Run the find.py script with the selected category
    result = subprocess.run(['python3', 'scrap.py', category], capture_output=True, text=True)
    if result.returncode != 0:
        st.error("Error running find.py script")
        st.stop()

def display_results():
    try:
        with open('find.json', 'r') as f:
            data = json.load(f)
            st.write(data)
    except FileNotFoundError:
        st.error("find.json not found. Please run the find.py script first.")

# Streamlit app
st.title('Scalpers Category Finder')

category = st.selectbox('Select a category:', ['jeans', 'shirts'])

if st.button('Find'):
    run_find_script(category)
    st.success(f"Results for {category} have been saved to find.json")
    display_results()
