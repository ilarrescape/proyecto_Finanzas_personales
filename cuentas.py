import mysql.connector
import streamlit as st
from dotenv import load_dotenv
import pandas as pd
import os
import time

load_dotenv()

class ClaseCuenta:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host = os.getenv('DB_HOST'),
            user = os.getenv('DB_USER'),
            password = os.getenv('DB_PASSWORD'),
            database = os.getenv('DB_NAME')
        )
        self.cursor = self.connection.cursor(dictionary=True)
    
    def obtener_cuenta(self):
        consulta = """
            select
                cuenta.id_cuenta as 'ID',
                usuario.nombre_real_usuario as 'Nombre Real',
                usuario.apellido_real_usuario as 'Apellido Real',
                cuenta.alias_cuenta as 'Alias',
                cuenta.numero_cuenta as 'CBU - CVU',
                banco.nombre_banco as 'Banco',  
                cuenta.saldo_cuenta as 'Saldo'
            from
                usuario
            join
                cuenta on usuario.id_usuario = cuenta.id_usuario
            join
                banco on cuenta.banco_cuenta = banco.id_banco
            where usuario.id_usuario = %s
        """
        self.cursor.execute(consulta, (st.session_state['id_usuario'],))
        result = self.cursor.fetchall()
        return result
    
    def obtener_banco(self):
        self.cursor.execute('SELECT * FROM banco')
        result = self.cursor.fetchall()
        return result
    
    def agregar_cuenta(self, alias, cvu_cbu, banco, saldo):
        self.cursor.execute('INSERT INTO cuenta (alias_cuenta, numero_cuenta, banco_cuenta, saldo_cuenta, id_usuario) VALUES (%s, %s, %s, %s,%s)',(alias, cvu_cbu, banco, saldo, st.session_state['id_usuario']))
        self.connection.commit()
    def eliminar_cuenta(self,id_cuenta):
        self.cursor.execute('DELETE FROM cuenta WHERE id_cuenta = %s',(id_cuenta,))
        self.connection.commit()
        
    
    def editar_cuenta(self, id, alias, numero_cuenta, banco_cuenta, saldo_cuenta, id_usuario):
        # st.write(type(alias))
        
        consulta_actualizar = """
        UPDATE 
            `db_finanzas`.`cuenta`
        SET
            `alias_cuenta` = %s,
            `numero_cuenta` = %s,
            `banco_cuenta` = %s,
            `saldo_cuenta` = %s,
            `id_usuario` = %s
        WHERE `id_cuenta` = %s;
        """
        self.cursor.execute(consulta_actualizar, (alias, numero_cuenta, banco_cuenta, saldo_cuenta, id_usuario, id))
        self.connection.commit()

class DataManagerCuenta():
    def __init__(self):
        self.db_cuenta = ClaseCuenta()
    
    @st.dialog('Modificar Cuenta')
    def modificar_cuenta(self,df):
        txt_modificar_alias = st.text_input('Alias:', value= df.iloc[0]['Alias'])
        dic_banco = {fila['nombre_banco']:fila['id_banco'] for fila in self.db_cuenta.obtener_banco()}
        lista_banco = list(dic_banco.keys())
        box_modificar_banco = st.selectbox('Seleccionar Banco', lista_banco, index=lista_banco.index((df.iloc[0]['Banco'])))
        num_modificar_CBU = st.number_input('CBU - CVU', value= df.iloc[0]['CBU - CVU'])
        num_modificar_saldo = st.number_input('Saldo', value= df.iloc[0]['Saldo'], step=0.25)

        if st.button('Guardar'):
                self.db_cuenta.editar_cuenta(alias=txt_modificar_alias,
                                            numero_cuenta= int(num_modificar_CBU),
                                            banco_cuenta= int(dic_banco[box_modificar_banco]),
                                            saldo_cuenta= float(num_modificar_saldo), 
                                            id_usuario=int(st.session_state['id_usuario']),
                                            id=int(df.iloc[0]['ID']))
                st.success('¡Datos ingresados correctamente!')
                time.sleep(1)
                st.rerun()

    @st.dialog('Eliminar Cuenta')
    def delete_cuenta(self,df):
        alias = df.iloc[0]['Alias']
        st.write(f'¿Está seguro de que quiere eliminar la cuenta __{alias}__?')
        if st.button('Eliminar'):
            id = int(df.iloc[0]['ID'])
            self.db_cuenta.eliminar_cuenta(id)
            st.success(f'Los datos se eliminaron satisfactoriamente')
            time.sleep(1)
            st.rerun()
    
    def pasar_valores(self,seleccion, df, edit_delete):
        df = df[df.index.isin(seleccion)]
        if not(df.empty): self.modificar_cuenta(df) if edit_delete =='Edit' else self.delete_cuenta(df)
    
    def display_cuenta(self):
        data_cuenta = self.db_cuenta.obtener_cuenta()
        if data_cuenta:
            df_cuenta = pd.DataFrame(data_cuenta)
            filtro = st.dataframe(
                                df_cuenta,
                                use_container_width=True,
                                selection_mode='single-row',
                                on_select='rerun',
                                height = 310,
                                hide_index= True
                                )
            
            _col_relleno, _col_editar, _col_eliminar = st.columns([8,1,1])
            
            
            deshabilitado = True
            if filtro['selection']['rows']:
                deshabilitado = False
                
            with _col_editar:
                if st.button('', icon=':material/edit:', disabled=deshabilitado, use_container_width = True):
                    self.pasar_valores(filtro['selection']['rows'],df_cuenta,'Edit')
            with _col_eliminar:
                if st.button('', icon=':material/delete:', disabled=deshabilitado, use_container_width = True):
                    self.pasar_valores(filtro['selection']['rows'],df_cuenta,'Delete')
        else:
            st.info(f"El usuario {st.session_state['nombre_usuario']} no tiene cuentas agendadas.")

    def add_cuenta(self):
        #alias, cvu_cbu, banco, saldo):
        alias = st.text_input('Alias de Cuenta')
        cvu_cbu = st.number_input('CBU/CVU:',step=1)
        
        lista_bancos = self.db_cuenta.obtener_banco()
        dic_bancos = {row['nombre_banco'] : row['id_banco']for row in lista_bancos}
        select_banco = st.selectbox('Banco', dic_bancos.keys())
        saldo = st.number_input('Saldo Actual',step=0.25)
        
        if st.button('Agregar Cuenta'):
            self.db_cuenta.agregar_cuenta(alias=alias, cvu_cbu=cvu_cbu, banco= dic_bancos[select_banco], saldo=saldo)
            st.rerun()

def main_cuentas():
    objeto_cuentas = DataManagerCuenta()
    
    _columna_ver_datos, _columna_agregar_datos = st.columns([6,2])
    
    with _columna_ver_datos:
        contenedor_cuenta = st.container(border= True, height= 410)
        with contenedor_cuenta:
            objeto_cuentas.display_cuenta()
    with _columna_agregar_datos:
        _contenedor_formulario = st.container(border=True, height= 410)
        with _contenedor_formulario:
            objeto_cuentas.add_cuenta()