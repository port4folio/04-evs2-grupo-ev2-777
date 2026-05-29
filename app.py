import sqlite3

class SistemaRRHH:
    def __init__(self, db_name="erp_seguridad.db"):  # <-- CORREGIDO DE VERDAD: __init__
        self.db_name = db_name
        self.inicializar_base_de_datos()

    def inicializar_base_de_datos(self):
        """Crea la tabla automáticamente si no existe."""
        conexion = sqlite3.connect(self.db_name)
        cursor = conexion.cursor()
        
        # --- TABLA DE PERSONAL ---
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
        
        # --- TABLA DE CONTRATOS Y SUELDOS ---
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS contratos_seguridad (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                rut_empleado VARCHAR(12) NOT NULL,
                tipo_contrato VARCHAR(50) NOT NULL,
                sueldo_base INTEGER NOT NULL,
                anexos TEXT,
                FOREIGN KEY (rut_empleado) REFERENCES personal_seguridad(rut)
            )
        """)
        
        conexion.commit()
        conexion.close()

    def registrar_personal(self, rut, nombre, apellido, rol, fecha_ingreso):
        """Inserta una nueva ficha de personal en el sistema (SL-5)."""
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

    def listar_personal(self):
        """SL-7: Consulta y muestra en pantalla a todo el personal de seguridad."""
        try:
            conexion = sqlite3.connect(self.db_name)
            cursor = conexion.cursor()
            cursor.execute("SELECT rut, nombre, apellido, rol, fecha_ingreso, activo FROM personal_seguridad")
            empleados = cursor.fetchall()

            print("\n==================================================")
            print("       NÓMINA DE PERSONAL DE SEGURIDAD - ERP      ")
            print("==================================================")
            if not empleados:
                print("No hay personal registrado en el sistema.")
            for emp in empleados:
                estado = "Activo" if emp[5] == 1 else "Inactivo"
                print(f"RUT: {emp[0]} | {emp[1]} {emp[2]} | Rol: {emp[3]} | Ingreso: {emp[4]} | Estado: {estado}")
            print("==================================================\n")
        except sqlite3.Error as e:
            print(f"Error al leer los datos: {e}")
        finally:
            conexion.close()

    def actualizar_rol_personal(self, rut, nuevo_rol):
        """SL-7: Modifica el rol de un trabajador existente mediante su RUT."""
        try:
            conexion = sqlite3.connect(self.db_name)
            cursor = conexion.cursor()
            cursor.execute("""
                UPDATE personal_seguridad  
                SET rol = ? 
                WHERE rut = ?
            """, (nuevo_rol, rut))
            conexion.commit()
            
            if cursor.rowcount > 0:
                print(f"¡Éxito! El rol del RUT {rut} fue actualizado a '{nuevo_rol}'.")
            else:
                print(f"Advertencia: No se encontró ningún empleado con el RUT {rut}.")
        except sqlite3.Error as e:
            print(f"Error al actualizar el rol: {e}")
        finally:
            conexion.close()

    def registrar_contrato(self, rut_empleado, tipo_contrato, sueldo_base, anexos):
        """Asocia un contrato de trabajo y sueldo a un empleado mediante su RUT."""
        try:
            conexion = sqlite3.connect(self.db_name)
            cursor = conexion.cursor()
            cursor.execute("""
                INSERT INTO contratos_seguridad (rut_empleado, tipo_contrato, sueldo_base, anexos)
                VALUES (?, ?, ?, ?)
            """, (rut_empleado, tipo_contrato, sueldo_base, anexos))
            conexion.commit()
            print(f"¡Éxito! Contrato '{tipo_contrato}' asignado al RUT {rut_empleado}.")
        except sqlite3.Error as e:
            print(f"Error al registrar el contrato: {e}")
        finally:
            conexion.close()

    def listar_contratos(self):
        """Consulta y despliega en pantalla la nómina de sueldos y anexos."""
        try:
            conexion = sqlite3.connect(self.db_name)
            cursor = conexion.cursor()
            cursor.execute("SELECT id, rut_empleado, tipo_contrato, sueldo_base, anexos FROM contratos_seguridad")
            contratos = cursor.fetchall()

            print("\n==================================================")
            print("       NÓMINA DE CONTRATOS Y SUELDOS - ERP        ")
            print("==================================================")
            if not contratos:
                print("No hay contratos registrados en el sistema.")
            for con in contratos:
                print(f"ID: {con[0]} | Empleado RUT: {con[1]} | Contrato: {con[2]} | Sueldo: ${con[3]:,} | Detalle: {con[4]}")
            print("==================================================\n")
        except sqlite3.Error as e:
            print(f"Error al leer los contratos: {e}")
        finally:
            conexion.close()


if __name__ == "__main__":  # <-- CORREGIDO DE VERDAD: __name__ y __main__
    sistema = SistemaRRHH()
    
    print("--- Registrando Personal de Seguridad Actividad SL-5 ---")
    sistema.registrar_personal(
        rut="12.345.678-9", 
        nombre="Juan", 
        apellido="Pérez", 
        rol="Guardia", 
        fecha_ingreso="2026-05-28"
    )
    
    print("--- Ejecutando Nuevas Consultas Actividad SL-7 ---")
    sistema.registrar_personal(
        rut="18.765.432-1", 
        nombre="María", 
        apellido="Soto", 
        rol="Supervisor", 
        fecha_ingreso="2026-05-28"
    )
    
    sistema.listar_personal()
    sistema.actualizar_rol_personal(rut="12.345.678-9", nuevo_rol="Jefe de Turno")
    sistema.listar_personal()

    print("--- Asociando Contratos de Trabajo Actividad SL-6 ---")
    
    # 1. Asociamos un contrato a Juan Pérez usando su RUT
    sistema.registrar_contrato(
        rut_empleado="12.345.678-9",
        tipo_contrato="Indefinido",
        sueldo_base=650000,
        anexos="Bono nocturno por turnos y asignación de movilización."
    )
    
    # 2. Asociamos un contrato a María Soto usando su RUT
    sistema.registrar_contrato(
        rut_empleado="18.765.432-1",
        tipo_contrato="Plazo Fijo",
        sueldo_base=850000,
        anexos="Seguro complementario de salud activo."
    )
    
    # 3. Mostramos la nómina de contratos y remuneraciones para evidenciar el cumplimiento
    sistema.listar_contratos()