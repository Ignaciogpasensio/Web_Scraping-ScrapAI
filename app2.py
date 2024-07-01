import streamlit as st

def main():
    # Configuración de la página
    st.set_page_config(page_title='ScrapAI', layout='wide')

    # CSS para el fondo que ocupe toda la pantalla sin márgenes
    st.markdown(
        """
        <style>
        body {
            margin: 0;
            padding: 0;
            background-color: #f0f0f0; /* Color de fondo */
            background-size: cover; /* Ajusta el tamaño del fondo */
            background-position: center; /* Centra el fondo */
        }
        .stApp {
            max-width: 100%; /* Ancho máximo de la aplicación */
            margin: 0;
            padding: 0;
        }
        </style>
        """, unsafe_allow_html=True
    )

    # Título centrado
    st.title("ScrapAI")
    
    # Imagen que ocupa todo el ancho
    st.image("im.jpg", width=None)  # width=None o width=0 para ocupar todo el ancho disponible

    # Texto en grande, en negrita y centrado
    st.markdown("<h1 style='text-align: center;'><b>ScrapAI</b></h1>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
