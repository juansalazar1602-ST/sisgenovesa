import streamlit as st
from db import engine
from sqlalchemy import text
from init_db import crear_tablas
from seed_propiedades import cargar_propiedades
from seed_usuarios import crear_admin
import streamlit as st
from sqlalchemy import text
import bcrypt
from db import engine
crear_tablas()
cargar_propiedades()
crear_admin()

if st.session_state.usuario is None:
    login()
    st.stop()

if "usuario" not in st.session_state:
    st.session_state.usuario = None

def login():
    st.title("Login SisGenovesa")

    username = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")

    if st.button("Ingresar"):
        with engine.connect() as conn:
            user = conn.execute(text("""
                SELECT * FROM usuarios 
                WHERE username = :u AND activo = TRUE
            """), {"u": username}).fetchone()

            if user:
                if bcrypt.checkpw(password.encode(), user.password_hash.encode()):
                    st.session_state.usuario = dict(user._mapping)
                    st.success("Bienvenido")
                    st.rerun()
                else:
                    st.error("Contraseña incorrecta")
            else:
                st.error("Usuario no existe")

usuario = st.session_state.usuario

st.sidebar.write(f"Usuario: {usuario['username']}")
st.sidebar.write(f"Rol: {usuario['rol']}")

if usuario["rol"] == "ADMIN":
    opciones = ["Dashboard", "Propiedades", "Pagos", "Gastos", "Usuarios"]
else:
    opciones = ["Mi Estado de Cuenta"]

opcion = st.sidebar.selectbox("Menú", opciones)

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
