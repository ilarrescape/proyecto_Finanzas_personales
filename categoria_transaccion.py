import mysql.connector
import streamlit as st
from dotenv import load_dotenv
import pandas as pd
import os

load_dotenv()

class CategoriaTransaccion:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host = os.getenv('DB_HOST'),
            user = os.getenv('DB_USER'),
            password = os.getenv('DB_PASSWORD'),
            database = os.getenv('DB_NAME')
        )
        self.cursor = self.connection.cursor(dictionary=True)
    
    def obtener_categoria(self):
        self.cursor.execute('SELECT * FROM categoria_transaccion')
        result = self.cursor.fetchall()
        return result
    
    def agregar_categoria(self, nombre, tipo):
        self.cursor.execute('INSERT INTO categoria_transaccion (nombre_categoria, tipo_categoria) VALUES (%s, %s)',(nombre, tipo))
        self.connection.commit()
    
    def actualizar_categoria(self,id,nombre, tipo):
        self.cursor.execute('UPDATE categoria_transaccion SET nombre_categoria = %s, tipo_categoria = %s WHERE id_categoria = %s',(nombre, tipo, id))
        self.connection.commit()
    
    def eliminar_categoria(self,id):
        self.cursor.execute('DELETE FROM categoria_transaccion WHERE id_categoria = %s',(id,))
        self.connection.commit()
    
class DataManagerCategoriaTransaccion:
    def __init__(self) -> None:
        self.db_categoria_transaccion = CategoriaTransaccion()
    
    def display_categoria_transaccion(self):
        data_categoria_transaccion = self.db_categoria_transaccion.obtener_categoria()
        
        st.write(data_categoria_transaccion)
        dataframe_categoria_transaccion = pd.DataFrame(data_categoria_transaccion)
        dataframe_categoria_transaccion = dataframe_categoria_transaccion.rename(columns={'id_categoria':'ID',
                                                                                        'nombre_categoria':'NOMBRE',
                                                                                        'tipo_categoria':'TIPO'})
        return dataframe_categoria_transaccion

