import streamlit as st
import subprocess
import json
import os

def run_scraping(category, min_price, max_price, min_discount, max_discount):
    command = ['python', 'Ignaciogpasensio/Web_Scraping-ScrapAI/scrap.py', '--category', category]
    if min_price is not None:
        command.extend(['--min_price', str(min_price)])
    if max_price is not None:
        command.extend(['--max_price', str(max_price)])
    if min_discount is not None:
        command.extend(['--min_discount', str(min_discount)])
    if max_discount is not None:
        command.extend(['--max_discount', str(max_discount)])
    subprocess.run(command)

def load_data(category):
    output_file = 'search.json'  # Adjust this path as needed
    output_path = os.path.join('Web_Scraping-ScrapAI', output_file)
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        st.error(f'Error: File "{filename}" not found.')
        return []
    except Exception as e:
        st.error(f'Error loading data: {e}')
        return []
    if not isinstance(data, list) or not all(isinstance(item, dict) for item in data):
        st.error(f'Error: Invalid format in file "{filename}". Expected a list of dictionaries.')
        return []
    for product in data:
        product['sizes'] = '/'.join(product.get('sizes', []))
        product['colors'] = '/'.join(product.get('colors', []))
    return data

subcategory_names = {
    'vestidos_monos': 'Vestidos & Monos',
    'faldas': 'Faldas',
    'camisas': 'Camisas',
    'camisetas': 'Camisetas',
    'tops': 'Tops',
    'sudaderas': 'Sudaderas',
    'brazers_chalecos': 'Brazers & Chalecos',
    'pantalones': 'Pantalones',
    'jeans': 'Jeans',
    'bermudas_shorts': 'Bermudas & Shorts',
    'chaquetas_trench': 'Chaquetas & Trenchs',
    'jerseis_cardigan': 'Jerséis y Cárdigans',
    'punto': 'Punto',
    'total_look': 'Total Look',
    'pijamas': 'Pijamas',
    'bikinis_bañadores': 'Bikinis & Bañadores',
    'athleisure': 'Athleisure',
    'sneakers': 'Sneakers',
    'sandalias': 'Sandalias',
    'zapatos_tacon': 'Zapatos de Tacón',
    'alpargatas_chanclas': 'Alpargatas & Chanclas',
    'zapatos_planos': 'Zapatos Planos',
    'bolsos_piel': 'Bolsos de Piel',
    'bolso_nylon': 'Bolsos de Nylon',
    'bandoleras': 'Bandoleras',
    'capazos': 'Capazos',
    'bolsos_rafia': 'Bolsos de Rafia',
    'bolsos_mini': 'Bolsos Mini',
    'bolsos_hombro': 'Bolsos de Hombro',
    'neceseres': 'Neceseres',
    'fundas_estuches': 'Fundas & Estuches',
    'toallas': 'Toallas',
    'gorras_sombreros': 'Gorras y Sombreros',
    'carteras': 'Carteras',
    'calcetines': 'Calcetines',
    'cinturones': 'Cinturones',
    'bisuteria': 'Bisutería',
    'llaveros': 'Llaveros',
    'gafas': 'Gafas',
    'accesorios_movil': 'Accesorios para Móvil',
    'fragancias': 'Fragancias'
}

def main():
    categories = {
        'Ropa': ['vestidos_monos', 'faldas', 'camisas', 'camisetas', 'tops', 'sudaderas', 'brazers_chalecos', 'pantalones', 'jeans', 'bermudas_shorts', 'chaquetas_trench', 'jerseis_cardigan', 'punto', 'total_look', 'pijamas', 'bikinis_bañadores', 'athleisure'],
        'Calzado': ['sneakers', 'sandalias', 'zapatos_tacon', 'alpargatas_chanclas', 'zapatos_planos'],
        'Bolsos': ['bolsos_piel', 'bolso_nylon', 'bandoleras', 'capazos', 'bolsos_rafia', 'bolsos_mini', 'bolsos_hombro', 'neceseres', 'fundas_estuches'],
        'Accesorios': ['toallas', 'gorras_sombreros', 'carteras', 'calcetines', 'cinturones', 'bisuteria', 'llaveros', 'gafas', 'accesorios_movil', 'fragancias']
    }
    st.markdown("""
    <style>
    .sidebar .sidebar-content {
        background-color: white !important;
        color: black !important;
        padding: 20px; /* Adds padding inside the sidebar */
        border-right: 2px solid #ccc; /* Adds a border on the right side of the sidebar */
    }
    .sidebar select {
        background-color: white !important;
        color: black !important;
        border: 1px solid #ccc !important; /* Adjust border color and style as needed */
        border-radius: 4px;
        padding: 8px;
        font-size: 14px;
        width: 100%; /* Optional: Adjust width to fit your layout */
        box-shadow: none !important; /* Optional: Remove box shadow */
    }
    .sidebar .stButton {
        background-color: #007bff !important;
        color: white !important;
        border-color: #007bff !important;
        border-radius: 4px;
        padding: 10px 20px;
        font-weight: bold;
    }
    .sidebar .stButton:hover {
        background-color: #0056b3 !important;
        border-color: #0056b3 !important;
    }
    .title {
        font-family: 'Arial', sans-serif;
        font-size: 80px;
        font-weight: bold;
        color: #333333;
        text-align: center; /* Center align the title */
        margin-top: 0px;
        margin-bottom: 20px; /* Optional: Add some bottom margin */
    }
    .product-container {
        position: relative;
        display: inline-block;
        width: 100%;
        margin-bottom: 20px; /* Adjust spacing between products */
    }
    .product-container img {
        width: 100%;
        height: auto;
        transition: transform 0.2s, opacity 0.2s;
        position: relative; /* Ensure discount text is positioned relative to the image */
    }
    .product-container:hover img {
        transform: scale(1.05);
        opacity: 0.8;
    }
    .discount-text {
        position: absolute;
        top: 50%; /* Center discount text vertically */
        left: 50%; /* Center discount text horizontally */
        transform: translate(-50%, -50%); /* Adjust for centering */
        color: black; /* Text color */
        font-size: 4em; /* Double size: 2em was previous size */
        font-weight: bold;
        z-index: 1;
    }
    .tooltip {
        position: relative;
        display: inline-block;
        z-index: 0; /* Ensure tooltips are behind the discount text */
    }
    .tooltip .tooltiptext {
        visibility: hidden;
        width: 200px;
        background-color: black;
        color: white;
        font-size: 1em;
        text-align: center;
        padding: 5px 0;
        border-radius: 6px;
        position: absolute;
        z-index: 2; /* Ensure tooltips are above other elements */
        bottom: 125%;
        left: 50%;
        margin-left: -100px;
        opacity: 0;
        transition: opacity 0.3s;
        pointer-events: none; /* Ensure tooltip does not interfere with mouse events */
    }
    .tooltip:hover .tooltiptext {
        visibility: visible;
        opacity: 1;
    }
    .tooltip .tooltiptext .smaller-text {
        font-size: 0.7em; /* Adjust the font size smaller */
        line-height: 1.5; /* Adjust the line height */
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown(
        """
        <script>
        document.addEventListener('DOMContentLoaded', function() {
            const tooltips = document.querySelectorAll('.tooltip');
            
            tooltips.forEach(tooltip => {
                const tooltipText = tooltip.querySelector('.tooltiptext');
                const rect = tooltip.getBoundingClientRect();
                
                if (rect.top < 0) {
                    tooltipText.style.top = '100%';
                }
            });
        });
        </script>
        """,
        unsafe_allow_html=True
    )

    main_category = st.sidebar.selectbox('Selecciona la Categoría', list(categories.keys()))
    subcategory = st.sidebar.selectbox(f'¿Qué gama de {main_category} desea?', categories[main_category])
    price_range = st.sidebar.slider('Seleccione el rango de precios que está dispuesto a pagar', min_value=0.0, max_value=2000.0, value=(0.0, 2000.0), step=1.0)
    min_price = price_range[0]
    max_price = price_range[1]
    discount_range = st.sidebar.slider('Seleccione el rango de descuento que le interesa', min_value=0, max_value=100, value=(0, 100), step=1)
    min_discount = discount_range[0]
    max_discount = discount_range[1]
    st.markdown('<p class="title">ScrapAI</p>', unsafe_allow_html=True)
    if st.sidebar.button('SCRAPE'):
        with st.spinner('Bichendo ofertas...'):
            run_scraping(subcategory, min_price, max_price, min_discount, max_discount)
    if st.sidebar.checkbox('Mostrar productos'):
        st.subheader(f'{subcategory_names[subcategory]}')
        data = load_data(subcategory)
        cols = st.columns(3)
        for index, product in enumerate(data):
            discount_text = f"-{product['product_discount']}%"
            image_url = product['product_image_url']
            product_page_url = product['product_page_url']
            product_name = product['product_name']
            product_brand = product['product_brand']
            cloth_type = product['cloth_type']
            product_price_before = product['product_price_before']
            product_price_after = product['product_price_after']
            product_id = product['product_id']
            sizes = product['sizes']
            colors = product['colors']
            if min_price <= product_price_after <= max_price and min_discount <= product['product_discount'] <= max_discount:
               cols[index % 3].markdown(f"""
                <a href="{product_page_url}" target="_blank" style="text-decoration: none; color: inherit;">
                    <div class="product-container">
                        <div class="tooltip">
                            <img src="{image_url}" alt="{product_name}"/>
                            <span class="discount-text">
                                {discount_text}
                            </span>
                            <span class="tooltiptext">
                                <strong>{product_name}</strong><br>
                                <s>{product_price_before}€</s><br>
                                <strong>{product_price_after}€</strong><br>
                                <div class="smaller-text">Brand: {product_brand}<br>
                                Sizes: {sizes}<br>
                                Colors: {colors}<br>
                                ID: {product_id}</div>
                            </span>
                        </div>
                    </div>
                </a>
                """, unsafe_allow_html=True)

if __name__ == '__main__':
    main()
