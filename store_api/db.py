from sqlalchemy import create_engine, text

from .constants import DB_URL

# Motor de conexion compartido por toda la aplicacion.
# El pool de conexiones lo maneja SQLAlchemy automaticamente.
motor = create_engine(DB_URL, pool_pre_ping=True)


# ---------------------------------------------------------------
# Funciones de soporte
# ---------------------------------------------------------------

def fila_a_dict(fila) -> dict:
    """Convierte una fila del resultado de una query en un diccionario."""
    return dict(fila._mapping)


def ejecutar_consulta(sql: str, parametros: dict = None) -> list[dict]:
    """Ejecuta una SELECT y devuelve todas las filas como lista de dicts."""
    with motor.connect() as conexion:
        resultado = conexion.execute(text(sql), parametros or {})

        return [fila_a_dict(fila) for fila in resultado]


def ejecutar_mutacion(sql: str, parametros: dict = None) -> int:
    """
    Ejecuta un INSERT, UPDATE o DELETE y hace commit.
    Retorna el id autoincremental generado por el INSERT (0 si no aplica).
    """
    with motor.begin() as conexion:
        resultado = conexion.execute(text(sql), parametros or {})

        return resultado.lastrowid or 0


# ---------------------------------------------------------------
# Queries de categorias
# ---------------------------------------------------------------

def listar_categorias() -> list[dict]:
    sql = """
        SELECT c.id, c.nombre, c.descripcion, COUNT(p.id) AS cantidad_productos
          FROM categorias c
          LEFT JOIN productos p ON p.categoria_id = c.id
         GROUP BY c.id, c.nombre, c.descripcion
         ORDER BY c.nombre
    """

    return ejecutar_consulta(sql)


def obtener_categoria_por_id(categoria_id: int) -> dict:
    sql   = 'SELECT id, nombre, descripcion FROM categorias WHERE id = :id'
    filas = ejecutar_consulta(sql, {'id': categoria_id})

    return filas[0] if filas else {}


def obtener_categoria_por_nombre(nombre: str) -> dict:
    sql   = 'SELECT id, nombre, descripcion FROM categorias WHERE nombre = :nombre'
    filas = ejecutar_consulta(sql, {'nombre': nombre})

    return filas[0] if filas else {}


def insertar_categoria(nombre: str, descripcion: str) -> int:
    sql = """
        INSERT INTO categorias (nombre, descripcion)
        VALUES (:nombre, :descripcion)
    """

    return ejecutar_mutacion(sql, {
        'nombre':      nombre,
        'descripcion': descripcion,
    })


def actualizar_categoria(categoria_id: int, nombre: str, descripcion: str) -> None:
    sql = """
        UPDATE categorias
           SET nombre = :nombre,
               descripcion = :descripcion
         WHERE id = :id
    """
    ejecutar_mutacion(sql, {
        'id':          categoria_id,
        'nombre':      nombre,
        'descripcion': descripcion,
    })


def eliminar_categoria(categoria_id: int) -> None:
    sql = 'DELETE FROM categorias WHERE id = :id'
    ejecutar_mutacion(sql, {'id': categoria_id})


def contar_productos_de_categoria(categoria_id: int) -> int:
    sql = 'SELECT COUNT(*) AS total FROM productos WHERE categoria_id = :id'
    filas = ejecutar_consulta(sql, {'id': categoria_id})

    return filas[0]['total'] if filas else 0


# ---------------------------------------------------------------
# Queries de productos
# ---------------------------------------------------------------

def listar_productos(categoria_id: int = None, texto: str = None) -> list[dict]:
    """
    Lista productos con el nombre de su categoria (JOIN).
    Filtros opcionales: por categoria y por texto en el nombre.
    """
    sql = """
        SELECT p.id, p.nombre, p.descripcion, p.precio, p.stock,
               p.imagen_url, p.categoria_id, c.nombre AS categoria_nombre
          FROM productos p
          JOIN categorias c ON c.id = p.categoria_id
         WHERE (:categoria_id IS NULL OR p.categoria_id = :categoria_id)
           AND (:texto IS NULL OR p.nombre LIKE CONCAT('%', :texto, '%'))
         ORDER BY p.nombre
    """

    return ejecutar_consulta(sql, {
        'categoria_id': categoria_id,
        'texto':        texto,
    })


def obtener_producto_por_id(producto_id: int) -> dict:
    sql = """
        SELECT p.id, p.nombre, p.descripcion, p.precio, p.stock,
               p.imagen_url, p.categoria_id, c.nombre AS categoria_nombre
          FROM productos p
          JOIN categorias c ON c.id = p.categoria_id
         WHERE p.id = :id
    """
    filas = ejecutar_consulta(sql, {'id': producto_id})

    return filas[0] if filas else {}


def insertar_producto(datos: dict) -> int:
    sql = """
        INSERT INTO productos (nombre, descripcion, precio, stock, imagen_url, categoria_id)
        VALUES (:nombre, :descripcion, :precio, :stock, :imagen_url, :categoria_id)
    """

    return ejecutar_mutacion(sql, datos)


def actualizar_producto(producto_id: int, datos: dict) -> None:
    sql = """
        UPDATE productos
           SET nombre = :nombre,
               descripcion = :descripcion,
               precio = :precio,
               stock = :stock,
               imagen_url = :imagen_url,
               categoria_id = :categoria_id
         WHERE id = :id
    """
    ejecutar_mutacion(sql, {**datos, 'id': producto_id})


def eliminar_producto(producto_id: int) -> None:
    sql = 'DELETE FROM productos WHERE id = :id'
    ejecutar_mutacion(sql, {'id': producto_id})
