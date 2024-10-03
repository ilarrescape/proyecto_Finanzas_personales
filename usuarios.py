import mysql.connector
import streamlit as st 
from dotenv import load_dotenv
import pandas as pd
import os
import time

load_dotenv()

class ClaseUsuario:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host = os.getenv('DB_HOST'),
            user = os.getenv('DB_USER'),
            password = os.getenv('DB_PASSWORD'),
            database = os.getenv('DB_NAME')
        )
        self.cursor = self.connection.cursor(dictionary=True)
        
    def obtener_datos(self):
        self.cursor.execute('SELECT * FROM usuario')
        result = self.cursor.fetchall()
        return result
    
    def agregar_datos(self,username, email, contraseña, moneda, nombre_real, apellido_real, tipo, estado):
        self.cursor.execute('INSERT INTO usuario (nombre_usuario, email_usuario, contraseña_usuario, moneda_usuario, nombre_real_usuario, apellido_real_usuario, tipo_usuario, estado_usuario) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)',(username, email, contraseña, moneda, nombre_real, apellido_real, tipo, estado))
        self.connection.commit()
    
    def actualizar_datos(self, id, username, email, contraseña, moneda, nombre_real, apellido_real, tipo, estado):
        self.cursor.execute('UPDATE usuario SET nombre_usuario = %s, email_usuario = %s, contraseña_usuario = %s, moneda_usuario = %s, nombre_real_usuario = %s, apellido_real_usuario = %s, tipo_usuario = s%, estado_usuario = s% WHERE id_usuario = %s',(username, email, contraseña, moneda, nombre_real, apellido_real, tipo, estado, id))
        self.connection.commit()

    def eliminar_datos(self, id):
        self.cursor.execute('DELETE FROM usuario WHERE id_usuario = %s',(id,))
        self.connection.commit()

class DataManagerUsuario:
    def __init__(self) -> None:
        self.db_usuario = ClaseUsuario()
        
    # @st.dialog('Modificar usuario')
    # def modify_usuario(self, id, username, email, contraseña, moneda, nombre_real, apellido_real):
    #     nombre_usuario = st.text_input('Ingrese la usuario: ', value=nombre)
    #     col_I, col_II, col_III = st.columns([5,4,4])
    #     with col_II:
    #         if st.button('Modificar',use_container_width= True):
    #             self.db_usuario.actualizar_datos(id, nombre_usuario)
    #             st.rerun()
    #     with col_III:
    #         if st.button('Eliminar', use_container_width= True):
    #             self.db_usuario.eliminar_datos(id)
    #             st.rerun()
    
    def display_usuario(self):
        data_usuario = self.db_usuario.obtener_datos()
        dataframe_usuario = pd.DataFrame(data_usuario)
        dataframe_usuario = dataframe_usuario.rename(columns={'id_usuario':'ID', 
                                                            'nombre_usuario':'USERNAME',
                                                            'email_usuario':'EMAIL',
                                                            'contraseña_usuario':'CONTRASEÑA',
                                                            'moneda_usuario':'MONEDA',
                                                            'nombre_real_usuario': 'NOMBRE',
                                                            'apellido_real_usuario':'APELLIDO'})
        # evento = st.dataframe(dataframe_usuario,
        #             height=175,
        #             use_container_width=True,
        #             hide_index=True, 
        #             selection_mode="single-row",
        #             on_select="rerun")
        
        # if evento['selection']['rows']:
        #     filtrado = dataframe_usuario[dataframe_usuario.index.isin(evento.selection['rows'])]
        #     valor_id = int(filtrado.iloc[0,0])
        #     valor_nombre = str(filtrado.iloc[0,1])
        #     self.modify_usuario(valor_id, valor_nombre)
    
    def add_usuario(self):
        cont_add_usuario = st.container(border=True)
        with cont_add_usuario:
            st.subheader('Agregar Nueva usuario')
            nombre_usuario = st.text_input('Ingresar usuario: ')
            if st.button('Guardar usuario'):
                self.db_usuario.agregar_datos(nombre_usuario)

