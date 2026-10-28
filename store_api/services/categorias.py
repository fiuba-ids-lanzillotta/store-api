from ..constants import (
    ERROR_CODE_CATEGORIA_NOT_FOUND,
    ERROR_CODE_CATEGORIA_CON_PRODUCTOS,
    ERROR_CODE_NOMBRE_YA_REGISTRADO,
)
from ..utils import construir_error_api
from ..validators.categorias import validar_body_categoria
from .. import db


def construir_categoria_dto(categoria: dict) -> dict:
    """DTO publico de una categoria."""
    dto = {
        'id':          categoria['id'],
        'nombre':      categoria['nombre'],
        'descripcion': categoria['descripcion'],
    }

    if 'cantidad_productos' in categoria:
        dto['cantidad_productos'] = categoria['cantidad_productos']

    return dto


def listar_categorias() -> list[dict]:
    return [construir_categoria_dto(fila) for fila in db.listar_categorias()]


def buscar_categoria_por_id(categoria_id: int) -> dict:
    categoria = db.obtener_categoria_por_id(categoria_id)

    if not categoria:
        return {}

    return construir_categoria_dto(categoria)


def buscar_categoria_por_id_o_error(categoria_id: int) -> dict:
    categoria = buscar_categoria_por_id(categoria_id)

    if not categoria:
        raise ValueError(construir_error_api(
            code=ERROR_CODE_CATEGORIA_NOT_FOUND,
            message='Categoria no encontrada',
            description=f"No existe una categoria con id '{categoria_id}'"
        ), 404)

    return categoria


def crear_categoria(body: dict) -> dict:
    datos = validar_body_categoria(body)
    _validar_nombre_disponible(datos['nombre'])

    categoria_id = db.insertar_categoria(datos['nombre'], datos['descripcion'])

    return buscar_categoria_por_id_o_error(categoria_id)


def actualizar_categoria(categoria_id: int, body: dict) -> dict:
    buscar_categoria_por_id_o_error(categoria_id)

    datos = validar_body_categoria(body)
    _validar_nombre_disponible(datos['nombre'], excluir_id=categoria_id)

    db.actualizar_categoria(categoria_id, datos['nombre'], datos['descripcion'])

    return buscar_categoria_por_id_o_error(categoria_id)


def eliminar_categoria_por_id(categoria_id: int) -> None:
    buscar_categoria_por_id_o_error(categoria_id)

    if db.contar_productos_de_categoria(categoria_id) > 0:
        raise ValueError(construir_error_api(
            code=ERROR_CODE_CATEGORIA_CON_PRODUCTOS,
            message='La categoria tiene productos asociados',
            description='Reasigna o elimina los productos antes de borrar la categoria'
        ), 409)

    db.eliminar_categoria(categoria_id)


def _validar_nombre_disponible(nombre: str, excluir_id: int = None) -> None:
    """El nombre es UNIQUE; lo chequeamos antes para responder 409 claro."""
    existente = db.obtener_categoria_por_nombre(nombre)

    if existente and existente['id'] != excluir_id:
        raise ValueError(construir_error_api(
            code=ERROR_CODE_NOMBRE_YA_REGISTRADO,
            message='Nombre ya registrado',
            description=f"Ya existe una categoria con el nombre '{nombre}'"
        ), 409)
