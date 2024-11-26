import mysql.connector
import streamlit as st
from dotenv import load_dotenv
import pandas as pd
import time
from moneda import Moneda

import os

#La biblioteca 're' sirve para las expresiones regulares
import re
from app_finanzas import main_finanzas
from cryptography.fernet import Fernet
import bcrypt





if 'nombre_usuario' not in st.session_state:
    st.session_state.nombre_usuario = None

if 'id_usuario' not in st.session_state:
    st.session_state.id_usuario = None

if 'usuario_valido'not in st.session_state:
    st.session_state.usuario_valido = False

load_dotenv()

# Cargamos la clave secreta
def cargar_clave():
    return open("secret.key", "rb").read()


#####---- Primero, tratamos con los usuarios ----#####

# Función para encriptar cadenas
def encriptar_elemento(cadena):
    clave = cargar_clave()
    objeto_fernet = Fernet(clave)
    cadena_encriptada = objeto_fernet.encrypt(cadena.encode())
    return cadena_encriptada

#Función para desencriptar cadenas
def descifrar_elemento(cadena_encriptada):
    clave = cargar_clave()
    objeto_fernet = Fernet(clave)
    cadena_descifrada = objeto_fernet.decrypt(cadena_encriptada).decode()
    return cadena_descifrada
    
#####---- Segundo, tratamos con las contraseñas ----#####

# Función para hashear la contraseña
def hashear_contraseña(contraseña):
    sal = bcrypt.gensalt()
    hasheada = bcrypt.hashpw(contraseña.encode('utf-8'),sal)
    return hasheada


# Función para verificar la contraseña
def verificar_contraseña(hash_guardada, contraseña_ingresada):
    return bcrypt.checkpw(contraseña_ingresada.encode('utf-8'), hash_guardada.encode('utf-8 '))

st.set_page_config(
    layout='wide'
)


class Usuario:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host = os.getenv('DB_HOST'),
            user = os.getenv('DB_USER'),
            password = os.getenv('DB_PASSWORD'),
            database = os.getenv('DB_NAME')
        )
        self.cursor = self.connection.cursor(dictionary=True)
        
    def fetch_encrypted_username(self):
        self.cursor.execute('SELECT nombre_usuario FROM usuario')
        result = self.cursor.fetchall()
        return result
    
    def fetch_data(self, nombre_usuario, contraseña_usuario):
        self.cursor.execute('SELECT id_usuario, nombre_usuario FROM usuario where nombre_usuario = %s and contraseña_usuario = %s',(nombre_usuario, contraseña_usuario))
        result = self.cursor.fetchall()
        return result
    
    def fetch_contraseña(self, nombre_usuario):
        self.cursor.execute('SELECT contraseña_usuario FROM usuario where nombre_usuario = %s',(nombre_usuario,))
        result = self.cursor.fetchall()
        return result
        
    def add_data(self, username, email, contraseña,moneda, nombre_real, apellido_real, tipo, estado):
        self.cursor.execute('INSERT INTO usuario (nombre_usuario, email_usuario, contraseña_usuario, moneda_usuario, nombre_real_usuario, apellido_real_usuario, tipo_usuario,  estado_usuario) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)',(username, email, contraseña,moneda, nombre_real, apellido_real, tipo, estado))
        self.connection.commit()
    
class DataManagerUsuario:
    def __init__(self):
        self.db_usuario = Usuario()
        self.db_moneda = Moneda()
        
        
    def buscar_nombre_cifrado(self, nombre):
        data_nombre_encriptado = self.db_usuario.fetch_encrypted_username()
        nombre_descifrado = ''
        for diccionario in data_nombre_encriptado:
            nombre_cifrado = diccionario['nombre_usuario']
            nombre_descifrado = descifrar_elemento(nombre_cifrado)
            if nombre_descifrado == nombre:
                return nombre_cifrado
        return 'No se encontró el Nombre del Usuario'
        
    
    def display_data(self,nombre, contraseña):
        nombre_cifrado = self.buscar_nombre_cifrado(nombre)
        
        if nombre_cifrado == 'No se encontró el Nombre del Usuario':
            return False, nombre_cifrado
        else:
            diccionario_obtenido = self.db_usuario.fetch_contraseña(nombre_cifrado)
            contraseña_hasheada = diccionario_obtenido[0]['contraseña_usuario']
            
            verifica = verificar_contraseña(contraseña_hasheada,contraseña)
            
            if verifica:
                data_usuarios = self.db_usuario.fetch_data(nombre_cifrado, contraseña_hasheada)
                
                id_usuario = data_usuarios[0]['id_usuario'] 

                nombre_descifrado = descifrar_elemento(data_usuarios[0]['nombre_usuario'])
                st.session_state.nombre_usuario = nombre_descifrado
                st.session_state.id_usuario = id_usuario
                return True, 'Inicio de Sesión Exitoso'
            else:
                return False, 'Contraseña Incorrecta'
    
    def validar_correo(self, email):
        cadena_patron = r'^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$'
        if re.match(cadena_patron, email):
            return True
        else:
            return False
    
    @st.dialog('Registro de Usuario',width="large")
    def registro_usuario(self):
        registro_nombre_usuario = st.text_input('Nombre de Usuario: ')
        _contra_I, _contra_II = st.columns(2)
        with _contra_I:
            contraseña_usuario = st.text_input('Contraseña: ', type='password')
        with _contra_II:
            repetir_contraseña = st.text_input('Repetir: ', type='password')
        
        _col_email, _col_moneda = st.columns([4,2])
        
        with _col_email:
            email_usuario = st.text_input('Correo Electrónico: ', )
        with _col_moneda:
            
            dic_moneda = {fila['nombre_moneda']:fila['id_moneda'] for fila in  self.db_moneda.obtener_datos()}
            
            select_moneda = st.selectbox('Seleccione una moneda: ', dic_moneda.keys())
        
        _col_nombre_real, _col_apellido_real = st.columns(2)
        with _col_nombre_real:
            nombre_real = st.text_input('Nombre Real:')
        with _col_apellido_real:
            apellido_real = st.text_input('Apellido Real:')
        
        tipo_usuario = 'Regular'
        estado_usuario = 'Activo'
        
        nombre_existe = False
        if st.button('Crear Usuario'):
            if contraseña_usuario == repetir_contraseña:
                data_nombre_encriptado = self.db_usuario.fetch_encrypted_username()
                nombre_descifrado = ''
                for diccionario in data_nombre_encriptado:
                    nombre_cifrado = diccionario['nombre_usuario']
                    nombre_descifrado = descifrar_elemento(nombre_cifrado)
                    if nombre_descifrado == registro_nombre_usuario:
                        nombre_existe = True
                if nombre_existe == False:
                    if self.validar_correo(email_usuario):
                        nuevo_nombre_cifrado = encriptar_elemento(registro_nombre_usuario)
                        contraseña_hasheada = hashear_contraseña(contraseña_usuario)
                        self.db_usuario.add_data(nuevo_nombre_cifrado, email_usuario,contraseña_hasheada, dic_moneda[select_moneda],nombre_real, apellido_real,tipo_usuario, estado_usuario)
                        st.success(f'El usuario {registro_nombre_usuario} fue creado exitosamente :smile:')
                        time.sleep(2)
                        st.rerun()
                    else:
                        st.error(f'El correo electrónico {email_usuario} está mal escrito')
                else:
                    st.error(f'El nombre de usuario {registro_nombre_usuario} ya se encuentra registrado.')   
            else:
                st.error('Las contraseñas no coinciden.')
    
    def login_usuario(self):
        valido = False
        mensaje = ''
        col_I,col_II, col_III = st.columns([6,5,6])
        with col_II:
            with st.container(border=True):
                st.image('estaticos\\sistema.webp')
                username = st.text_input('Ingresar Usuario: ')
                userpass = st.text_input('Ingresar Contraseña: ', type='password')
                col_sesion, col_registro = st.columns(2)
                with col_sesion:
                    if st.button('Iniciar Sesión',type='primary', use_container_width=True):
                        valido, mensaje = self.display_data(username, userpass)
                with col_registro:
                    if st.button('Registrarme', use_container_width=True):
                        self.registro_usuario()
                if mensaje !='':
                    if valido == False:
                        st.error(mensaje)
                    else:
                        st.success(mensaje)
                        st.session_state.nombre_usuario = username
            return valido

def main_usuarios():
    if st.session_state['usuario_valido'] == True:
        main_finanzas(st.session_state['usuario_valido'])
    else:
        objeto_usuario = DataManagerUsuario()
        st.session_state['usuario_valido'] = objeto_usuario.login_usuario()
        
        if st.session_state['usuario_valido']:
            st.rerun()

main_usuarios()