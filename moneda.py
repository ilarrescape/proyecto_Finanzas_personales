import mysql.connector
import streamlit as st 
from dotenv import load_dotenv
import pandas as pd
import os
import time

load_dotenv()

class Moneda:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host = os.getenv('DB_HOST'),
            user = os.getenv('DB_USER'),
            password = os.getenv('DB_PASSWORD'),
            database = os.getenv('DB_NAME')
        )
        self.cursor = self.connection.cursor(dictionary=True)
        
    def obtener_datos(self):
        self.cursor.execute('SELECT * FROM moneda')
        result = self.cursor.fetchall()
        return result
    
    def agregar_datos(self,nombre):
        #Solución planteada al problema expuesto por los alumnos:
        #--->Qué pasa si no tenemos registros en la tabla moneda
        try:
            self.cursor.execute('SELECT * FROM moneda ORDER BY id_moneda DESC LIMIT 1')
            list_diccionario = self.cursor.fetchall()
            nuevo_id = list_diccionario[0]['id_moneda']
            nuevo_id += 1
            self.cursor.execute('INSERT INTO moneda (id_moneda, nombre_moneda) VALUES (%s, %s)',(nuevo_id, nombre))
            self.connection.commit()
        except:
            st.info('La tabla está vacía. El siguiente registro será el primero. :smile:')
            time.sleep(2)
            nuevo_id = 1
            self.cursor.execute('INSERT INTO moneda (id_moneda, nombre_moneda) VALUES (%s, %s)',(nuevo_id, nombre))
            self.connection.commit()
            st.rerun()
    
    def actualizar_datos(self, id, nombre):
        self.cursor.execute('UPDATE moneda SET nombre_moneda = %s WHERE id_moneda = %s',(nombre, id))
        self.connection.commit()

    def eliminar_datos(self, id):
        self.cursor.execute('DELETE FROM moneda WHERE id_moneda = %s',(id,))
        self.connection.commit()

class DataManagerMoneda:
    def __init__(self) -> None:
        self.db_moneda = Moneda()
        
    @st.dialog('Modificar Moneda')
    def modify_moneda(self, id, nombre):
        col_a, col_b, col_c = st.columns([0.5,9,0.5])
        with col_b:
            nombre_moneda = st.text_input('Ingrese la moneda: ', value=nombre)
            col_I, col_II, col_III = st.columns([5,4,4])
            with col_II:
                if st.button('Modificar',use_container_width= True):
                    self.db_moneda.actualizar_datos(id, nombre_moneda)
                    st.rerun()
            with col_III:
                if st.button('Eliminar', use_container_width= True):
                    self.db_moneda.eliminar_datos(id)
                    st.rerun()
    
    def display_moneda(self):
        data_moneda = self.db_moneda.obtener_datos()
        dataframe_moneda = pd.DataFrame(data_moneda)
        dataframe_moneda = dataframe_moneda.rename(columns={'id_moneda':'ID', 'nombre_moneda':'NOMBRE'})
        evento = st.dataframe(dataframe_moneda,
                    height=175,
                    use_container_width=True,
                    hide_index=True, 
                    selection_mode="single-row",
                    on_select="rerun")
        if evento['selection']['rows']:
            filtrado = dataframe_moneda[dataframe_moneda.index.isin(evento.selection['rows'])]
            valor_id = int(filtrado.iloc[0,0])
            valor_nombre = str(filtrado.iloc[0,1])
            self.modify_moneda(valor_id, valor_nombre)
    
    def add_moneda(self):
        cont_add_moneda = st.container(border=True)
        with cont_add_moneda:
            st.subheader('Agregar Nueva Moneda')
            nombre_moneda = st.text_input('Ingresar Moneda: ')
            if st.button('Guardar Moneda'):
                self.db_moneda.agregar_datos(nombre_moneda)
    
def fun_moneda():
    objeto_moneda = DataManagerMoneda()
    col_I, col_II = st.columns(2)
    with col_I:
        objeto_moneda.add_moneda()
    with col_II:
        objeto_moneda.display_moneda()
