from flask import Blueprint, jsonify, request

from ..utils import validar_entero, validar_minimo
from ..services.categorias import (
    listar_categorias,
    buscar_categoria_por_id_o_error,
    crear_categoria,
    actualizar_categoria,
    eliminar_categoria_por_id,
)

categorias_bp = Blueprint('categorias', __name__)


def _status_de_error(error: ValueError) -> int:
    return error.args[1] if len(error.args) > 1 else 400


@categorias_bp.route('/categorias', methods=['GET'])
def get_categorias():
    """Lista todas las categorias (publico)."""
    return jsonify(listar_categorias())


@categorias_bp.route('/categorias/<categoria_id>', methods=['GET'])
def get_categoria(categoria_id):
    try:
        id_validado = validar_minimo(validar_entero(categoria_id, 'id'), 1, 'id')
        categoria   = buscar_categoria_por_id_o_error(id_validado)
    except ValueError as error:
        return jsonify(error.args[0]), _status_de_error(error)

    return jsonify(categoria)


@categorias_bp.route('/categorias', methods=['POST'])
def post_categoria():
    body = request.get_json(silent=True)

    try:
        categoria = crear_categoria(body)
    except ValueError as error:
        return jsonify(error.args[0]), _status_de_error(error)

    return jsonify(categoria), 201


@categorias_bp.route('/categorias/<categoria_id>', methods=['PUT'])
def put_categoria(categoria_id):
    body = request.get_json(silent=True)

    try:
        id_validado = validar_minimo(validar_entero(categoria_id, 'id'), 1, 'id')
        categoria   = actualizar_categoria(id_validado, body)
    except ValueError as error:
        return jsonify(error.args[0]), _status_de_error(error)

    return jsonify(categoria)


@categorias_bp.route('/categorias/<categoria_id>', methods=['DELETE'])
def delete_categoria(categoria_id):
    try:
        id_validado = validar_minimo(validar_entero(categoria_id, 'id'), 1, 'id')
        eliminar_categoria_por_id(id_validado)
    except ValueError as error:
        return jsonify(error.args[0]), _status_de_error(error)

    return '', 204
