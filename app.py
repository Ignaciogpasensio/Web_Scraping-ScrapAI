import streamlit as st
import json
import subprocess

def run_scrap_script(category):
    # Run the scrap.py script with the selected category
    result = subprocess.run(['python3', 'scrap.py', category], capture_output=True, text=True)
    if result.returncode != 0:
        st.error(f"Error running scrap.py script: {result.stderr}")
        st.stop()

def display_results():
    try:
        with open('find.json', 'r') as f:
            data = json.load(f)
            st.write(data)
    except FileNotFoundError:
        st.error("find.json not found. Please run the scrap.py script first.")

# Streamlit app
st.title('Scalpers Category Finder')

category = st.selectbox('Select a category:', ['jeans', 'shirts'])

if st.button('Find'):
    run_scrap_script(category)
    st.success(f"Results for {category} have been saved to find.json")
    display_results()
