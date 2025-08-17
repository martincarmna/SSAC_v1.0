CREATE TABLE tramites (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    dependencia VARCHAR(100),
    modalidad VARCHAR(50),
    tipo_tramite VARCHAR(100),
    costo DECIMAL(10,2),
    formato_pago VARCHAR(100),
    estado VARCHAR(20),
    documento_expide VARCHAR(100),
    vigencia VARCHAR(50)
);
CREATE TABLE servicios (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(100) NOT NULL,
  tipo_servicio VARCHAR(100),
  costo DECIMAL(10,2),
  estado VARCHAR(50)
);
-- Crear base de datos
CREATE DATABASE IF NOT EXISTS prueba_flask;
USE prueba_flask;

-- Crear tabla ciudadanos
CREATE TABLE IF NOT EXISTS ciudadanos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    apellido_paterno VARCHAR(100),
    apellido_materno VARCHAR(100),
    fecha_nacimiento DATE,
    curp VARCHAR(18),
    rfc VARCHAR(13),
    correo VARCHAR(150),
    domicilio VARCHAR(255),
    celular VARCHAR(15),
    cp VARCHAR(10),
    genero VARCHAR(10)
);

-- Borrar tabla usuarios si ya existía mal definida
DROP TABLE IF EXISTS usuarios;

-- Crear tabla usuarios correctamente
CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario VARCHAR(100) NOT NULL,
    contrasena VARCHAR(100) NOT NULL
);

-- Insertar usuario de prueba
INSERT INTO usuarios (usuario, contrasena)
VALUES ('admi', '1234');

CREATE TABLE apoyos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    categoria VARCHAR(50),
    fecha_inicio DATE,
    fecha_vencimiento DATE,
    estado VARCHAR(20),
    imagen VARCHAR(255)
);


CREATE TABLE solicitudes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ciudadano_id INT,
    apoyo_id INT,
    fecha_solicitud DATE,
    FOREIGN KEY (ciudadano_id) REFERENCES ciudadanos(id),
    FOREIGN KEY (apoyo_id) REFERENCES apoyos(id)
);
