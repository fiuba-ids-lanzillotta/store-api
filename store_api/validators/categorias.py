from ..constants import (
    CATEGORIA_NOMBRE_MAX_LEN,
    CATEGORIA_DESCRIPCION_MAX_LEN,
    ERROR_CODE_INVALID_BODY,
)
from ..utils import (
    construir_error_api,
    validar_string_no_vacio,
    validar_string_opcional,
    validar_largo_string,
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


def validar_body_categoria(body: dict) -> dict:
    """Body de POST/PUT /categorias: nombre, descripcion."""
    _validar_body_presente(body)

    errores = []

    nombre, e1 = _recoger(lambda: validar_largo_string(
        validar_string_no_vacio(body.get('nombre'), 'nombre'),
        1, CATEGORIA_NOMBRE_MAX_LEN, 'nombre'
    ))
    errores.extend(e1)

    descripcion, e2 = _recoger(lambda: validar_largo_string(
        validar_string_opcional(body.get('descripcion'), 'descripcion'),
        0, CATEGORIA_DESCRIPCION_MAX_LEN, 'descripcion'
    ))
    errores.extend(e2)

    if errores:
        raise ValueError({'errors': errores})

    return {
        'nombre':      nombre,
        'descripcion': descripcion,
    }
