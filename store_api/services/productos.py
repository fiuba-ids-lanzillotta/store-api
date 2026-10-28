from ..constants import (
    ERROR_CODE_PRODUCTO_NOT_FOUND,
    ERROR_CODE_CATEGORIA_NOT_FOUND,
)
from ..utils import construir_error_api
from ..validators.productos import validar_body_producto
from .. import db


def construir_producto_dto(producto: dict) -> dict:
    """DTO publico de un producto, con la categoria anidada."""
    return {
        'id':          producto['id'],
        'nombre':      producto['nombre'],
        'descripcion': producto['descripcion'],
        'precio':      float(producto['precio']),
        'stock':       producto['stock'],
        'imagen_url':  producto['imagen_url'],
        'categoria': {
            'id':     producto['categoria_id'],
            'nombre': producto['categoria_nombre'],
        },
    }


def listar_productos(categoria_id: int = None, texto: str = None) -> list[dict]:
    filas = db.listar_productos(categoria_id=categoria_id, texto=texto)

    return [construir_producto_dto(fila) for fila in filas]


def buscar_producto_por_id(producto_id: int) -> dict:
    producto = db.obtener_producto_por_id(producto_id)

    if not producto:
        return {}

    return construir_producto_dto(producto)


def buscar_producto_por_id_o_error(producto_id: int) -> dict:
    producto = buscar_producto_por_id(producto_id)

    if not producto:
        raise ValueError(construir_error_api(
            code=ERROR_CODE_PRODUCTO_NOT_FOUND,
            message='Producto no encontrado',
            description=f"No existe un producto con id '{producto_id}'"
        ), 404)

    return producto


def crear_producto(body: dict) -> dict:
    datos = validar_body_producto(body)
    _validar_categoria_existente(datos['categoria_id'])

    producto_id = db.insertar_producto(datos)

    return buscar_producto_por_id_o_error(producto_id)


def actualizar_producto(producto_id: int, body: dict) -> dict:
    buscar_producto_por_id_o_error(producto_id)

    datos = validar_body_producto(body)
    _validar_categoria_existente(datos['categoria_id'])

    db.actualizar_producto(producto_id, datos)

    return buscar_producto_por_id_o_error(producto_id)


def eliminar_producto_por_id(producto_id: int) -> None:
    buscar_producto_por_id_o_error(producto_id)
    db.eliminar_producto(producto_id)


def _validar_categoria_existente(categoria_id: int) -> None:
    """La FK exige que la categoria exista; lo validamos para dar un 400 claro."""
    if not db.obtener_categoria_por_id(categoria_id):
        raise ValueError(construir_error_api(
            code=ERROR_CODE_CATEGORIA_NOT_FOUND,
            message='Categoria no encontrada',
            description=f"No existe una categoria con id '{categoria_id}'"
        ))
