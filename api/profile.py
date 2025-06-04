from flask import Blueprint, jsonify
from db_sqlite import get_db

profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/api/profile/<int:user_id>', methods=['GET'])
def get_profile(user_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT username, photo_base64 FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    if user:
        return jsonify({
            'username': user[0],
            'photo': user[1]
        })
    else:
        return jsonify({'error': 'Usuario no encontrado'}), 404
