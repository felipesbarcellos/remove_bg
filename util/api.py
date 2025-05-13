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
import logging

app = Flask(__name__)
CORS(
    app,
    resources={
        r"/api/*": {
            "origins": Config.CORS_ORIGINS,
            "methods": Config.CORS_METHODS,
            "allow_headers": Config.CORS_ALLOW_HEADERS,
            "expose_headers": Config.CORS_EXPOSE_HEADERS,
            "supports_credentials": Config.CORS_SUPPORTS_CREDENTIALS,
        }
    },
)

# Configuração do Swagger
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": "apispec",
            "route": "/apispec.json",
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidocs/",
}

swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "Remove BG API",
        "description": "API para remoção de fundo de imagens",
        "version": "1.0.0",
    },
    "basePath": "/api",
    "schemes": ["https", "http"],
    "consumes": ["multipart/form-data", "application/json"],
    "produces": ["application/json", "image/png"],
}

Swagger(app, config=swagger_config, template=swagger_template)

# Configure rate limiting with in-memory storage
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["100 per day", "10 per minute"],
)

# Configure Swagger template
app.config["SWAGGER"] = {
    "title": "Remove BG API",
    "uiversion": 3,
    "openapi": "3.0.2",
    "specs_route": "/apidocs/",
}

# Configuração para upload de arquivos
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}


def allowed_file(filename):
    """Verifica se o arquivo tem uma extensão permitida."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# Improved error handling for the upload_file endpoint
@app.route("/api/upload", methods=["POST"])
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
        description: Arquivo de imagem (png, jpg, jpeg)
    responses:
      200:
        description: Sucesso
        schema:
          type: object
          properties:
            fileName:
              type: string
              description: Nome do arquivo salvo
        examples:
          application/json: { "fileName": "teste.jpg" }
      400:
        description: Erro na requisição
        schema:
          type: object
          properties:
            error:
              type: string
        examples:
          application/json: { "error": "No file selected for uploading" }
      500:
        description: Erro inesperado
        schema:
          type: object
          properties:
            error:
              type: string
        examples:
          application/json: { "error": "An unexpected error occurred" }
    """
    try:
        if "file" not in request.files:
            return jsonify({"error": "No file part in the request"}), 400

        file = request.files["file"]

        if file.filename == "":
            return jsonify({"error": "No file selected for uploading"}), 400

        if not allowed_file(file.filename):
            return (
                jsonify({"error": "Invalid file extension. Allowed: png, jpg, jpeg"}),
                400,
            )

        file_path = os.path.join(PATH_INPUT, file.filename)
        file.save(file_path)

        return jsonify({"fileName": file.filename}), 200
    except IOError as e:
        logging.exception("I/O error during file upload")
        return jsonify({"error": "Failed to save the file. Please try again."}), 500
    except Exception as e:
        logging.exception("Unexpected error in upload_file")
        return jsonify({"error": "An unexpected error occurred"}), 500


# Improved error handling for setup_directories
try:
    setup_directories()
except Exception as e:
    logging.exception("Failed to initialize directories")
    raise RuntimeError("Failed to initialize required directories") from e

# Endpoint para remover o fundo da imagem


def get_download_url(filename):
    # Pega o host da requisição para gerar URL absoluta
    host = request.headers.get("Host", request.host)
    if "ngrok" in host:
        scheme = "https"
    else:
        scheme = request.scheme
    return f"{scheme}://{host}/api/download?file={filename}"


# Improved error handling with specific exceptions and meaningful messages
@app.route("/api/remove-background", methods=["POST"])
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
        description: Nome do arquivo (ex teste.jpg)
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
        examples:
          application/json: { "message": "Background removed successfully", "download_url": "http://localhost:8000/api/download?file=teste.png" }
      400:
        description: Erro ao processar a imagem
        schema:
          type: object
          properties:
            error:
              type: string
        examples:
          application/json: { "error": "File path is required" }
    """
    try:
        file_name = request.args.get("file")
        if not file_name:
            return jsonify({"error": "File path is required"}), 400

        file_path = os.path.join(PATH_INPUT, file_name)
        if not os.path.exists(file_path):
            return jsonify({"error": f"File not found: {file_name}"}), 404

        handler = ImageHandler(file_path)
        handler.remove_background()
        handler.save()
        input_name = os.path.splitext(os.path.basename(file_name))[0]
        download_filename = f"{input_name}.png"
        download_url = get_download_url(download_filename)
        return (
            jsonify(
                {
                    "message": "Background removed successfully",
                    "download_url": download_url,
                }
            ),
            200,
        )
    except FileNotFoundError as e:
        logging.exception("File not found error")
        return jsonify({"error": str(e)}), 404
    except ValueError as e:
        logging.exception("Value error")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logging.exception("Unexpected error in remove_background")
        return jsonify({"error": "An unexpected error occurred"}), 500


# Similar improvements for add_background
@app.route("/api/add-background", methods=["POST"])
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
        description: Nome do arquivo (ex teste.jpg)
      - name: color
        in: query
        type: string
        required: false
        default: "#000000"
        description: Cor em hexadecimal (ex #FFFFFF)
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
        examples:
          application/json: { "message": "Background added successfully", "download_url": "http://localhost:8000/api/download?file=teste.png" }
      400:
        description: Erro ao processar a imagem
        schema:
          type: object
          properties:
            error:
              type: string
        examples:
          application/json: { "error": "File name is required" }
    """
    try:
        file_name = request.args.get("file")
        color = request.args.get("color", "#000000")
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
        download_url = get_download_url(download_filename)
        return (
            jsonify(
                {
                    "message": "Background added successfully",
                    "download_url": download_url,
                }
            ),
            200,
        )
    except FileNotFoundError as e:
        logging.exception("File not found error")
        return jsonify({"error": str(e)}), 404
    except ValueError as e:
        logging.exception("Value error")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logging.exception("Unexpected error in add_background")
        return jsonify({"error": "An unexpected error occurred"}), 500


@app.route("/api/download", methods=["GET", "OPTIONS"])
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
        description: Nome do arquivo (ex teste.png)
    responses:
      200:
        description: Sucesso
        schema:
          type: file
        examples:
          application/octet-stream: (arquivo binário)
      400:
        description: Parâmetro ausente ou inválido
        schema:
          type: object
          properties:
            error:
              type: string
        examples:
          application/json: { "error": "File parameter is required" }
      404:
        description: Arquivo não encontrado
        schema:
          type: object
          properties:
            error:
              type: string
        examples:
          application/json: { "error": "File not found: teste.png" }
      500:
        description: Erro inesperado
        schema:
          type: object
          properties:
            error:
              type: string
        examples:
          application/json: { "error": "An unexpected error occurred" }
    """
    if request.method == "OPTIONS":
        response = app.make_default_options_response()
        response.headers["Access-Control-Allow-Origin"] = request.headers.get("Origin")
        response.headers["Access-Control-Allow-Methods"] = "GET, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "*"
        response.headers["Access-Control-Allow-Credentials"] = "true"
        response.headers["Access-Control-Expose-Headers"] = (
            "Content-Disposition, Content-Length, Content-Type"
        )
        response.headers["Vary"] = "Origin"
        return response
    try:
        file_name = request.args.get("file")
        if not file_name:
            return jsonify({"error": "File parameter is required"}), 400

        output_path = os.path.join(PATH_OUTPUT, file_name)
        if not os.path.exists(output_path):
            return jsonify({"error": f"File not found: {file_name}"}), 404

        response = send_file(
            output_path,
            as_attachment=True,
            download_name=file_name,
            mimetype="image/png",
        )
        origin = request.headers.get("Origin")
        if origin in Config.CORS_ORIGINS:
            response.headers["Access-Control-Allow-Origin"] = origin
            response.headers["Access-Control-Allow-Credentials"] = "true"
            response.headers["Access-Control-Allow-Headers"] = ", ".join(
                Config.CORS_ALLOW_HEADERS
            )
            response.headers["Access-Control-Expose-Headers"] = (
                "Content-Disposition, Content-Length, Content-Type"
            )
            response.headers["Vary"] = "Origin"
        return response
    except FileNotFoundError as e:
        logging.exception("File not found error")
        return jsonify({"error": str(e)}), 404
    except ValueError as e:
        logging.exception("Value error")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logging.exception("Unexpected error in download_image")
        return jsonify({"error": "An unexpected error occurred"}), 500


@app.route("/api/health", methods=["GET"])
def health_check():
    """
    Health check endpoint
    ---
    tags:
      - system
    responses:
      200:
        description: Service is healthy
        examples:
          application/json: {
            "status": "healthy",
            "_links": {
              "upload": { "href": "/api/upload", "method": "POST" },
              "remove_background": { "href": "/api/remove-background", "method": "POST" },
              "add_background": { "href": "/api/add-background", "method": "POST" },
              "download": { "href": "/api/download", "method": "GET" }
            }
          }
    """
    return (
        jsonify(
            {
                "status": "healthy",
                "_links": {
                    "upload": {"href": "/api/upload", "method": "POST"},
                    "remove_background": {
                        "href": "/api/remove-background",
                        "method": "POST",
                    },
                    "add_background": {"href": "/api/add-background", "method": "POST"},
                    "download": {"href": "/api/download", "method": "GET"},
                },
            }
        ),
        200,
    )


if __name__ == "__main__":
    app.run(debug=True)
