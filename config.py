import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    # File paths
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'imagens', 'entrada')
    OUTPUT_FOLDER = os.path.join(BASE_DIR, 'imagens', 'saida')
    ORIGINALS_FOLDER = os.path.join(BASE_DIR, 'imagens', 'originais')
    
    # File configuration
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5MB max file size
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}    # Flask configuration
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.getenv('SECRET_KEY')    # CORS configuration
    CORS_ORIGINS = [
        "http://localhost:3000",
        "http://localhost:5000",
        "http://127.0.0.1:4040",
        "http://127.0.0.1:5000",
        "http://127.0.0.1:8000",
        "https://humorous-pretty-glider.ngrok-free.app"
    ]
    CORS_METHODS = ["GET", "POST", "OPTIONS", "PUT", "DELETE"]
    CORS_ALLOW_HEADERS = [
        "Content-Type",
        "Authorization",
        "Accept",
        "Origin",
        "X-Requested-With",
        "Access-Control-Allow-Origin",
        "Access-Control-Allow-Headers"
    ]
    CORS_EXPOSE_HEADERS = ["Content-Disposition", "Content-Length", "Content-Type"]
    CORS_SUPPORTS_CREDENTIALS = True
    CORS_MAX_AGE = 86400
