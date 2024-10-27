from flask import Flask
from os import environ
from dotenv import load_dotenv
from .models import db
import openai

load_dotenv()

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.secret_key = environ.get("SECRET_KEY", "dev-secret-key")
    app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL', 'sqlite:///covenants.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
    app.config['UPLOAD_FOLDER'] = 'uploads'
    
    # Initialize OpenAI
    openai.api_key = environ.get('OPENAI_API_KEY')  # Get from environment variables
    if not openai.api_key:
        raise ValueError("OpenAI API key not found in environment variables")
    
    # Initialize extensions
    db.init_app(app)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    # Register blueprints
    from app.auth.routes import auth_bp
    from app.main.routes import main_bp
    from app.documents.routes import documents_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(documents_bp)
    
    return app
