CREATE DATABASE biblioteca;
USE biblioteca;

SELECT * FROM usuario;

/*
CREATE TABLE libro (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(50),
    autor VARCHAR(50),
    genero VARCHAR(40),
    editorial VARCHAR(50),
    sinopsis VARCHAR(1000),
    fecha_publicacion DATE,
    estado VARCHAR(20)
);

CREATE TABLE usuario(
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50),
    apellido VARCHAR(50),
    user_name VARCHAR(50),
    email VARCHAR(100),
    contraseña VARCHAR(350)
);

CREATE TABLE prestamo (
    id INT AUTO_INCREMENT PRIMARY KEY,
    libro_id INT,
    usuario_id INT,
    fecha_prestamo DATE,
    fecha_devolucion DATE,
    FOREIGN KEY (libro_id) REFERENCES libro(id),
    FOREIGN KEY (usuario_id) REFERENCES usuario(id)
);
*/