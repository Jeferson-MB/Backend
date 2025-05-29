from flask import Flask
from flask_cors import CORS
import os
from api import create_api
from config import Config
from utils.setup import init_database, init_directories

app = Flask(__name__)
CORS(app) 


app.config.from_object(Config)
init_directories()
init_database()
# -----------------------------------------------

create_api(app)

# Ruta de prueba
@app.route('/')
def hello_world():
    return 'Hello World!'

if __name__ == '__main__':
    # app.run(debug=True)

    # Modo Producción
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)