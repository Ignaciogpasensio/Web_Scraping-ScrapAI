import streamlit as st
import subprocess
import json

# Función para ejecutar scrap.py con argumentos
def run_scraping(category, min_price, max_price, min_discount, max_discount):
    command = ['python', 'scrap.py', '--category', category]

    if min_price is not None:
        command.extend(['--min_price', str(min_price)])
    if max_price is not None:
        command.extend(['--max_price', str(max_price)])
    if min_discount is not None:
        command.extend(['--min_discount', str(min_discount)])
    if max_discount is not None:
        command.extend(['--max_discount', str(max_discount)])

    subprocess.run(command)

# Función para cargar y formatear datos JSON
def load_data(category):
    filename = f'search.json'
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Iterar a través de los productos y formatear tamaños y colores
    for product in data:
        product['sizes'] = '/'.join(product['sizes'])
        product['colors'] = '/'.join(product['colors'])

    return data

# Diccionario de mapeo para nombres de subcategoría
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

# Aplicación Streamlit
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
        padding: 20px; /* Añade padding dentro de la barra lateral */
        border-right: 2px solid #ccc; /* Añade un borde en el lado derecho de la barra lateral */
    }
    .sidebar select {
        background-color: white !important;
        color: black !important;
        border: 1px solid #ccc !important; /* Ajusta el color y estilo del borde según sea necesario */
        border-radius: 4px;
        padding: 8px;
        font-size: 14px;
        width: 100%; /* Opcional: Ajusta el ancho para que se ajuste a tu diseño */
        box-shadow: none !important; /* Opcional: Elimina la sombra */
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
    .title-container {
        background-image: url('https://i.pinimg.com/736x/c0/51/e0/c051e01026300529d49ce029aef829dc.jpg'); /* URL de tu imagen de fondo */
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        text-align: center;
        padding: 100px 0; /* Ajusta el espacio alrededor del título */
    }
    .title {
        font-family: 'Arial', sans-serif;
        font-size: 80px;
        font-weight: bold;
        color: white;
        text-align: center; /* Centra el título */
        margin-top: 0px;
        margin-bottom: 20px; /* Opcional: Añade un margen inferior */
    }
    .product-container {
        position: relative;
        display: inline-block;
        width: 100%;
        margin-bottom: 20px; /* Ajusta el espacio entre productos */
    }
    .product-container img {
        width: 100%;
        height: auto;
        transition: transform 0.2s, opacity 0.2s;
        position: relative; /* Asegura que el texto de descuento esté posicionado relativo a la imagen */
    }
    .product-container:hover img {
        transform: scale(1.05);
        opacity: 0.8;
    }
    .discount-text {
        position: absolute;
        top: 50%; /* Centra verticalmente el texto de descuento */
        left: 50%; /* Centra horizontalmente el texto de descuento */
        transform: translate(-50%, -50%); /* Ajusta para centrar */
        color: black; /* Color del texto */
        font-size: 4em; /* Doble tamaño: 2em era el tamaño anterior */
        font-weight: bold;
        z-index: 1;
    }
    .tooltip {
        position: relative;
        display: inline-block;
        z-index: 0; /* Asegura que los tooltips estén detrás del texto de descuento */
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
        z-index: 2; /* Asegura que los tooltips estén por encima de otros elementos */
        bottom: 125%;
        left: 50%;
        margin-left: -100px;
        opacity: 0;
        transition: opacity 0.3s;
        pointer-events: none; /* Asegura que el tooltip no interfiera con los eventos del mouse */
    }
    .tooltip:hover .tooltiptext {
        visibility: visible;
        opacity: 1;
    }
    .tooltip .tooltiptext .smaller-text {
        font-size: 0.7em; /* Ajusta el tamaño de la fuente a más pequeño */
        line-height: 1.5; /* Ajusta la altura de línea */
    }
    </style>
    """, unsafe_allow_html=True)

    # JavaScript para ajustar la posición del tooltip dinámicamente
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

    # Barra lateral - Selección de categoría principal
    main_category = st.sidebar.selectbox('Selecciona la Categoría', list(categories.keys()))

    # Barra lateral - Selección de subcategoría basada en la categoría principal
    subcategory = st.sidebar.selectbox(f'¿Qué gama de {main_category} desea?', categories[main_category])

    # Slider de rango de precios
    price_range = st.sidebar.slider('Seleccione el rango de precios que está dispuesto a pagar', min_value=0.0, max_value=2000.0, value=(0.0, 2000.0), step=1.0)
    min_price = price_range[0]
    max_price = price_range[1]

    # Slider de rango de descuento
    discount_range = st.sidebar.slider('Seleccione el rango de descuento que le interesa', min_value=0, max_value=100, value=(0, 100), step=1)
    min_discount = discount_range[0]
    max_discount = discount_range[1]

    # Título personalizado con estilo de fuente y alineación central
    st.markdown('<div class="title-container"><p class="title">ScrapAI</p></div>', unsafe_allow_html=True)

    if st.sidebar.button('SCRAPE'):
        with st.spinner('Buscando ofertas...'):
            run_scraping(subcategory, min_price, max_price, min_discount, max_discount)

    # Mostrar datos de productos raspados
    if st.sidebar.checkbox('Mostrar productos'):
        st.subheader(f'{subcategory_names[subcategory]}')
        data = load_data(subcategory)

        # Crear columnas para mostrar productos
        cols = st.columns(6)
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

            # Filtrar productos según el rango de precio y descuento
            if min_price <= product_price_after <= max_price and min_discount <= product['product_discount'] <= max_discount:
                cols[index % 6].markdown(f"""
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
                                <div class="smaller-text">Marca: {product_brand}<br>
                                Tallas: {sizes}<br>
                                Colores: {colors}<br>
                                ID: {product_id}</div>
                            </span>
                        </div>
                    </div>
                </a>
                """, unsafe_allow_html=True)

if __name__ == '__main__':
    main()
