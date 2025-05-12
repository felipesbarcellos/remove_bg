from flask import Flask, jsonify, request, send_file
from flasgger import Swagger
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_cors import CORS
from util.ImageHandler import ImageHandler
import os
from util import setup_directories
from util.constants import PATH_INPUT, PATH_OUTPUT
from config import Config

app = Flask(__name__)
CORS(app, 
     resources={r"/api/*": {
         "origins": Config.CORS_ORIGINS,  # Lista de origens permitidas
         "methods": Config.CORS_METHODS,
         "allow_headers": Config.CORS_ALLOW_HEADERS,
         "expose_headers": Config.CORS_EXPOSE_HEADERS,
         "supports_credentials": Config.CORS_SUPPORTS_CREDENTIALS
     }})

# Configuração do Swagger
swagger_config = {
    "headers": [],
    "specs": [{
        "endpoint": 'apispec',
        "route": '/apispec.json',
        "rule_filter": lambda rule: True,
        "model_filter": lambda tag: True,
    }],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidocs/"
}

swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "Remove BG API",
        "description": "API para remoção de fundo de imagens",
        "version": "1.0.0"
    },    "basePath": "/api",
    "schemes": ["https", "http"],
    "consumes": ["multipart/form-data", "application/json"],
    "produces": ["application/json", "image/png"]
}

Swagger(app, config=swagger_config, template=swagger_template)

# Configure rate limiting
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["100 per day", "10 per minute"]
)

# Configure Swagger template
app.config['SWAGGER'] = {
    'title': 'Remove BG API',
    'uiversion': 3,
    'openapi': '3.0.2',
    'specs_route': '/apidocs/'
}

# Configuração para upload de arquivos
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/api/upload', methods=['POST'])
def upload_file():
    """
    Upload de imagem
    ---
    tags:
      - imagens
    consumes:
      - multipart/form-data
    parameters:
      - name: file
        in: formData
        type: file
        required: true
        description: Arquivo de imagem
    responses:
      200:
        description: Sucesso
        schema:
          type: object
          properties:
            filePath:
              type: string
              description: Caminho do arquivo
      400:
        description: Erro na requisição
        schema:
          type: object
          properties:
            error:
              type: string
              description: Mensagem de erro
    """
    if 'file' not in request.files:
      return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']

    if file.filename == '':
      return jsonify({"error": "No file selected for uploading"}), 400

    file_path = os.path.join(PATH_INPUT, file.filename)
    file.save(file_path)

    return jsonify({"filePath": file_path}), 200


# Initialize directories during application startup
setup_directories()

# Endpoint para remover o fundo da imagem

def get_download_url(filename):
    # Pega o host da requisição para gerar URL absoluta
    host = request.headers.get('Host', request.host)
    if 'ngrok' in host:
        scheme = 'https'
    else:
        scheme = request.scheme
    return f"{scheme}://{host}/api/download?file={filename}"

@app.route('/api/remove-background', methods=['POST'])
def remove_background():
    """
    Remove o fundo da imagem
    ---
    tags:
      - imagens
    parameters:
      - name: file
        in: query
        type: string
        required: true
        description: Nome do arquivo
    responses:
      200:
        description: Fundo removido com sucesso
        schema:
          type: object
          properties:
            message:
              type: string
              description: Mensagem de sucesso
            download_url:
              type: string
              description: URL para download da imagem processada
      400:
        description: Erro ao processar a imagem
        schema:
          type: object
          properties:
            error:
              type: string
              description: Mensagem de erro
    """
    try:
        file_name = request.args.get("file")
        print(f"Received file path: {file_name}")

        if not file_name:
            return jsonify({"error": "File path is required"}), 400

        if not os.path.isabs(file_name):
            file_name = os.path.abspath(f"{PATH_INPUT}{file_name}")

        if not os.path.exists(file_name):
            return jsonify({"error": f"File not found: {file_name}"}), 404

        handler = ImageHandler(os.path.join(PATH_INPUT, file_name))
        handler.remove_background()
        handler.save()
        
        input_name = os.path.splitext(os.path.basename(file_name))[0]
        download_filename = f"{input_name}.png"
        print(f"Arquivo processado: {handler.output_path}")
        print(f"Nome do arquivo para download: {download_filename}")
        
        download_url = get_download_url(download_filename)
        return jsonify({"message": "Background removed successfully", "download_url": download_url}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint para adicionar um fundo à imagem

@app.route('/api/add-background', methods=['POST'])
def add_background():
    """
    Adiciona fundo colorido
    ---
    tags:
      - imagens
    parameters:
      - name: file
        in: query
        type: string
        required: true
        description: Nome do arquivo
      - name: color
        in: query
        type: string
        required: false
        default: "#000000"
        description: Cor em hexadecimal
    responses:
      200:
        description: Fundo adicionado com sucesso
        schema:
          type: object
          properties:
            message:
              type: string
              description: Mensagem de sucesso
            download_url:
              type: string
              description: URL para download da imagem processada
      400:
        description: Erro ao processar a imagem
        schema:
          type: object
          properties:
            error:
              type: string
              description: Mensagem de erro
    """
    try:
        file_name = request.args.get("file")
        color = request.args.get("color", "#000")

        if not file_name:
            return jsonify({"error": "File name is required"}), 400

        file_path = os.path.join(PATH_INPUT, file_name)

        if not os.path.exists(file_path):
            return jsonify({"error": f"File not found: {file_name}"}), 404

        handler = ImageHandler(file_path)
        handler.add_background(color)
        handler.save()

        input_name = os.path.splitext(file_name)[0]
        download_filename = f"{input_name}.png"
        print(f"Arquivo processado: {handler.output_path}")
        print(f"Nome do arquivo para download: {download_filename}")
        
        download_url = get_download_url(download_filename)
        return jsonify({"message": "Background added successfully", "download_url": download_url}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint para download da imagem processada

@app.route('/api/download', methods=['GET', 'OPTIONS'])
def download_image():
    """
    Download da imagem
    ---
    tags:
      - imagens
    parameters:
      - name: file
        in: query
        type: string
        required: true
        description: Nome do arquivo
    responses:
      200:
        description: Sucesso
        schema:
          type: file
      404:
        description: Arquivo não encontrado
        schema:
          type: object
          properties:
            error:
              type: string
              description: Mensagem de erro
    """
    if request.method == 'OPTIONS':
        response = app.make_default_options_response()
        response.headers['Access-Control-Allow-Origin'] = request.headers.get('Origin')
        response.headers['Access-Control-Allow-Methods'] = 'GET, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = '*'
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        response.headers['Access-Control-Expose-Headers'] = 'Content-Disposition, Content-Length, Content-Type'
        response.headers['Vary'] = 'Origin'
        return response

    try:
        file_name = request.args.get("file")
        if not file_name:
            return jsonify({"error": "File parameter is required"}), 400

        output_path = os.path.join(PATH_OUTPUT, file_name)
        print(f"Tentando download do arquivo: {output_path}")

        if not os.path.exists(output_path):
            return jsonify({"error": f"File not found: {file_name}"}), 404

        response = send_file(
            output_path,
            as_attachment=True,
            download_name=file_name,
            mimetype='image/png'
        )
        
        origin = request.headers.get('Origin')
        if origin in Config.CORS_ORIGINS:
            response.headers['Access-Control-Allow-Origin'] = origin
            response.headers['Access-Control-Allow-Credentials'] = 'true'
            response.headers['Access-Control-Allow-Headers'] = ', '.join(Config.CORS_ALLOW_HEADERS)
            response.headers['Access-Control-Expose-Headers'] = 'Content-Disposition, Content-Length, Content-Type'
            response.headers['Vary'] = 'Origin'
        return response
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
