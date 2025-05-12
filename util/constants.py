import os

# Try to load environment variables from .env file if available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # Running in container or dotenv not installed
    pass

# Base paths
BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
PATH_INPUT = os.path.join(BASE_DIR, 'imagens', 'entrada') + "/"
PATH_OUTPUT = os.path.join(BASE_DIR, 'imagens', 'saida') + "/"
PATH_ORIGINALS = os.path.join(BASE_DIR, 'imagens', 'originais') + "/"

# Test configurations
TEST_FILE = "teste.jpg"
PATH_INPUT_TEST = os.path.join(PATH_INPUT, TEST_FILE)

# File configurations
MAX_CONTENT_LENGTH = int(os.getenv('MAX_CONTENT_LENGTH', 5 * 1024 * 1024))  # 5MB default
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Flask configurations
DEBUG = os.getenv('FLASK_ENV', 'production') == 'development'
TESTING = False
SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'fallback-development-key')

# CORS configuration
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
