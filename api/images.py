from flask import Blueprint, current_app, request, jsonify
import json, base64

images_bp = Blueprint('images', __name__)

def load_db():
    with open(current_app.config['DATABASE_FILE']) as f:
        return json.load(f)
    
def save_db(data):
    with open(current_app.config['DATABASE_FILE'], 'w') as f:
        json.dump(data, f, indent=2)

@images_bp.route('/images', methods=["GET"])
def get_images():
    db = load_db()
    return jsonify(db["images"])

@images_bp.route('/upload', methods=["POST"])
def upload():
    user_id = request.form['user_id']
    file = request.files['image']
    if file:
        file_data = file.read() # Leyendo como binario
        encoded_data = base64.b64encode(file_data).decode('utf-8')

        db = load_db()
        new_image = {
            'id': len(db['images']) + 1,
            'user_id': int(user_id),
            'filename': file.filename,
            'filedata': encoded_data,
            'comments': []
        }
        db['images'].append(new_image)
        save_db(db)
        return jsonify({ 'message': 'Imagen subida' }), 201
    
    return jsonify({ 'error': 'No se recibió la imagen' }), 400
