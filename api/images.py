from flask import Blueprint, request, jsonify
from db_sqlite import get_db
import datetime

images_bp = Blueprint('images', __name__)

# Debug route to test if blueprint is working
@images_bp.route('/images/test', methods=['GET'])
def test_images():
    return jsonify({'message': 'Images blueprint is working!', 'status': 'ok'}), 200

# Obtener todas las imágenes
@images_bp.route('/images', methods=['GET'])  # ✅ Corrected - removed /api prefix
def get_images():
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT id, user_id, image_base64 FROM images")
        images = cursor.fetchall()
        image_list = [
            {'id': row[0], 'user_id': row[1], 'image_base64': row[2]}
            for row in images
        ]
        return jsonify(image_list)
    except Exception as e:
        print(f"Error in get_images: {e}")
        return jsonify({'error': 'Error al obtener imágenes'}), 500

# Obtener una imagen específica por ID
@images_bp.route('/images/<int:image_id>', methods=['GET'])  # ✅ Corrected
def get_image(image_id):
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT id, user_id, image_base64 FROM images WHERE id = ?", (image_id,))
        row = cursor.fetchone()
        if row:
            return jsonify({'id': row[0], 'user_id': row[1], 'image_base64': row[2]})
        else:
            return jsonify({'error': 'Imagen no encontrada'}), 404
    except Exception as e:
        print(f"Error in get_image: {e}")
        return jsonify({'error': 'Error al obtener imagen'}), 500

# Subir una imagen en base64
@images_bp.route('/images', methods=['POST'])  # ✅ Corrected
def upload_image():
    try:
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
    except Exception as e:
        print(f"Error in upload_image: {e}")
        return jsonify({'error': 'Error al subir imagen'}), 500

# Eliminar una imagen
@images_bp.route('/images/<int:image_id>', methods=['DELETE'])  # ✅ Corrected
def delete_image(image_id):
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("DELETE FROM images WHERE id = ?", (image_id,))
        db.commit()
        
        # Verify if the image was actually deleted
        if cursor.rowcount == 0:
            return jsonify({'error': 'Imagen no encontrada'}), 404
        
        return jsonify({'message': 'Imagen eliminada exitosamente'}), 200
    except Exception as e:
        print(f"Error in delete_image: {e}")
        return jsonify({'error': 'Error al eliminar imagen'}), 500