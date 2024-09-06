import mysql.connector
import streamlit as st 
from dotenv import load_dotenv
import pandas as pd
import os

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
        self.cursor.execute('SELECT * FROM moneda ORDER BY id_moneda DESC LIMIT 1')
        list_diccionario = self.cursor.fetchall()
        nuevo_id = list_diccionario[0]['id_moneda']
        nuevo_id += 1
        self.cursor.execute('INSERT INTO moneda (id_moneda, nombre_moneda) VALUES (%s, %s)',(nuevo_id, nombre))
        self.connection.commit()
    
    def actualizar_datos(self, id, nombre):
        self.cursor.execute('UPDATE moneda SET nombre_moneda = %s WHERE id_moneda = %s',(nombre, id))
        self.connection.commit()

    def eliminar_datos(self, id):
        self.cursor.execute('DELETE FROM moneda WHERE id_moneda = %s',(id,))
        self.connection.commit()

class DataManagerMoneda:
    def __init__(self) -> None:
        self.db_moneda = Moneda()
    
    def display_moneda(self):
        data_moneda = self.db_moneda.obtener_datos()
        dataframe_moneda = pd.DataFrame(data_moneda)
        dataframe_moneda = dataframe_moneda.rename(columns={'id_moneda':'ID', 'nombre_moneda':'NOMBRE'})
        st.dataframe(dataframe_moneda, height=175, use_container_width=True, hide_index=True)


instancia = DataManagerMoneda()

# st.dataframe(instancia.display_moneda())

instancia.display_moneda()

#|---> Git Init
#|---> Guardar datos en master o main |---> git add . (staged area) |---> git commit -m 'Mensaje Desciptivo'
#|---> Crear nuevas ramas |---> git branch nombre_rama
#|---> Movernos a la rama |---> git checkout nombre_rama
#|---> Agregar modificaciones a la rama |---> git add .|---> git commit -m 'mensaje descriptivo'

#|-------------------------------------
#|git status|---> Saber el estado de nuestros archivos en una rama
#|git branch|---> Saber el nombre de la rama donde estamos parados
#|git branch -l|---> Saber todas las ramas (En color verde va a aparecer dónde están parados) 

#|--------Anotaciones---------
#| 1- Si un archivo aparece en color rojo cuando escribimos 'git status', significa que hay que pasarlo al "staged area"
#| 2- Si un archivo aparece en color verde cuando escribimos 'git status', significa que se encuentra en "staged area"
#| 3- Si el archivo se encuentra en el "staged area", hay que comprometerlo con 'git commit'
