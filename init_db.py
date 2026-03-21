from db import engine
from sqlalchemy import text

def crear_tablas():
    with engine.connect() as conn:

        # PROPIEDADES
        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS propiedades (
            id SERIAL PRIMARY KEY,
            numero_propiedad INT UNIQUE NOT NULL,
            tipo VARCHAR(10) NOT NULL, -- CASA o LOTE
            estado VARCHAR(20) DEFAULT 'ACTIVO',
            observacion TEXT
        );
        """))

        # PROPIETARIOS
        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS propietarios (
            id SERIAL PRIMARY KEY,
            nombre VARCHAR(150),
            cedula VARCHAR(20),
            telefono VARCHAR(20),
            email VARCHAR(100),
            fecha_nacimiento DATE
        );
        """))

        # RELACION PROPIEDAD - PROPIETARIO (HISTORICO)
        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS propiedad_propietario (
            id SERIAL PRIMARY KEY,
            propiedad_id INT REFERENCES propiedades(id),
            propietario_id INT REFERENCES propietarios(id),
            fecha_inicio DATE,
            fecha_fin DATE
        );
        """))

        # ALICUOTAS
        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS alicuotas (
            id SERIAL PRIMARY KEY,
            propiedad_id INT REFERENCES propiedades(id),
            anio INT,
            mes INT,
            valor DECIMAL(10,2),
            estado VARCHAR(20) DEFAULT 'PENDIENTE'
        );
        """))

        # PAGOS
        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS pagos (
            id SERIAL PRIMARY KEY,
            propiedad_id INT REFERENCES propiedades(id),
            fecha_pago DATE,
            monto DECIMAL(10,2),
            metodo_pago VARCHAR(50),
            observacion TEXT
        );
        """))

        # PROVEEDORES
        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS proveedores (
            id SERIAL PRIMARY KEY,
            nombre VARCHAR(150),
            contacto VARCHAR(100),
            telefono VARCHAR(20)
        );
        """))

        # GASTOS
        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS gastos (
            id SERIAL PRIMARY KEY,
            proveedor_id INT REFERENCES proveedores(id),
            fecha DATE,
            concepto TEXT,
            monto DECIMAL(10,2),
            metodo_pago VARCHAR(50),
            observacion TEXT
        );
        """))

        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id SERIAL PRIMARY KEY,
            username VARCHAR(50) UNIQUE,
            password_hash TEXT,
            rol VARCHAR(20), -- ADMIN / PROPIETARIO
            propiedad_id INT REFERENCES propiedades(id),
            activo BOOLEAN DEFAULT TRUE
        );
        """))

        conn.execute(text("""
        ALTER TABLE alicuotas
        ADD COLUMN IF NOT EXISTS periodo VARCHAR(7);
        """))

        conn.execute(text("""
        ALTER TABLE alicuotas
        ADD COLUMN IF NOT EXISTS es_asociado BOOLEAN;
        """))

        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS alicuotas (
            id SERIAL PRIMARY KEY,
            propiedad_id INT REFERENCES propiedades(id),
            anio INT,
            mes INT,
            periodo VARCHAR(7), -- ej: 2023-01
            valor NUMERIC(10,2),
            estado VARCHAR(20) DEFAULT 'PENDIENTE',
            fecha_pago DATE,
            es_asociado BOOLEAN
        );
        """))
        
        conn.commit()

    print("Tablas creadas correctamente")

if __name__ == "__main__":
    crear_tablas()
