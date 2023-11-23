import streamlit as st
import pandas as pd
import altair as alt


# ---------> Cabecera del Dashboard
st.set_page_config(page_title="Dashboard - Comunicaciones SINCO", page_icon="📊")
st.write("""
# Comunicaciones SINCO
Fondo de Compensación Interterritorial\n
Consejo Federal de Gobierno
""")
# Fin de Cabecera del Dashboard <-------------------------------------------------------

#-----------------------------------------------------------------------
# convertir en funcion

#@st.cache_data
def load_data():
    # ----------> Leer Bases de Datos
    df = pd.read_excel("casos.xlsx")
    df["Transmisor/Nombre"] = df["Transmisor/Nombre"].astype(str)
    df =  df.loc[~df["Transmisor/Nombre"].str.contains("prueba"), ]
    df = df.dropna(subset=["Estatus"])
    df.loc[df["Asignado/Asignado/Nombre"].isna(), "Asignado/Asignado/Nombre"] = "Ninguno"
    #  Fin de leer Bases de Datos <--------------------------------------------------------

    # ----------> Traducir los estatus
    # estatus de asignacion
    d = {
        "assigned":"Asignado",
        "answered":"Respondido",
        "cancel":"Cancelado",
        "process":"Proceso",
        False:"False",

    }
    df["Asignado/Estatus"] = df["Asignado/Estatus"].replace(d)

    d2 = {
        'process':'A-En Proceso', 
        'confirm':'B-Confirmado', 
        'bound':'C-Vinculado', 
        'reply':'D-Respondido', 
        'waiting':'E-En Espera', 
        'unanswered':'F-Sin respuesta'
    }
    df["Estatus"] = df["Estatus"].replace(d2)
    # Fin de traduccion de estatus <-------------------------------------------------------
    return df

df = load_data()

#fin convertir en funcion
#-----------------------------------------------------------------------

# --------> Crear listas de opciones 
list_options_estatus = ['0-Todos']
list_options_estatus.extend(df["Estatus"].unique().tolist())
list_options_estatus.sort()

list_options_asignado = ['0-Todos']
list_options_asignado.extend(df["Asignado/Asignado/Nombre"].unique().tolist())
list_options_asignado.sort()

list_options = ['0-Todos']
list_options.extend(df["Asignado/Estatus"].unique().tolist())
# Fin de Crear listas de opciones <---------------------------------------------------- 

### -----------------------------------> Creacion de barra de selecciones
# Sidebar para seleccionar destinatario
responsable = st.sidebar.selectbox('Responsable del Caso', ['0-Todos', 
                                                            'LUIS GERMAN RIVAS ZAMBRANO', 
                                                            'CRUZ DAVID MATA NOGUERA', 
                                                            'CIRO ANTONIO RODRIGUEZ VILLANUEVA', 
                                                            'SOFIA MARGARITA FLEURY HERNANDEZ', 
                                                            'CESAR EDUARDO CARRERO ARISTIZABAL', 
                                                            'RICARDO JOSE MUSETT ROMAN', 
                                                            'LUISANA VALENTINA VELASQUEZ FERMIN', 
                                                            'JOALI GABRIELA MORENO PINTO'])

# Sidebar para seleccionar estatus
estatus = st.sidebar.selectbox('Estatus de Casos', list_options_estatus)

# Sidebar para seleccionar responsable de responder
analista = st.sidebar.selectbox('Analista Asignado', list_options_asignado)

# Sidebar para seleccionar el estatus de la asignacion
asignacion = st.sidebar.selectbox('Estatus de asignación', list_options)
### Fin de Creacion de barra de selecciones <-------------------------------------------

### --------------------------> Opciones para matriciar
r = (df['Responsable/Mostrar nombre'] == responsable)
e = (df['Estatus'] == estatus)
a = (df['Asignado/Asignado/Nombre'] == analista)
ea = (df['Asignado/Estatus'] == asignacion)
### Fin de Opciones para matriciar <------------------------------------------------------

### -----------------------> Definicion de funciones
def info_sin_estatus():
    # -- Grafico de categorias --
    st.subheader('Casos por Asunto')
    categorias = df_full["Categoría/Nombre de categoría"].value_counts()
    df_categorias = pd.DataFrame({"categoria":categorias.index, "valores":categorias})
    bar = alt.Chart(df_categorias).mark_bar().encode(
        x= alt.X("categoria", sort=None),
        y="valores"
    )
    st.altair_chart(
        (bar).interactive(),
        use_container_width=True
    )
    # Mostrar la información filtrada en un cuadro
    t_min= df_full["Creado en"].min()

    st.subheader('El mas antiguo')
    st.dataframe(df_full.loc[(df_full["Creado en"]==t_min), ])
    st.subheader('Lo mas reciente')
    st.text(len(df_full))
    st.dataframe(df_full)

def info_full():
        # -- Grafico de estatus --
    st.subheader('Balance General')
    valores = df_full["Estatus"].value_counts()
    source = pd.DataFrame({"category": valores.index, "value": valores})
    ch = alt.Chart(source).mark_arc().encode(
        theta="value",
        color="category"
    )
    st.altair_chart(
        (ch).interactive(),
        use_container_width=True
    )
    # -- Grafico de categorias --
    st.subheader('Casos por Asunto')
    categorias = df_full["Categoría/Nombre de categoría"].value_counts()
    df_categorias = pd.DataFrame({"categoria":categorias.index, "valores":categorias})
    bar = alt.Chart(df_categorias).mark_bar().encode(
        x= alt.X("categoria", sort=None),
        y="valores"
    )
    st.altair_chart(
        (bar).interactive(),
        use_container_width=True
    )
    # Mostrar la información filtrada en un cuadro
    t_min= df_full["Creado en"].min()

    st.subheader('El mas antiguo')
    st.dataframe(df_full.loc[(df_full["Creado en"]==t_min), ])
    st.subheader('Lo mas reciente')
    st.text(len(df_full))
    st.dataframe(df_full)

def info_general():
    # -- Grafico de estatus --
    st.subheader('Balance General')
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
    # -- Grafico de categorias --
    st.subheader('Casos por Asunto')
    st.text(f"{len(df)} Casos")
    categorias = df["Categoría/Nombre de categoría"].value_counts()
    df_categorias = pd.DataFrame({"categoria":categorias.index, "valores":categorias})
    bar = alt.Chart(df_categorias).mark_bar().encode(
        x= alt.X("categoria", sort=None),
        y="valores"
    )
    st.altair_chart(
        (bar).interactive(),
        use_container_width=True
    )
    #st.subheader('Todas las comunicaciones')
    #st.text(len(df))
    #st.dataframe(df)
### Fin de Definicion de funciones <------------------------------------------------------

### -----------------------> Matriz de funcionalidad
# Verifica que todos esten filtrados (listo)
if (responsable != "0-Todos") & (estatus != "0-Todos") & (analista != "0-Todos") & (asignacion != "0-Todos"):
    # Filtrar el DataFrame según las opciones seleccionadas en las sidebars
    df_full = df[r & e & a & ea]
    info_sin_estatus()
# Verifica que el responsable solamente este filtrado
elif (responsable != "0-Todos") & (estatus == "0-Todos") & (analista == "0-Todos") & (asignacion == "0-Todos"):
    # Filtrar el DataFrame según las opciones seleccionadas en las sidebars
    df_full = df[r]
    info_full()
# Verifica que esten filtrados el destinatario y el estatus
elif (responsable != "0-Todos") & (estatus != "0-Todos") & (analista == "0-Todos") & (asignacion == "0-Todos"):
    df_full = df[r & e]
    info_sin_estatus()
# Verifica que esten filtrados el destinatario, el estatus y el analista
elif (responsable != "0-Todos") & (estatus != "0-Todos") & (analista != "0-Todos") & (asignacion == "0-Todos"):
    df_full = df[r & e & a]
    info_sin_estatus()
# Verifica que esten filtrados el estatus, el analista y la asignacion
elif (responsable == "0-Todos") & (estatus != "0-Todos") & (analista != "0-Todos") & (asignacion != "0-Todos"):
    df_full = df[e & a & ea]
    info_sin_estatus()
# Verifica que esten filtrados el analista y la asignacion
elif (responsable == "0-Todos") & (estatus == "0-Todos") & (analista != "0-Todos") & (asignacion != "0-Todos"):
    df_full = df[a & ea]
    info_full()
# Verifica que esten filtrados solo la asignacion
elif (responsable == "0-Todos") & (estatus == "0-Todos") & (analista == "0-Todos") & (asignacion != "0-Todos"):
    df_full = df[ea]
    info_full()
# Verifica que esten filtrados responsable, estatus y asignacion
elif (responsable != "0-Todos") & (estatus != "0-Todos") & (analista == "0-Todos") & (asignacion != "0-Todos"):
    df_full = df[r & e & ea]
    info_sin_estatus()
# Verifica que esten filtrados responsable, analista y asignacion
elif (responsable != "0-Todos") & (estatus == "0-Todos") & (analista != "0-Todos") & (asignacion != "0-Todos"):
    df_full = df[r & a & ea]
    info_full()
# Verifica que esten filtrados responsable y analista
elif (responsable != "0-Todos") & (estatus == "0-Todos") & (analista != "0-Todos") & (asignacion == "0-Todos"):
    df_full = df[r & a]
    info_full()
# Verifica que esten filtrados responsable y asignacion
elif (responsable != "0-Todos") & (estatus == "0-Todos") & (analista == "0-Todos") & (asignacion != "0-Todos"):
    df_full = df[r & ea]
    info_full()
# Verifica que esten filtrados estatus y asignacion
elif (responsable == "0-Todos") & (estatus != "0-Todos") & (analista == "0-Todos") & (asignacion != "0-Todos"):
    df_full = df[e & ea]
    info_sin_estatus()
# Verifica que esten filtrados solo estatus
elif (responsable == "0-Todos") & (estatus != "0-Todos") & (analista == "0-Todos") & (asignacion == "0-Todos"):
    df_full = df[e]
    info_sin_estatus()
# Verifica que esten filtrados solo analista
elif (responsable == "0-Todos") & (estatus == "0-Todos") & (analista != "0-Todos") & (asignacion == "0-Todos"):
    df_full = df[a]
    info_full()
# Verifica que esten filtrados estatus y analista
elif (responsable == "0-Todos") & (estatus != "0-Todos") & (analista != "0-Todos") & (asignacion == "0-Todos"):
    df_full = df[e & a]
    info_sin_estatus()
# Verifica que ninguno este filtrado
else:
    info_general()
### Fin de la Matriz de funcionalidad <-------------------------------------------------------------------------------
