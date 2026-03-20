from db import engine
from sqlalchemy import text

def cargar_propiedades():
    with engine.connect() as conn:

        # Verifica si ya existen datos
        result = conn.execute(text("SELECT COUNT(*) FROM propiedades"))
        total = result.scalar()

        if total > 0:
            print("Las propiedades ya están cargadas")
            return

        # Insertar 118 propiedades como CASA
        for i in range(1, 119):
            conn.execute(text("""
                INSERT INTO propiedades (numero_propiedad, tipo)
                VALUES (:numero, 'CASA')
            """), {
                "numero": i
            })

        conn.commit()
        print("118 propiedades creadas como CASA")

if __name__ == "__main__":
    cargar_propiedades()
