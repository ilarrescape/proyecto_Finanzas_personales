import streamlit as st
import pandas as pd

dic = {
    'Nombre Alumno':['A','B','C'],
    'Nota Matemáticas': [7,8,7],
    'Nota Literatura':[8,7,8]
}

df_ejemplo = pd.DataFrame(
    dic
)


@st.dialog('Ventana Emergente')
def ejemplo_dialog(nombre, matemáticas, literatura):
    
    nom = st.text_input('Ingrese Nombre',value=nombre)
    mat = st.text_input('Ingrese apellido', value=matemáticas)
    lit = st.text_input('Enviar Mensaje',value=literatura)

def mostrar_df():
    seleccion = st.dataframe(df_ejemplo,
                            selection_mode= "single-row",
                            on_select = "rerun")
    if seleccion['selection']['rows']:
        filtrado = df_ejemplo[df_ejemplo.index.isin(seleccion.selection['rows'])]
        
        nombre_alumno = str(filtrado.iloc[0,0])
        nota_mat = str(filtrado.iloc[0,1])
        nota_lit = str(filtrado.iloc[0,2])
        
        ejemplo_dialog(nombre_alumno, nota_mat, nota_lit)
        
        