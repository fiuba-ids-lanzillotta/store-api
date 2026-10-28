from .constants import (
    ERROR_CODE_INVALID_MIN_VALUE,
    ERROR_CODE_INVALID_MAX_VALUE,
    ERROR_CODE_INVALID_PRECIO,
)


# ---------------------------------------------------------------
# Errores
# ---------------------------------------------------------------

def construir_error_api(code: str, message: str, description: str, level: str = 'error') -> dict:
    """Construye un payload de error compatible con el resto de la API."""
    return {
        'errors': [{
            'code': code,
            'message': message,
            'level': level,
            'description': description
        }]
    }


# ---------------------------------------------------------------
# Validaciones genericas
# ---------------------------------------------------------------

def validar_entero(numero, nombre: str = 'numero') -> int:
    try:
        return int(str(numero))
    except (ValueError, TypeError):
        raise ValueError(construir_error_api(
            code=f'invalid.{nombre}.format',
            message=f"Formato de '{nombre}' invalido",
            description=f"El valor '{numero}' no puede convertirse a un numero entero"
        ))


def validar_decimal(numero, nombre: str = 'precio') -> float:
    """Convierte a float; acepta '12.50' o 12.5 pero no 'abc' ni negativos raros."""
    try:
        valor = float(str(numero).replace(',', '.'))
    except (ValueError, TypeError, AttributeError):
        raise ValueError(construir_error_api(
            code=ERROR_CODE_INVALID_PRECIO,
            message=f"Formato de '{nombre}' invalido",
            description=f"El valor '{numero}' no es un numero valido"
        ))

    if valor != valor or valor in (float('inf'), float('-inf')):
        raise ValueError(construir_error_api(
            code=ERROR_CODE_INVALID_PRECIO,
            message=f"Formato de '{nombre}' invalido",
            description=f"El valor '{numero}' no es un numero valido"
        ))

    return round(valor, 2)


def validar_minimo(valor: float, minimo: float, nombre: str):
    if valor < minimo:
        raise ValueError(construir_error_api(
            code=ERROR_CODE_INVALID_MIN_VALUE,
            message='Valor por debajo del minimo permitido',
            description=f"El parametro '{nombre}' debe ser mayor o igual a {minimo}. Se recibio: {valor}"
        ))

    return valor


def validar_string_no_vacio(valor, nombre: str) -> str:
    if valor is None or not str(valor).strip():
        raise ValueError(construir_error_api(
            code=f'required.{nombre}',
            message=f"Campo requerido: '{nombre}'",
            description=f"El campo '{nombre}' es obligatorio y no puede estar vacio"
        ))

    return str(valor).strip()


def validar_string_opcional(valor, nombre: str) -> str:
    """String opcional: None/vacio devuelve '' (se persiste como cadena vacia)."""
    if valor is None:
        return ''

    return str(valor).strip()


def validar_largo_string(valor: str, minimo: int, maximo: int, nombre: str) -> str:
    if len(valor) < minimo:
        raise ValueError(construir_error_api(
            code=ERROR_CODE_INVALID_MIN_VALUE,
            message=f"Longitud minima no alcanzada en '{nombre}'",
            description=f"El campo '{nombre}' debe tener al menos {minimo} caracteres"
        ))

    if len(valor) > maximo:
        raise ValueError(construir_error_api(
            code=ERROR_CODE_INVALID_MAX_VALUE,
            message=f"Longitud maxima superada en '{nombre}'",
            description=f"El campo '{nombre}' debe tener como maximo {maximo} caracteres"
        ))

    return valor
