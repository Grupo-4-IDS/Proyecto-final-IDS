CREATE TABLE Usuarios (
    ID SERIAL PRIMARY KEY,
    usuario VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(50) NOT NULL UNIQUE,
    cuit_cuil VARCHAR(20) NOT NULL UNIQUE,
    contrasena VARCHAR(10) NOT NULL,
    fecha_registro DATE NOT NULL DEFAULT CURRENT_DATE
);

CREATE TABLE Causas (
    ID SERIAL PRIMARY KEY,
    fecha_creacion DATE NOT NULL DEFAULT CURRENT_DATE,
    descripcion TEXT NOT NULL,
    meta NUMERIC(11, 2) NOT NULL,
    foto TEXT,
    monto_recaudado NUMERIC(12, 2) DEFAULT 0
);