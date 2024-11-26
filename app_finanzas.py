import streamlit as st 
import pandas as pd

from dotenv import load_dotenv
from dialog_de_prueba import mostrar_df
from moneda import fun_moneda
from cuentas import main_cuentas

load_dotenv()


def mostrar_home():
    st.info(f'Bienvenido {st.session_state.nombre_usuario}, su ID es {st.session_state.id_usuario}')
    st.write(st.session_state)

def main_finanzas(es_valido):
    if es_valido == True:
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
        if st.sidebar.button('Configurar Moneda',use_container_width=True):
            st.session_state.page = 'config-currency'
        if st.sidebar.button('Administrar Cuentas', use_container_width=True):
            st.session_state.page = 'bank-account'
        
        ### -----------------###
        if st.session_state.page == 'Inicio':
            mostrar_home()
        if st.session_state.page == 'config-currency':
            fun_moneda()
        if st.session_state.page == 'bank-account':
            main_cuentas()