from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import base64
import jwt
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)

SECRET_KEY = 'clave_secreta_segura'
UPLOAD_FOLDER = 'images'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Mock users (puedes conectar a base de datos real si lo deseas)
USERS = {
    "user@example.com": {
        "password": "1234",
        "name": "Usuario de Prueba",
        "image": "user.png"  # Asegúrate de tener esta imagen en /images
    }
}

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = USERS.get(email)
    if user and user["password"] == password:
        token = jwt.encode({
            'email': email,
            'exp': datetime.utcnow() + timedelta(hours=1)
        }, SECRET_KEY, algorithm='HS256')
        return jsonify({'token': token})
    return jsonify({'error': 'Credenciales inválidas'}), 401

@app.route('/api/user', methods=['GET'])
def get_user():
    auth = request.headers.get('Authorization')
    if not auth:
        return jsonify({'error': 'No autorizado'}), 401

    try:
        token = auth.split()[1]
        decoded = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        email = decoded['email']
        user = USERS.get(email)

        if not user:
            return jsonify({'error': 'Usuario no encontrado'}), 404

        image_path = os.path.join(UPLOAD_FOLDER, user["image"])
        if os.path.exists(image_path):
            with open(image_path, 'rb') as img_file:
                image_base64 = base64.b64encode(img_file.read()).decode('utf-8')
        else:
            image_base64 = None

        return jsonify({
            'name': user["name"],
            'email': email,
            'image_base64': image_base64
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 401

@app.route('/api/upload', methods=['POST'])
def upload_image():
    data = request.get_json()
    filename = data.get('filename')
    image_data = data.get('image')

    if not filename or not image_data:
        return jsonify({'error': 'Faltan datos'}), 400

    image_data = image_data.split(',')[1] if ',' in image_data else image_data
    filepath = os.path.join(UPLOAD_FOLDER, filename)

    with open(filepath, 'wb') as f:
        f.write(base64.b64decode(image_data))

    return jsonify({'message': 'Imagen guardada correctamente', 'filename': filename})

@app.route('/images/<path:filename>')
def serve_image(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True)
