import streamlit as st
from db import engine
from sqlalchemy import text
from init_db import crear_tablas
crear_tablas()
from seed_propiedades import cargar_propiedades
cargar_propiedades()

from sqlalchemy import text

with engine.connect() as conn:
    result = conn.execute(text("SELECT COUNT(*) FROM propiedades"))
    total = result.scalar()

st.write(f"Total propiedades: {total}")

st.set_page_config(page_title="SisGenovesa", layout="wide")

st.title("Sistema de Alícuotas - Genovesa")

st.sidebar.title("Menú")
opcion = st.sidebar.selectbox("Selecciona", [
    "Dashboard",
    "Propiedades",
    "Pagos",
    "Gastos"
])

def test_db():
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            return "Conectado a la base de datos"
    except Exception as e:
        return str(e)

if opcion == "Dashboard":
    st.subheader("Estado del sistema")
    st.success(test_db())

elif opcion == "Propiedades":
    st.subheader("Registro de propiedades")
    st.info("Aquí irá el módulo de propiedades")

elif opcion == "Pagos":
    st.subheader("Registro de pagos")
    st.info("Aquí irá el módulo de pagos")

elif opcion == "Gastos":
    st.subheader("Registro de gastos")
    st.info("Aquí irá el módulo de gastos")
