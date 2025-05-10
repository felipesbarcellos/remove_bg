from flask import Flask, jsonify, request, send_file
from flasgger import Swagger
from util.ImageHandler import ImageHandler
import os
from util import setup_directories
from util.constants import PATH_INPUT, PATH_OUTPUT

app = Flask(__name__)
Swagger(app)

# Configuração para upload de arquivos
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/api/upload', methods=['POST'])
def upload_file():
    """
    Endpoint que recebe o caminho do arquivo e o salva no servidor
    ---
    parameters:
      - name: file
        in: formData
        type: file
        required: true
        description: O arquivo a ser enviado
        responses:
          200:
            description: Arquivo enviado com sucesso
            schema:
              type: object
              properties:
                filePath:
                  type: string
                  description: Caminho do arquivo salvo no servidor
          400:
            description: Erro ao enviar o arquivo
            schema:
              type: object
              properties:
                error:
                  type: string
                  description: Mensagem de erro"""
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

@app.route('/api/remove-background', methods=['POST'])
def remove_background():
    """
    Endpoint para remover o fundo da imagem
    ---
    parameters:
      - name: file
        in: query
        type: string
        required: true
        description: O nome do arquivo a ser processado com extensão
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
        # Obtém o caminho do arquivo a partir dos parâmetros da URL
        file_name = request.args.get("file")
        print(f"Received file path: {file_name}")

        if not file_name:
            return jsonify({"error": "File path is required"}), 400

        # Garantir que o caminho é absoluto e existe
        if not os.path.isabs(file_name):
            file_name = os.path.abspath(f"{PATH_INPUT}{file_name}")

        if not os.path.exists(file_name):
            return jsonify({"error": f"File not found: {file_name}"}), 404

        # Cria uma instância do ImageHandler
        handler = ImageHandler(os.path.join(PATH_INPUT, file_name))
        handler.remove_background()
        handler.save()        # Retorna o link para download
        # Pega apenas o nome base do arquivo (sem extensão) da entrada
        input_name = os.path.splitext(os.path.basename(file_name))[0]
        # A saída será sempre .png
        download_filename = f"{input_name}.png"
        print(f"Arquivo processado: {handler.output_path}")
        print(f"Nome do arquivo para download: {download_filename}")
        download_url = f"/api/image/download/{download_filename}"
        return jsonify({"message": "Background removed successfully", "download_url": download_url}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint para adicionar um fundo à imagem

@app.route('/api/add-background', methods=['POST'])
def add_background():
    """
    Endpoint para adicionar um fundo à imagem
    ---
    parameters:
      - name: file_name
        in: query
        type: string
        required: true
        description: O nome do arquivo a ser processado com extensão
      - name: color
        in: query
        type: string
        required: false
        description: A cor do fundo a ser adicionado (opcional)
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
        # Obtém o nome do arquivo e a cor do fundo a partir dos parâmetros da URL
        file_name = request.args.get("file")
        color = request.args.get("color", "#000")  # Preto como padrão

        if not file_name:
            return jsonify({"error": "File name is required"}), 400

        # Constrói o caminho completo do arquivo de entrada
        file_path = os.path.join(PATH_INPUT, file_name)

        if not os.path.exists(file_path):
            return jsonify({"error": f"File not found: {file_name}"}), 404

        # Cria uma instância do ImageHandler
        handler = ImageHandler(file_path)
        handler.add_background(color)
        handler.save()

        # Pega apenas o nome base do arquivo (sem extensão) da entrada
        input_name = os.path.splitext(file_name)[0]
        # A saída será sempre .png
        download_filename = f"{input_name}.png"
        print(f"Arquivo processado: {handler.output_path}")
        print(f"Nome do arquivo para download: {download_filename}")
        download_url = f"/api/image/download/{download_filename}"
        return jsonify({"message": "Background added successfully", "download_url": download_url}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint para download da imagem processada

@app.route('/api/download', methods=['GET'])
def download_image():
    """
    Endpoint para download da imagem processada
    ---
    parameters:
      - name: filename
        in: query
        type: string
        required: true
        description: O nome do arquivo a ser baixado + .png
    responses:
      200:
        description: Arquivo baixado com sucesso
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
    try:
        # Garante que estamos procurando por um arquivo PNG
        name_without_ext = request.args.get("file")

        # Corrige o caminho do arquivo de saída para evitar problemas de formatação
        output_path = os.path.abspath(os.path.join(PATH_OUTPUT, f"{name_without_ext}"))
        

        print(f"Tentando download do arquivo: {output_path}")

        # Verifica se o arquivo existe
        if not os.path.exists(output_path):
          return jsonify({"error": f"File not found: {output_path}"}), 404

        # Envia o arquivo para download com o nome original
        return send_file(
            output_path,
            as_attachment=True,
            download_name=f"{name_without_ext}"
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
