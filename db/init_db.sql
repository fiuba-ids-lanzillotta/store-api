-- =============================================================
--  Store - Script DDL + datos semilla para MySQL
-- =============================================================
--  docker-compose lo ejecuta automaticamente al levantar el contenedor
--  (volumen montado en /docker-entrypoint-initdb.d).
--
--  La base `store` la crea el propio contenedor via MYSQL_DATABASE.
-- =============================================================

CREATE TABLE IF NOT EXISTS categorias (
    id          INT          AUTO_INCREMENT PRIMARY KEY,
    nombre      VARCHAR(50)  NOT NULL UNIQUE,
    descripcion VARCHAR(200) NOT NULL DEFAULT '',
    creado_en   DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS productos (
    id           INT            AUTO_INCREMENT PRIMARY KEY,
    nombre       VARCHAR(100)   NOT NULL,
    descripcion  VARCHAR(500)   NOT NULL DEFAULT '',
    precio       DECIMAL(10, 2) NOT NULL DEFAULT 0,
    stock        INT            NOT NULL DEFAULT 0,
    imagen_url   VARCHAR(500)   NOT NULL DEFAULT '',
    categoria_id INT            NOT NULL,
    creado_en    DATETIME       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_producto_categoria FOREIGN KEY (categoria_id)
        REFERENCES categorias(id),
    INDEX idx_producto_categoria (categoria_id)
);

-- ---------------------------------------------------------------
--  Datos semilla (idempotentes: solo si la tabla esta vacia)
-- ---------------------------------------------------------------

INSERT INTO categorias (nombre, descripcion)
SELECT 'Electronica', 'Dispositivos y accesorios electronicos'
WHERE NOT EXISTS (SELECT 1 FROM categorias);

INSERT INTO categorias (nombre, descripcion)
SELECT 'Hogar', 'Articulos para el hogar'
WHERE NOT EXISTS (SELECT 1 FROM categorias WHERE nombre = 'Hogar');

INSERT INTO categorias (nombre, descripcion)
SELECT 'Indumentaria', 'Ropa y accesorios'
WHERE NOT EXISTS (SELECT 1 FROM categorias WHERE nombre = 'Indumentaria');

INSERT INTO productos (nombre, descripcion, precio, stock, imagen_url, categoria_id)
SELECT 'Auriculares Bluetooth', 'Auriculares inalambricos con estuche de carga', 25999.99, 15, '', c.id
  FROM categorias c
 WHERE c.nombre = 'Electronica'
   AND NOT EXISTS (SELECT 1 FROM productos);

INSERT INTO productos (nombre, descripcion, precio, stock, imagen_url, categoria_id)
SELECT 'Teclado Mecanico', 'Teclado mecanico RGB switches rojos', 45999.00, 8, '', c.id
  FROM categorias c
 WHERE c.nombre = 'Electronica'
   AND NOT EXISTS (SELECT 1 FROM productos WHERE nombre = 'Teclado Mecanico');

INSERT INTO productos (nombre, descripcion, precio, stock, imagen_url, categoria_id)
SELECT 'Lampara de Escritorio', 'Lampara LED con intensidad regulable', 18500.50, 20, '', c.id
  FROM categorias c
 WHERE c.nombre = 'Hogar'
   AND NOT EXISTS (SELECT 1 FROM productos WHERE nombre = 'Lampara de Escritorio');

INSERT INTO productos (nombre, descripcion, precio, stock, imagen_url, categoria_id)
SELECT 'Remera Basica', 'Remera de algodon unisex', 9999.99, 50, '', c.id
  FROM categorias c
 WHERE c.nombre = 'Indumentaria'
   AND NOT EXISTS (SELECT 1 FROM productos WHERE nombre = 'Remera Basica');
