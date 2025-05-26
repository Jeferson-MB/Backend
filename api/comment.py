from flask import Blueprint, current_app, request, jsonify
import json

comments_bp = Blueprint('comments', __name__)

def load_db():
    # app.config['DATABASE_FILE']
    with open(current_app.config['DATABASE_FILE']) as f:
        return json.load(f)
    
def save_db(data):
    with open(current_app.config['DATABASE_FILE'], 'w') as f:
        json.dump(data, f, indent=2)

@comments_bp.route('/comment/<int:image_id>', methods=["POST"])
def add_comment(image_id):
    data = request.json # Trae el user_id y el text
    db = load_db()

    for image in db['images']:
        if image['id'] == image_id:
            newComment = {
                "user_id": data["user_id"],
                "text": data["comment"]
            }
            image['comments'].append(newComment)
            save_db(db)
            return jsonify({ 'message': 'Comentario agregado' }), 201
    return jsonify({ 'error': 'Imagen no encontrada' }), 404

