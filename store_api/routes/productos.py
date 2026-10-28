from flask import Blueprint, jsonify, request

from ..utils import validar_entero, validar_minimo, validar_string_opcional
from ..services.productos import (
    listar_productos,
    buscar_producto_por_id_o_error,
    crear_producto,
    actualizar_producto,
    eliminar_producto_por_id,
)

productos_bp = Blueprint('productos', __name__)


def _status_de_error(error: ValueError) -> int:
    return error.args[1] if len(error.args) > 1 else 400


@productos_bp.route('/productos', methods=['GET'])
def get_productos():
    """
    Lista los productos (publico). Filtros opcionales por query string:
    ?categoria_id=1  y/o  ?q=texto (busca en el nombre).
    """
    try:
        categoria_id = _parametro_opcional_entero('categoria_id')
        texto        = validar_string_opcional(request.args.get('q'), 'q') or None
    except ValueError as error:
        return jsonify(error.args[0]), _status_de_error(error)

    return jsonify(listar_productos(categoria_id=categoria_id, texto=texto))


@productos_bp.route('/productos/<producto_id>', methods=['GET'])
def get_producto(producto_id):
    try:
        id_validado = validar_minimo(validar_entero(producto_id, 'id'), 1, 'id')
        producto    = buscar_producto_por_id_o_error(id_validado)
    except ValueError as error:
        return jsonify(error.args[0]), _status_de_error(error)

    return jsonify(producto)


@productos_bp.route('/productos', methods=['POST'])
def post_producto():
    body = request.get_json(silent=True)

    try:
        producto = crear_producto(body)
    except ValueError as error:
        return jsonify(error.args[0]), _status_de_error(error)

    return jsonify(producto), 201


@productos_bp.route('/productos/<producto_id>', methods=['PUT'])
def put_producto(producto_id):
    body = request.get_json(silent=True)

    try:
        id_validado = validar_minimo(validar_entero(producto_id, 'id'), 1, 'id')
        producto    = actualizar_producto(id_validado, body)
    except ValueError as error:
        return jsonify(error.args[0]), _status_de_error(error)

    return jsonify(producto)


@productos_bp.route('/productos/<producto_id>', methods=['DELETE'])
def delete_producto(producto_id):
    try:
        id_validado = validar_minimo(validar_entero(producto_id, 'id'), 1, 'id')
        eliminar_producto_por_id(id_validado)
    except ValueError as error:
        return jsonify(error.args[0]), _status_de_error(error)

    return '', 204


def _parametro_opcional_entero(nombre: str):
    """Query param entero opcional: None si no viene, error si no es entero >= 1."""
    crudo = request.args.get(nombre)

    if crudo is None or crudo == '':
        return None

    return validar_minimo(validar_entero(crudo, nombre), 1, nombre)
