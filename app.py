import logging
from flask import Flask, jsonify
from flask_cors import CORS

from store_api.constants import BASE_URL, ERROR_CODE_INTERNAL
from store_api.utils import construir_error_api
from store_api.routes.productos import productos_bp
from store_api.routes.categorias import categorias_bp

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s - %(name)s - %(message)s')

app = Flask(__name__)
app.json.sort_keys = False

# Habilitar CORS para que el frontend pueda consumir la API
CORS(app)


@app.errorhandler(500)
def internal_error(error):
    """Error inesperado (excepciones no capturadas, ej. caida de la base)."""
    return jsonify(construir_error_api(
        code=ERROR_CODE_INTERNAL,
        message='Error interno del servidor',
        description='Ocurrio un error inesperado. Intenta mas tarde.'
    )), 500


app.register_blueprint(productos_bp, url_prefix=BASE_URL)
app.register_blueprint(categorias_bp, url_prefix=BASE_URL)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
