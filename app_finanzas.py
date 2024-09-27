import streamlit as st 
import pandas as pd

from moneda import fun_moneda

def mostrar_home():
    st.title('Bienvenido a la Aplicación de Finanzas Personales :smile:')

def main():
    if 'page' not in st.session_state:
        st.session_state.page = 'Inicio'

    st.markdown(
    """
        <style>
            .st-emotion-cache-igwvy71 h1{
                color: white;
                text-align: center;
            }
            .st-emotion-cache-8atqhb {
                padding-left: 1em;
                padding-right: 1em;
                padding-bottom: 1.5em;
                border-radius: 0.5em;
                border: 1px solid rgba(0, 0, 0, 0.5);
                background-color: black;
            }
        </style>
    """, unsafe_allow_html=True)
    
    st.sidebar.title('Menú de Opciones')

    if st.sidebar.button('Inicio', use_container_width=True):
        st.session_state.page = 'Inicio'
    if st.sidebar.button('Registro de Usuario', use_container_width= True):
        st.session_state.page = 'registro-usuario'
    if st.sidebar.button('Configurar Moneda',use_container_width=True):
        st.session_state.page = 'config-currency'
        
    if st.session_state.page == 'Inicio':
        mostrar_home()
    if st.session_state.page == 'config-currency':
        fun_moneda()
    # if st.session_state.page == 'registro-usuario':
    #     #mostrar_registro()

if __name__ == "__main__":
    main()