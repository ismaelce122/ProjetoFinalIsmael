CREATE DATABASE oscontrol;

USE oscontrol;

CREATE TABLE clientes (
id INT PRIMARY KEY AUTO_INCREMENT,
nome VARCHAR(100) NOT NULL,
telefone VARCHAR(100) NOT NULL,
email VARCHAR(100) NOT NULL UNIQUE,
documento VARCHAR(100) NOT NULL,
endereco VARCHAR(100) NOT NULL,
senha VARCHAR(500) NOT NULL,
criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE veiculos (
id INT PRIMARY KEY AUTO_INCREMENT,
id_clientes INT,
modelo VARCHAR(50) NOT NULL,
marca VARCHAR(50) NOT NULL,
ano VARCHAR(50) NOT NULL,
placa VARCHAR(50) NOT NULL,
observacoes VARCHAR(150)
);

CREATE TABLE mecanicos (
id INT PRIMARY KEY AUTO_INCREMENT,
nome VARCHAR(100) NOT NULL,
especialidades VARCHAR(100) NOT NULL
);

CREATE TABLE os (
id INT PRIMARY KEY AUTO_INCREMENT,
id_clientes INT,
id_veiculos INT,
data_os DATE DEFAULT(CURRENT_DATE()),
status_os VARCHAR(100) NOT NULL,
problema VARCHAR(150) NOT NULL,
diagnostico VARCHAR(150) NOT NULL,
mecanico VARCHAR(100) NOT NULL,
itens_os VARCHAR(100) NOT NULL,
valor_total VARCHAR(100) NOT NULL,
observacoes VARCHAR(150)
);

DROP TABLE clientes;

SELECT * FROM clientes;

INSERT INTO clientes(nome, telefone, email, documento, endereco) VALUES ('Joana', '(85)94754-2233', 'joana@gmail.com', '800.833.333-44', 'rua 77 - Maraponga');


DB_HOST= localhost
DB_USER= root
DB_PASSWORD= 
DB_NAME= oscontrol
FLASK_SECRET_KEY= 12345678#