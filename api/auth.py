from flask import Blueprint, current_app, request, jsonify
import json

auth_bp = Blueprint('auth', __name__)

# Carga el archivo JSON de base de datos
def load_db():
    # app.config['DATABASE_FILE']
    with open(current_app.config['DATABASE_FILE']) as f:
        return json.load(f)

def save_db(data):
    with open(current_app.config['DATABASE_FILE'], 'w') as f:
        json.dump(data, f, indent=2)

@auth_bp.route('/login', methods=["POST"])
def login():
    data = request.json # Datos que vienen de postman (cliente)
    db = load_db() # Datos que estan en el servidor (DB)
    for user in db["users"]:
        if user['username'] == data["username"] and user["password"] == data["password"]:
            return jsonify({ 'mensaje': 'Login exitoso', 'user_id': user["id"] }), 200
        
    return jsonify({ 'error': 'Credenciales inválidas' }), 401

@auth_bp.route('/register', methods=["POST"])
def register():
    data = request.json
    db = load_db()
    # Si existe un username en base de datos que sea igual al que viene en el request 
    if any(u["username"] == data["username"] for u in db["users"]):
        return jsonify({ 'error': 'Usuario ya existe' }), 400
    
    newUser = {
        'id': len(db['users']) + 1, # 3
        'username': data['username'],
        'password': data['password']
    }
    db["users"].append(newUser)
    save_db(db)
    return jsonify({ 'message:' 'Registrado correctamente' }), 201

@auth_bp.route('/users', methods=["GET"])
def get_users():
    db = load_db()
    return jsonify(db["users"]), 200