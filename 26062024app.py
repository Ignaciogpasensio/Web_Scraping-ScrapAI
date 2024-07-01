import streamlit as st
import json
import subprocess

# Function to run scrap.py with specified arguments
def run_scraper(category, min_price, max_price):
    process = subprocess.Popen(['python', 'scrap.py', '--category', category, '--min_price', str(min_price), '--max_price', str(max_price)])
    process.wait()

# Function to load scraped data from JSON file
def load_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def main():
    st.title('Scalpers Product Scraper and Viewer')

    # Sidebar for user input
    st.sidebar.title('Scrape Settings')
    category = st.sidebar.selectbox('Select Category', ['faldas', 'favoritos', 'vestidos_monos', 'sneakers', 'bolsos', 'toallas'])
    min_price = st.sidebar.number_input('Minimum Price', min_value=0.0, step=1.0)
    max_price = st.sidebar.number_input('Maximum Price', min_value=0.0, step=1.0)

    if st.sidebar.button('Scrape Products'):
        # Run the scraper with selected options
        run_scraper(category, min_price, max_price)
        st.success(f'Scraping complete for category: {category}')

    # Display scraped products
    data_file = 'search.json'  # Update with your JSON file path
    try:
        products_data = load_data(data_file)
        # Display each product with its image
        for product in products_data:
            # Handle price data
            price_value = product['price']
            if isinstance(price_value, (int, float)):
                price_str = f'{price_value:.2f}'  # Format as string with two decimals
            elif isinstance(price_value, str):
                price_str = price_value.replace('£', '').replace(',', '').strip()
            else:
                price_str = 'Price not available'

            # Convert price string to float (if possible)
            try:
                price = float(price_str)
            except ValueError:
                price = 0.0

            # Filter products based on price range
            if min_price <= price <= max_price:
                st.subheader(product['product_name'])
                st.image(f"https:{product['images'][0]}", caption=product['product_name'], use_column_width=True)
                st.write(f"Price: {price_str}€")
                st.write(f"Category: {product['cloth_type']}")
                st.write(f"Link: [Product Link]({product['product_url']})")
    except FileNotFoundError:
        st.error(f"No data file found. Please scrape products first.")
    except json.JSONDecodeError:
        st.error(f"Error decoding the JSON data. Please check the data file format.")

if __name__ == "__main__":
    main()
