from .auth import auth_bp
from .images import images_bp
from .comment import comments_bp
from .upload import upload_bp

def create_api(app):
    # Registrar todos los blueprints con prefijo /api
    app.register_blueprint(auth_bp, url_prefix='/api')
    app.register_blueprint(images_bp, url_prefix='/api')
    app.register_blueprint(comments_bp, url_prefix='/api')
    app.register_blueprint(upload_bp, url_prefix='/api')