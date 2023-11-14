import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="Dashboard - Comunicaciones SINCO")
st.write("""
# Comunicaciones SINCO
Fondo de Compensación Interterritorial\n
Consejo Federal de Gobierno
""")

df = pd.read_excel("casos.xlsx")
df["Transmisor/Nombre"] = df["Transmisor/Nombre"].astype(str)
df =  df.loc[~df["Transmisor/Nombre"].str.contains("prueba"), ]

df = df.dropna(subset=["Estatus"])

#df["Estatus"] = df["Estatus"].astype(str)
df.loc[df["Estatus"].isna(), "Estatus"] = "Ninguno"

# estatus de asignacion
d = {
    "assigned":"Asignado",
    "answered":"Respondido",
    "cancel":"Cancelado",
    "process":"Proceso",
    False:"False",

}

df["Asignado/Estatus"] = df["Asignado/Estatus"].replace(d)

#Estatus
d2 = {
    'process':'A-En Proceso', 
    'confirm':'B-Confirmado', 
    'bound':'C-Vinculado', 
    'reply':'D-Respondido', 
    'waiting':'E-En Espera', 
    'unanswered':'F-Sin respuesta'
    }

df["Estatus"] = df["Estatus"].replace(d2)

# -- Grafico de estatus --
valores = df["Estatus"].value_counts()

source = pd.DataFrame({"category": valores.index, "value": valores})

ch = alt.Chart(source).mark_arc().encode(
    theta="value",
    color="category"
)

st.altair_chart(
    (ch).interactive(),
    use_container_width=True
)


list_options_estatus = []
list_options_estatus.extend(df["Estatus"].unique().tolist())
list_options_estatus.sort()

estatus = st.sidebar.selectbox('Seleccione el estatus', list_options_estatus)
df_process = df.loc[(df["Estatus"]==estatus), ]


responsable = st.sidebar.selectbox('Seleccione el responsable', ['Todos', 'LUIS GERMAN RIVAS ZAMBRANO', 'CRUZ DAVID MATA NOGUERA',
       'CIRO ANTONIO RODRIGUEZ VILLANUEVA',
       'SOFIA MARGARITA FLEURY HERNANDEZ',
       'CESAR EDUARDO CARRERO ARISTIZABAL', 'RICARDO JOSE MUSETT ROMAN',
       'LUISANA VALENTINA VELASQUEZ FERMIN',
       'JOALI GABRIELA MORENO PINTO'])

if (responsable != "Todos"):
    df_process = df_process.loc[(df_process["Responsable/Mostrar nombre"] ==responsable), ]
    
analistas = st.sidebar.selectbox('Seleccione el analista', ['Todos', 
                                                                 'ROSARIO ELISA MATHEUS SULBARAN', 
                                                                 'NORMAN JOSE SOTO BOLIVAR', 
                                                                 'CRUZ DAVID MATA NOGUERA', 
                                                                 'SOFIA MARGARITA FLEURY HERNANDEZ',])

if (analistas != "Todos"):
    df_process = df_process.loc[(df_process["Asignado/Asignado/Nombre"] ==analistas), ]


list_options = ['Todos']
list_options.extend(df_process["Asignado/Estatus"].unique().tolist())
   
asignacion_estatus = st.sidebar.selectbox('Seleccione el estatus de asignación', list_options)

if (asignacion_estatus != "Todos"):
    df_process = df_process.loc[(df_process["Asignado/Estatus"] ==asignacion_estatus), ]

# -- Grafico de categorias --

st.subheader('Casos por Asunto')



categorias = df_process["Categoría/Nombre de categoría"].value_counts()

df_categorias = pd.DataFrame({"categoria":categorias.index, "valores":categorias})

bar = alt.Chart(df_categorias).mark_bar().encode(
    x= alt.X("categoria", sort=None),
    y="valores"
)

st.altair_chart(
    (bar).interactive(),
    use_container_width=True
)



t_min= df_process["Creado en"].min()


st.subheader('El mas urgente de atender')
st.dataframe(df_process.loc[(df_process["Creado en"]==t_min), ])

st.subheader('por atender rapido')
st.text(len(df_process))
st.dataframe(df_process.sort_values(by=["Creado en"]).head(100))
