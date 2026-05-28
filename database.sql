-- Crear tabla para registrar el personal de seguridad (HU01 / SL-5)
CREATE TABLE IF NOT EXISTS personal_seguridad (
    rut VARCHAR(12) PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    apellido VARCHAR(50) NOT NULL,
    rol VARCHAR(30) NOT NULL,          -- 'Guardia', 'Supervisor', 'Admin RRHH'
    fecha_ingreso DATE NOT NULL,
    activo BOOLEAN DEFAULT TRUE,
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);