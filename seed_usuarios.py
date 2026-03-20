from db import engine
from sqlalchemy import text
import bcrypt

def crear_admin():
    with engine.connect() as conn:

        result = conn.execute(text("""
            SELECT COUNT(*) FROM usuarios WHERE rol = 'ADMIN'
        """))
        existe = result.scalar()

        if existe > 0:
            print("Admin ya existe")
            return

        password = "admin123".encode()
        hash_pw = bcrypt.hashpw(password, bcrypt.gensalt()).decode()

        conn.execute(text("""
            INSERT INTO usuarios (username, password_hash, rol)
            VALUES ('admin', :password, 'ADMIN')
        """), {"password": hash_pw})

        conn.commit()
        print("Admin creado")

if __name__ == "__main__":
    crear_admin()
