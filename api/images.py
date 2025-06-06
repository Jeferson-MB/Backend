import os
import cloudinary
import cloudinary.uploader
from flask import Blueprint, current_app, request, jsonify
import json

images_bp = Blueprint('images', __name__)

def load_db():
    with open(current_app.config['DATABASE_FILE']) as f:
        return json.load(f)

def save_db(data):
    with open(current_app.config['DATABASE_FILE'], 'w') as f:
        json.dump(data, f, indent=2)

cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET')
)

@images_bp.route('/images', methods=["POST"])
def upload_image():
    if request.is_json:
        data = request.get_json()
        image_url = data.get('image_url')
        filename = data.get('filename')
        user_id = data.get('user_id')
        if not all([image_url, filename, user_id]):
            return jsonify({"error": "Faltan datos"}), 400
        db = load_db()
        new_id = (max([img['id'] for img in db['images']] or [0]) + 1)
        new_image = {
            'id': new_id,
            'user_id': int(user_id),
            'filename': filename,
            'image_url': image_url,
            'comments': [],
            'likes': []
        }
        db['images'].append(new_image)
        save_db(db)
        return jsonify({'message': 'Imagen subida', 'id': new_id}), 201

    user_id = request.form.get('user_id')
    file = request.files.get('image')
    if file and user_id:
        try:
            result = cloudinary.uploader.upload(file)
            image_url = result['secure_url']
        except Exception as e:
            return jsonify({'error': 'Error al subir a Cloudinary', 'details': str(e)}), 500

        db = load_db()
        new_id = (max([img['id'] for img in db['images']] or [0]) + 1)
        new_image = {
            'id': new_id,
            'user_id': int(user_id),
            'filename': file.filename,
            'image_url': image_url,
            'comments': [],
            'likes': []
        }
        db['images'].append(new_image)
        save_db(db)
        return jsonify({'message': 'Imagen subida', 'id': new_id}), 201

    return jsonify({'error': 'No se recibió la imagen'}), 400

@images_bp.route('/images', methods=["GET"])
def get_images():
    db = load_db()
    return jsonify(db["images"])