from ..constants import (
    PRODUCTO_NOMBRE_MAX_LEN,
    PRODUCTO_DESCRIPCION_MAX_LEN,
    PRODUCTO_IMAGEN_MAX_LEN,
    PRECIO_MIN,
    STOCK_MIN,
    ERROR_CODE_INVALID_BODY,
)
from ..utils import (
    construir_error_api,
    validar_string_no_vacio,
    validar_string_opcional,
    validar_largo_string,
    validar_entero,
    validar_decimal,
    validar_minimo,
)


def _validar_body_presente(body):
    if body is None:
        raise ValueError(construir_error_api(
            code=ERROR_CODE_INVALID_BODY,
            message='Cuerpo de la solicitud invalido',
            description='El cuerpo debe ser un JSON valido con Content-Type application/json'
        ))


def _recoger(fn):
    """Ejecuta fn() y devuelve (valor, errores) acumulando los errores en formato API."""
    try:
        return fn(), []
    except ValueError as error:
        return None, list(error.args[0]['errors'])


def validar_body_producto(body: dict) -> dict:
    """Body de POST/PUT /productos: nombre, descripcion, precio, stock, imagen_url, categoria_id."""
    _validar_body_presente(body)

    errores = []

    nombre, e1 = _recoger(lambda: validar_largo_string(
        validar_string_no_vacio(body.get('nombre'), 'nombre'),
        1, PRODUCTO_NOMBRE_MAX_LEN, 'nombre'
    ))
    errores.extend(e1)

    descripcion, e2 = _recoger(lambda: validar_largo_string(
        validar_string_opcional(body.get('descripcion'), 'descripcion'),
        0, PRODUCTO_DESCRIPCION_MAX_LEN, 'descripcion'
    ))
    errores.extend(e2)

    precio, e3 = _recoger(lambda: validar_minimo(
        validar_decimal(body.get('precio'), 'precio'), PRECIO_MIN, 'precio'
    ))
    errores.extend(e3)

    stock, e4 = _recoger(lambda: validar_minimo(
        validar_entero(body.get('stock'), 'stock'), STOCK_MIN, 'stock'
    ))
    errores.extend(e4)

    imagen_url, e5 = _recoger(lambda: validar_largo_string(
        validar_string_opcional(body.get('imagen_url'), 'imagen_url'),
        0, PRODUCTO_IMAGEN_MAX_LEN, 'imagen_url'
    ))
    errores.extend(e5)

    categoria_id, e6 = _recoger(lambda: validar_minimo(
        validar_entero(body.get('categoria_id'), 'categoria_id'), 1, 'categoria_id'
    ))
    errores.extend(e6)

    if errores:
        raise ValueError({'errors': errores})

    return {
        'nombre':       nombre,
        'descripcion':  descripcion,
        'precio':       precio,
        'stock':        stock,
        'imagen_url':   imagen_url,
        'categoria_id': categoria_id,
    }
