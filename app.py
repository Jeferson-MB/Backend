import os
from flask import Flask, jsonify
from flask_cors import CORS

# Módulos internos
from api import create_api
from config import Config
from utils.setup import init_database, init_directories
from db_sqlite import close_connection, init_db

app = Flask(__name__)
CORS(app)

# Configuración desde Config
app.config.from_object(Config)

# Inicialización de directorios y base de datos
init_directories()
init_database()

# Inicializar la base de datos dentro del contexto de la aplicación
with app.app_context():
    from db_sqlite import get_db
    # Esto forzará la creación de la conexión si es necesario
    get_db()

# Registro de Blueprints - SOLO usar create_api
create_api(app)

# Ruta de prueba
@app.route('/')
def hello_world():
    return 'Hello World!'

# Mostrar rutas disponibles (debug)
@app.route('/debug/routes')
def show_routes():
    routes = []
    for rule in app.url_map.iter_rules():
        routes.append({
            'endpoint': rule.endpoint,
            'methods': list(rule.methods),
            'rule': str(rule)
        })
    return jsonify(routes)

# Cierre de conexión de BD cuando termina la app
@app.teardown_appcontext
def teardown_db(exception):
    close_connection(exception)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)