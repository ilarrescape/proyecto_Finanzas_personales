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

instancia = Moneda()

instancia.actualizar_datos(5,'Euro')
