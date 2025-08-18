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



use prueba_flask;
CREATE TABLE solicitudes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ciudadano_id INT,
    tipo_solicitud_id int,
    fecha_solicitud DATE,
    estado_solicitud varchar(40),
    FOREIGN KEY (ciudadano_id) REFERENCES ciudadanos(id),
    FOREIGN KEY (tramites_id) REFERENCES tramites(id),
	FOREIGN KEY (tipo_solicitud_id) REFERENCES tipo_solicitud(id)
);

insert into solicitudes
(ciudadano_id, fecha_solicitud, estado_solicitud) values
(4,4,'2025-08-14','Pendiente');

select * from ciudadanos;
select * from tramites;

use prueba_flask;
create table tipos_solicitud(
id_tipo int,
tipo_solicitud varchar(30)
); 

use prueba_flask;
create table solicitud_Tram(
id_sol_tram INT AUTO_INCREMENT PRIMARY KEY,
tramites_id int,
ciudadanos_id int,
modalidad varchar(40),
costo float,
estado varchar(20),
tipo_tramite varchar(100),
dependencia varchar(100),
vigencia int,
documenti_expide varchar(100),
formato_pago varchar(100),
FOREIGN KEY (tramites_id) REFERENCES tramites(id),
FOREIGN KEY (ciudadanos_id) REFERENCES ciudadanos(id)
);

use prueba_flask;
insert into solicitud_tram values (1,5,4,'Presencial',200,'En proceso','Tramite',
'',5,'Credencial','Efectivo');

select * from tramites;

use prueba_flask;
create table solicitud_Serv(
id_sol_Ser INT AUTO_INCREMENT PRIMARY KEY,
servicios_id int,
ciudadanos_id int,
nombre varchar (100),
costo float,
estado varchar(20),
tipo_tramite varchar(100),
formato_pago varchar(100),
FOREIGN KEY (servicios_id) REFERENCES servicios(id),
FOREIGN KEY (ciudadanos_id) REFERENCES ciudadanos(id)
);


use prueba_flask;
insert into solicitud_Serv values (1,8,4,'Toma de agua',50,'Activo','Servicio','Efectivo');

insert into solicitudes_tramite  
(id_tipo,tipo_solicitud) values
(1,'Tramite');


use prueba_flask;
create table solicitud_apoyo(
id_sol_apoyo INT AUTO_INCREMENT PRIMARY KEY,
apoyos_id int,
ciudadanos_id int,
nombre varchar (100),
descripcion varchar(100),
fecha_solicitud date,
costo float,
estado varchar(20),
tipo_tramite varchar(100),
formato_pago varchar(100),
FOREIGN KEY (apoyos_id) REFERENCES apoyos(id),
FOREIGN KEY (ciudadanos_id) REFERENCES ciudadanos(id)
);

create table tipo_tramite(
id_tipo_tramite INT AUTO_INCREMENT PRIMARY KEY,
tipo_tramite varchar(100)
);

insert into tipo_tramite values (3,'Apoyo');



use prueba_flask;
insert into solicitud_apoyo values (1,3,4,'gas','hwvdhgwcvdwdhgwv',NOW(),66,'Activo','Apoyo','Efectivo');

select * from tipo_tramite;
use prueba_flask;
CREATE TABLE solicitudes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ciudadano_id INT,
    tipo_solicitud_id int,
    fecha_solicitud DATE,
    estado_solicitud varchar(40),
    FOREIGN KEY (ciudadano_id) REFERENCES ciudadanos(id),
    FOREIGN KEY (tramites_id) REFERENCES tramites(id),
	FOREIGN KEY (tipo_solicitud_id) REFERENCES tipo_solicitud(id)
);

insert into solicitudes
(ciudadano_id, fecha_solicitud, estado_solicitud) values
(4,4,'2025-08-14','Pendiente');

select * from ciudadanos;
select * from tramites;

use prueba_flask;
create table tipos_solicitud(
id_tipo int,
tipo_solicitud varchar(30)
); 

use prueba_flask;
create table solicitud_Tram(
id_sol_tram INT AUTO_INCREMENT PRIMARY KEY,
tramites_id int,
ciudadanos_id int,
modalidad varchar(40),
costo float,
estado varchar(20),
tipo_tramite varchar(100),
dependencia varchar(100),
vigencia int,
documenti_expide varchar(100),
formato_pago varchar(100),
FOREIGN KEY (tramites_id) REFERENCES tramites(id),
FOREIGN KEY (ciudadanos_id) REFERENCES ciudadanos(id)
);

use prueba_flask;
insert into solicitud_tram values (1,5,4,'Presencial',200,'En proceso','Tramite',
'',5,'Credencial','Efectivo');

select * from tramites;

use prueba_flask;
create table solicitud_Serv(
id_sol_Ser INT AUTO_INCREMENT PRIMARY KEY,
servicios_id int,
ciudadanos_id int,
nombre varchar (100),
costo float,
estado varchar(20),
tipo_tramite varchar(100),
formato_pago varchar(100),
FOREIGN KEY (servicios_id) REFERENCES servicios(id),
FOREIGN KEY (ciudadanos_id) REFERENCES ciudadanos(id)
);


use prueba_flask;
insert into solicitud_Serv values (1,8,4,'Toma de agua',50,'Activo','Servicio','Efectivo');

insert into solicitudes_tramite  
(id_tipo,tipo_solicitud) values
(1,'Tramite');


use prueba_flask;
create table solicitud_apoyo(
id_sol_apoyo INT AUTO_INCREMENT PRIMARY KEY,
apoyos_id int,
ciudadanos_id int,
nombre varchar (100),
descripcion varchar(100),
fecha_solicitud date,
costo float,
estado varchar(20),
tipo_tramite varchar(100),
formato_pago varchar(100),
FOREIGN KEY (apoyos_id) REFERENCES apoyos(id),
FOREIGN KEY (ciudadanos_id) REFERENCES ciudadanos(id)
);

create table tipo_tramite(
id_tipo_tramite INT AUTO_INCREMENT PRIMARY KEY,
tipo_tramite varchar(100)
);

insert into tipo_tramite values (3,'Apoyo');



use prueba_flask;
insert into solicitud_apoyo values (1,3,4,'gas','hwvdhgwcvdwdhgwv',NOW(),66,'Activo','Apoyo','Efectivo');

select * from tipo_tramite;
