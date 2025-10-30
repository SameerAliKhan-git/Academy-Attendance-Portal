from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import config
import os

db = SQLAlchemy()
login_manager = LoginManager()

def create_app(config_name='development'):
    """Application factory pattern."""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Ensure upload folder exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
    
    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.main import main_bp
    from app.routes.student import student_bp
    from app.routes.parent import parent_bp
    from app.routes.teacher import teacher_bp
    from app.routes.admin import admin_bp
    from app.routes.announcements import announcements_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(student_bp, url_prefix='/student')
    app.register_blueprint(parent_bp, url_prefix='/parent')
    app.register_blueprint(teacher_bp, url_prefix='/teacher')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(announcements_bp, url_prefix='/announcements')
    
    return app
