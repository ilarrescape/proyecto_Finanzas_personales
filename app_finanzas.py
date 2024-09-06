import streamlit as st 
import pandas as pd


def mostrar_home():
    st.title('Bienvenido a la Aplicación de Finanzas Personales :smile:')

def main():
    if 'page' not in st.session_state:
        st.session_state.page = 'Inicio'

    st.sidebar.title('Menú de Opciones')

    if st.sidebar.button('Inicio'):
        st.session_state.page = 'Inicio'
    if st.sidebar.button('Registro de Usuario'):
        st.session_state.page = 'registro-usuario'
    if st.sidebar.button('Configurar Moneda'):
        st.session_state.page = 'config-currency'
        
    if st.session_state.page == 'Inicio':
        mostrar_home()
    if st.session_state.page == 'registro-usuario':
        #mostrar_registro()

if __name__ == "__main__":
    main()