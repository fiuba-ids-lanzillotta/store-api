import os
from dotenv import load_dotenv

load_dotenv()

# URL base de la API
BASE_URL = '/store_api'

# Reglas de dominio para productos
PRODUCTO_NOMBRE_MAX_LEN = 100
PRODUCTO_DESCRIPCION_MAX_LEN = 500
PRODUCTO_IMAGEN_MAX_LEN = 1500000   # ~1MB de data URI base64
PRECIO_MIN = 0
STOCK_MIN = 0

# Reglas de dominio para categorias
CATEGORIA_NOMBRE_MAX_LEN = 50
CATEGORIA_DESCRIPCION_MAX_LEN = 200

# Configuracion de la base de datos MySQL (levantada via docker-compose)
DB_HOST     = os.getenv('DB_HOST', 'localhost')
DB_PORT     = int(os.getenv('DB_PORT', '3306'))
DB_USER     = os.getenv('DB_USER', 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'root')
DB_NAME     = os.getenv('DB_NAME', 'store')
DB_URL      = f'mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

# Codigos de error
ERROR_CODE_INTERNAL              = 'internal.error'
ERROR_CODE_INVALID_BODY          = 'invalid.body'
ERROR_CODE_INVALID_MIN_VALUE     = 'invalid.min.value'
ERROR_CODE_INVALID_MAX_VALUE     = 'invalid.max.value'
ERROR_CODE_INVALID_PRECIO        = 'invalid.precio.format'
ERROR_CODE_PRODUCTO_NOT_FOUND    = 'producto.not.found'
ERROR_CODE_CATEGORIA_NOT_FOUND   = 'categoria.not.found'
ERROR_CODE_CATEGORIA_CON_PRODUCTOS = 'categoria.con.productos'
ERROR_CODE_NOMBRE_YA_REGISTRADO  = 'nombre.already.registered'
