# repast/__init__.py
from flask import Flask
from flask_cors import CORS
from .config import get_settings

def create_app():
    app = Flask(__name__)
    settings = get_settings()
    
    # Configure app using settings
    app.config['DEBUG'] = settings.DEBUG
    app.config['ENV'] = settings.FLASK_ENV
    
    # Configure CORS
    CORS(app)
    
    return app