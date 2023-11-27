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
st.write("""
# Información!!!
         Esta pagina ya no esta en uso. Dirijase al boton de abajo para ingresar al nuevo
         portal de Atención Ciudadana del Consejo Federal de Gobierno.
""")


st.link_button(
    "Inicio Atencion CFG",
    "https://atencioncfg.streamlit.app/"
)

st.write(
    """
Nota: Si usted trabaja en la OAC, para poder ingresar al Dashboard debe ingresar su usuario que consta de la inicial de su nombre y su apellido, (ejemplo: Carlos perez usuario: cperez) y su contraseña es su numero de cedula (solo numeros)

""")