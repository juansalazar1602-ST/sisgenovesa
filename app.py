import streamlit as st
from db import engine
from sqlalchemy import text
from init_db import crear_tablas
from seed_propiedades import cargar_propiedades
from seed_usuarios import crear_admin
import bcrypt

# -----------------------------------
# CONFIGURACIÓN INICIAL
# -----------------------------------
st.set_page_config(page_title="SisGenovesa", layout="wide")

# Inicializar sesión
if "usuario" not in st.session_state:
    st.session_state.usuario = None

# Crear estructura base (solo corre si no existe)
crear_tablas()
cargar_propiedades()
crear_admin()

# -----------------------------------
# LOGIN
# -----------------------------------
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

# Si no está logueado → mostrar login
if st.session_state.usuario is None:
    login()
    st.stop()

# -----------------------------------
# USUARIO LOGUEADO
# -----------------------------------
usuario = st.session_state.usuario

st.sidebar.write(f"Usuario: {usuario['username']}")
st.sidebar.write(f"Rol: {usuario['rol']}")

# -----------------------------------
# MENÚ SEGÚN ROL
# -----------------------------------
if usuario["rol"] == "ADMIN":
    opciones = ["Dashboard", "Propiedades", "Pagos", "Gastos", "Usuarios"]
else:
    opciones = ["Mi Estado de Cuenta"]

opcion = st.sidebar.selectbox("Menú", opciones)

# -----------------------------------
# DASHBOARD
# -----------------------------------
if opcion == "Dashboard":
    st.title("Sistema de Alícuotas - Genovesa")

    with engine.connect() as conn:
        total = conn.execute(text("SELECT COUNT(*) FROM propiedades")).scalar()

    st.success("Conectado a la base de datos")
    st.write(f"Total propiedades: {total}")

# -----------------------------------
# PROPIEDADES
# -----------------------------------
elif opcion == "Propiedades":
    st.subheader("Listado de propiedades")

    with engine.connect() as conn:
        data = conn.execute(text("""
            SELECT id, numero_propiedad, tipo 
            FROM propiedades
            ORDER BY numero_propiedad
        """)).fetchall()

    for p in data:
        col1, col2, col3, col4 = st.columns([1,2,2,2])

        col1.write(p.numero_propiedad)
        col2.write(p.tipo)

        nuevo_tipo = col3.selectbox(
            f"Tipo {p.id}",
            ["CASA", "LOTE"],
            index=0 if p.tipo == "CASA" else 1
        )

        if col4.button(f"Guardar {p.id}"):
            with engine.connect() as conn:
                conn.execute(text("""
                    UPDATE propiedades
                    SET tipo = :tipo
                    WHERE id = :id
                """), {
                    "tipo": nuevo_tipo,
                    "id": p.id
                })
                conn.commit()
            st.success(f"Propiedad {p.numero_propiedad} actualizada")
            st.rerun()

# -----------------------------------
# USUARIOS (ADMIN)
# -----------------------------------
elif opcion == "Usuarios" and usuario["rol"] == "ADMIN":

    st.subheader("Crear usuario")

    with engine.connect() as conn:
        propiedades = conn.execute(text("""
            SELECT id, numero_propiedad FROM propiedades
        """)).fetchall()

    opciones_prop = {
        f"Casa {p.numero_propiedad}": p.id for p in propiedades
    }

    username = st.text_input("Usuario (ej: casa_10)")
    password = st.text_input("Contraseña", type="password")
    propiedad_select = st.selectbox("Selecciona propiedad", list(opciones_prop.keys()))

    if st.button("Crear usuario"):
        propiedad_id = opciones_prop[propiedad_select]

        hash_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

        with engine.connect() as conn:
            conn.execute(text("""
                INSERT INTO usuarios (username, password_hash, rol, propiedad_id)
                VALUES (:u, :p, 'PROPIETARIO', :prop)
            """), {
                "u": username,
                "p": hash_pw,
                "prop": propiedad_id
            })
            conn.commit()

        st.success("Usuario creado correctamente")

# -----------------------------------
# PAGOS
# -----------------------------------
elif opcion == "Pagos":
    st.subheader("Módulo de pagos")
    st.info("Aquí vamos a registrar pagos próximamente")

# -----------------------------------
# GASTOS
# -----------------------------------
elif opcion == "Gastos":
    st.subheader("Módulo de gastos")
    st.info("Aquí vamos a registrar gastos")

# -----------------------------------
# COPROPIETARIO
# -----------------------------------
elif opcion == "Mi Estado de Cuenta":
    st.subheader("Mi estado de cuenta")

    st.info("Aquí verás tus pagos y deudas (siguiente paso)")
