from flask import Blueprint, request, jsonify
import json
import bcrypt
from db_sqlite import query_db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=["POST"])
def login():
    data = request.json # Datos que vienen de postman (cliente)
    #db = load_db() # Datos que estan en el servidor (DB)
    user = query_db(
        'SELECT * FROM users WHERE username = ? AND password = ?',
        (data['username'], ), one=True
    )

    if user:
        stored_hash = user['password']

        # Contraseñas: 1 manda el cliente, 2: En base de datos
        password_bytes = data['password'].encode['utf-8']
        stored_hash_bytes = stored_hash.encode('utf-8')

        if bcrypt.checkpw(password_bytes, stored_hash_bytes):
            return jsonify({'mensaje': 'Login exitoso', 'user_id': user['id']}), 200
        
    return jsonify({ 'error': 'Credenciales inválidas' }), 401

@auth_bp.route('/register', methods=["POST"])
def register():
    data = request.json
    
    # Verifica si el usuario ya existe
    existing_user = query_db(
        'SELECT * FROM users WHERE username = ?',
        (data['username'],), one=True
    )

    if existing_user:
        return jsonify({'error': 'Usuario ya existe'}), 400
    
    # Hashear la contraseña antes de guardarla
    password_bytes = data['password'].encode('utf-8')
    hashed_password = bcrypt.hashpw(password_bytes, bcrypt.gensalt())

    # Insertar nuevo usuario en la base de datos
    query_db(
        'INSERT INTO users (username, password) VALUES (?, ?)',
        (data['username'], hashed_password.decode('utf-8')), commit=True
    )

    # Obtener el ID del nuevo usuario
    new_user = query_db(
        'SELECT id FROM users WHERE username = ?',
        (data['username'],), one=True
    )

    return jsonify({
        'message': 'Registrado correctamente',
        'user_id': new_user['id']
    }), 201
    '''db = load_db()
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
    return jsonify({ 'message:' 'Registrado correctamente' }), 201'''

@auth_bp.route('/users', methods=["GET"])
def get_users():
    users = query_db('SELECT id, username FROM users')
    return jsonify([dict(user) for user in users]), 200