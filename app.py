import sqlite3

class SistemaRRHH:
    def __init__(self, db_name="erp_seguridad.db"):
        self.db_name = db_name
        self.inicializar_base_de_datos()

    def inicializar_base_de_datos(self):
        """Crea la tabla automáticamente si no existe."""
        conexion = sqlite3.connect(self.db_name)
        cursor = conexion.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS personal_seguridad (
                rut VARCHAR(12) PRIMARY KEY,
                nombre VARCHAR(50) NOT NULL,
                apellido VARCHAR(50) NOT NULL,
                rol VARCHAR(30) NOT NULL,
                fecha_ingreso TEXT NOT NULL,
                activo INTEGER DEFAULT 1
            )
        """)
        conexion.commit()
        conexion.close()

    def registrar_personal(self, rut, nombre, apellido, rol, fecha_ingreso):
        """Inserta una nueva ficha de personal en el sistema."""
        try:
            conexion = sqlite3.connect(self.db_name)
            cursor = conexion.cursor()
            cursor.execute("""
                INSERT INTO personal_seguridad (rut, nombre, apellido, rol, fecha_ingreso)
                VALUES (?, ?, ?, ?, ?)
            """, (rut, nombre, apellido, rol, fecha_ingreso))
            conexion.commit()
            print(f"¡Éxito! Empleado {nombre} {apellido} registrado correctamente.")
        except sqlite3.IntegrityError:
            print(f"Error: El RUT {rut} ya se encuentra registrado.")
        finally:
            conexion.close()


if __name__ == "__main__":
    sistema = SistemaRRHH()
    
    print("--- Registrando Personal de Seguridad Actividad SL-5 ---")
    sistema.registrar_personal(
        rut="12.345.678-9", 
        nombre="Juan", 
        apellido="Pérez", 
        rol="Guardia", 
        fecha_ingreso="2026-05-28"
    )