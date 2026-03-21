from db import engine
from sqlalchemy import text
from datetime import datetime

def generar_alicuotas():

    with engine.connect() as conn:

        # Verificar si ya existen
        total = conn.execute(text("SELECT COUNT(*) FROM alicuotas")).scalar()

        if total > 0:
            print("Ya existen alícuotas generadas")
            return

        propiedades = conn.execute(text("""
            SELECT id, tipo, es_asociado
            FROM propiedades
        """)).fetchall()

        fecha_inicio = datetime(2022, 9, 1)
        fecha_actual = datetime.now()

        fecha = fecha_inicio

        while fecha <= fecha_actual:

            anio = fecha.year
            mes = fecha.month
            periodo = f"{anio}-{str(mes).zfill(2)}"

            for p in propiedades:

                # REGLAS DE NEGOCIO
                if fecha < datetime(2023, 10, 1):
                    aplica = True  # todos
                else:
                    aplica = p.es_asociado  # solo asociados

                if not aplica:
                    continue

                # VALOR SEGÚN TIPO
                if p.tipo == "CASA":
                    valor = 20
                else:
                    valor = 10

                conn.execute(text("""
                    INSERT INTO alicuotas 
                    (propiedad_id, anio, mes, periodo, valor, es_asociado)
                    VALUES (:prop, :anio, :mes, :periodo, :valor, :asoc)
                """), {
                    "prop": p.id,
                    "anio": anio,
                    "mes": mes,
                    "periodo": periodo,
                    "valor": valor,
                    "asoc": aplica
                })

            # avanzar mes
            if mes == 12:
                fecha = datetime(anio + 1, 1, 1)
            else:
                fecha = datetime(anio, mes + 1, 1)

        conn.commit()
        print("Alícuotas generadas correctamente")

if __name__ == "__main__":
    generar_alicuotas()
