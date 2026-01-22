CREATE DATABASE oscontrol;

USE oscontrol;

CREATE TABLE clientes (
id INT PRIMARY KEY AUTO_INCREMENT,
nome VARCHAR(80) NOT NULL,
telefone VARCHAR(50),
email VARCHAR(100),
documento VARCHAR(100),
endereco VARCHAR(150)
);

CREATE TABLE veiculos (
id INT PRIMARY KEY AUTO_INCREMENT,
id_clientes INT,
modelo VARCHAR(80) NOT NULL,
marca VARCHAR(50),
ano VARCHAR(100),
placa VARCHAR(50),
observacoes VARCHAR(200)
);

CREATE TABLE mecanicos (
id INT PRIMARY KEY AUTO_INCREMENT,
nome VARCHAR(80) NOT NULL,
especialidades VARCHAR(50)
);

CREATE TABLE os (
id INT PRIMARY KEY AUTO_INCREMENT,
id_clientes INT,
id_veiculos INT,
data_os DATE DEFAULT(CURRENT_DATE()),
status_os VARCHAR(50),
problema VARCHAR(100),
diagnostico VARCHAR(100),
mecanico VARCHAR(50),
itens_os VARCHAR(200),
valor_total VARCHAR(50),
observacoes VARCHAR(200)
);

DROP TABLE clientes;

SELECT * FROM clientes;

INSERT INTO clientes(nome, telefone, email, documento, endereco) VALUES ('Joana', '(85)94754-2233', 'joana@gmail.com', '800.833.333-44', 'rua 77 - Maraponga');


DB_HOST= localhost
DB_USER= root
DB_PASSWORD= 
DB_NAME= oscontrol
FLASK_SECRET_KEY= 12345678#