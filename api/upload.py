from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from db_sqlite import get_db
import datetime
import base64
import os

upload_bp = Blueprint('upload', __name__)

# Configuración de archivos permitidos
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@upload_bp.route('/api/upload', methods=['POST'])
def upload_file():
    if 'image' not in request.files:
        return jsonify({'error': 'No se encontró archivo'}), 400
    
    file = request.files['image']
    
    if file.filename == '':
        return jsonify({'error': 'No se seleccionó archivo'}), 400
    
    if file and allowed_file(file.filename):
        try:
            # Leer archivo y convertir a base64
            file_data = file.read()
            base64_data = base64.b64encode(file_data).decode('utf-8')
            mime_type = file.content_type
            
            # Crear data URL completa
            data_url = f"data:{mime_type};base64,{base64_data}"
            
            # Guardar en base de datos
            db = get_db()
            cursor = db.cursor()
            cursor.execute(
                "INSERT INTO images (user_id, image_base64, created_at) VALUES (?, ?, ?)",
                (1, data_url, datetime.datetime.now())  # user_id = 1 por defecto
            )
            db.commit()
            
            return jsonify({
                'message': 'Imagen subida exitosamente',
                'image_id': cursor.lastrowid
            }), 201
            
        except Exception as e:
            return jsonify({'error': f'Error procesando archivo: {str(e)}'}), 500
    
    return jsonify({'error': 'Tipo de archivo no permitido'}), 400