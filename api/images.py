from flask import Blueprint, current_app, request, jsonify
import json, base64, os

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
    images = []

    for image in db.get('images', []):
        image_path = os.path.join(current_app.root_path, 'static', 'uploads', image['filename'])
        if os.path.exists(image_path):
            with open(image_path, 'rb') as img_file:
                encoded_string = base64.b64encode(img_file.read()).decode('utf-8')
            images.append({
                'id': image['id'],
                'user_id': image['user_id'],
                'filename': image['filename'],
                'image_data': encoded_string,
                'mime_type': 'image/jpeg',  # Puedes hacer esto dinámico si gustas
                'comments': image.get('comments', [])
            })

    return jsonify(images)

@images_bp.route('/upload', methods=["POST"])
def upload():
    user_id = request.form.get('user_id')
    file = request.files.get('image')

    if file and user_id:
        # Guardar archivo físicamente
        upload_path = os.path.join(current_app.root_path, 'static', 'uploads')
        os.makedirs(upload_path, exist_ok=True)
        filepath = os.path.join(upload_path, file.filename)
        file.save(filepath)

        # Codificar a base64 para la base de datos (opcional si ya lo tienes guardado en disco)
        file.seek(0)  # Reiniciar puntero para volver a leer
        encoded_data = base64.b64encode(file.read()).decode('utf-8')

        db = load_db()
        new_image = {
            'id': len(db['images']) + 1,
            'user_id': int(user_id),
            'filename': file.filename,
            'filedata': encoded_data,  # Podrías omitir esto si no deseas guardar el base64
            'comments': []
        }
        db['images'].append(new_image)
        save_db(db)

        return jsonify({ 'message': 'Imagen subida con éxito' }), 201

    return jsonify({ 'error': 'Faltan datos: imagen o user_id' }), 400

