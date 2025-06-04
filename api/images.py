from flask import Blueprint, request, jsonify
from db_sqlite import get_db
import datetime

images_bp = Blueprint('images', __name__)

# Obtener todas las imágenes
@images_bp.route('/api/images', methods=['GET'])
def get_images():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT id, user_id, image_base64 FROM images")
    images = cursor.fetchall()
    image_list = [
        {'id': row[0], 'user_id': row[1], 'image_base64': row[2]}
        for row in images
    ]
    return jsonify(image_list)

# Obtener una imagen específica por ID
@images_bp.route('/api/images/<int:image_id>', methods=['GET'])
def get_image(image_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT id, user_id, image_base64 FROM images WHERE id = ?", (image_id,))
    row = cursor.fetchone()
    if row:
        return jsonify({'id': row[0], 'user_id': row[1], 'image_base64': row[2]})
    else:
        return jsonify({'error': 'Imagen no encontrada'}), 404

# Subir una imagen en base64
@images_bp.route('/api/images', methods=['POST'])
def upload_image():
    data = request.get_json()
    user_id = data.get('user_id')
    image_base64 = data.get('image_base64')

    if not user_id or not image_base64:
        return jsonify({'error': 'Faltan datos requeridos'}), 400

    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO images (user_id, image_base64, created_at) VALUES (?, ?, ?)",
        (user_id, image_base64, datetime.datetime.now())
    )
    db.commit()

    return jsonify({'message': 'Imagen subida exitosamente', 'image_id': cursor.lastrowid}), 201

# Eliminar una imagen
@images_bp.route('/api/images/<int:image_id>', methods=['DELETE'])
def delete_image(image_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM images WHERE id = ?", (image_id,))
    db.commit()
    return jsonify({'message': 'Imagen eliminada'}), 200

