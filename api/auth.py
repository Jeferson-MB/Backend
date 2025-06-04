from flask import Blueprint, request, jsonify
from db_sqlite import get_user_by_username

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/api/login', methods=['POST', 'OPTIONS'])
def login():
    if request.method == 'OPTIONS':
        return '', 200
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user = get_user_by_username(username)
    if user and user['password'] == password:
        return jsonify({'username': username, 'name': user['name']}), 200
    return jsonify({'error': 'Credenciales inválidas'}), 401