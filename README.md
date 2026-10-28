# Store - API

> **Aviso:** este proyecto es **codigo de ejemplo** con fines didacticos. Puede contener errores, simplificaciones o decisiones de diseno discutibles. Si se usa como base para un trabajo practico u otro entregable, **debe adaptarse a las buenas practicas y consignas especificas de la materia/catedra**.

## Motivacion

Backend (API REST en Flask) de un ejemplo integrador: una **tienda simple** con
`categorias` y `productos`, persistida en **MySQL**. La consumen el frontend
[`store-web`](../store-web) (server-rendered) o cualquier cliente HTTP.

**Sin autenticacion**: todos los endpoints son publicos, a proposito, para
mantener el ejemplo minimo.

## Arquitectura

```
  Frontend (store-web, puerto 5001)
     |
     |  requests.get/post/put/delete (JSON)
     v
  Flask API (este proyecto, puerto 5000, montada en /store_api)
     |
     v
  MySQL 8 (categorias, productos) via docker-compose
```

## Estructura del proyecto

```
store-api/
├── app.py                       # Entry point Flask (puerto 5000)
├── requirements.txt
├── .env.example                 # Variables de entorno de ejemplo
├── docker-compose.yml           # MySQL 8 con init_db.sql montado
├── db/
│   └── init_db.sql              # DDL + datos semilla
└── store_api/
    ├── constants.py             # BASE_URL, reglas de dominio, DB config, error codes
    ├── db.py                    # Engine SQLAlchemy + queries (SQL crudo con text())
    ├── utils.py                 # Errores API y validadores genericos
    ├── routes/
    │   ├── productos.py         # GET/POST/PUT/DELETE /productos
    │   └── categorias.py        # GET/POST/PUT/DELETE /categorias
    ├── services/
    │   ├── productos.py         # DTOs + logica de negocio
    │   └── categorias.py
    └── validators/
        ├── productos.py         # Validacion de bodies
        └── categorias.py
```

Capas: `routes -> services -> validators -> db`. Las rutas no tienen logica de
negocio; los services orquestan; los validators devuelven errores 400
acumulados; `db.py` es el unico lugar con SQL.

## Endpoints

Montados bajo `/store_api`:

| Metodo | Ruta | Descripcion |
|--------|------|-------------|
| GET    | `/productos` | Lista productos (`?categoria_id=`, `?q=` opcionales) |
| GET    | `/productos/<id>` | Detalle de un producto |
| POST   | `/productos` | Crea un producto |
| PUT    | `/productos/<id>` | Actualiza un producto |
| DELETE | `/productos/<id>` | Elimina un producto (204) |
| GET    | `/categorias` | Lista categorias (con `cantidad_productos`) |
| GET    | `/categorias/<id>` | Detalle de una categoria |
| POST   | `/categorias` | Crea una categoria |
| PUT    | `/categorias/<id>` | Actualiza una categoria |
| DELETE | `/categorias/<id>` | Elimina una categoria (409 si tiene productos) |

### Ejemplos

```bash
# Crear categoria
curl -X POST http://localhost:5000/store_api/categorias \
  -H 'Content-Type: application/json' \
  -d '{"nombre": "Libros", "descripcion": "Libros y comics"}'

# Crear producto
curl -X POST http://localhost:5000/store_api/productos \
  -H 'Content-Type: application/json' \
  -d '{"nombre": "Novela", "descripcion": "Tapa dura", "precio": 19999.90, "stock": 5, "imagen_url": "", "categoria_id": 4}'

# Listar productos de una categoria
curl "http://localhost:5000/store_api/productos?categoria_id=4"
```

### Formato de error

Todos los errores devuelven el mismo envelope:

```json
{
  "errors": [
    { "code": "required.nombre", "message": "Campo requerido: 'nombre'",
      "level": "error", "description": "El campo 'nombre' es obligatorio y no puede estar vacio" }
  ]
}
```

## Requisitos previos

- Python 3.10+
- Docker + Docker Compose (recomendado) o un MySQL 8 local

## Configuracion y ejecucion

```bash
# 1) Levantar MySQL (crea la base `store` y corre init_db.sql)
docker compose up -d

# 2) Crear .env a partir del ejemplo (los defaults ya funcionan)
cp .env.example .env

# 3) Crear entorno virtual e instalar dependencias
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # Linux/macOS
pip install -r requirements.txt

# 4) Correr la API en http://localhost:5000
python app.py
```
