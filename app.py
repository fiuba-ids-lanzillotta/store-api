import logging
from flask import Flask
from flask_cors import CORS

from store_api.constants import BASE_URL
from store_api.routes.productos import productos_bp
from store_api.routes.categorias import categorias_bp

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s - %(name)s - %(message)s')

app = Flask(__name__)
app.json.sort_keys = False

# Habilitar CORS para que el frontend pueda consumir la API
CORS(app)

app.register_blueprint(productos_bp, url_prefix=BASE_URL)
app.register_blueprint(categorias_bp, url_prefix=BASE_URL)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
