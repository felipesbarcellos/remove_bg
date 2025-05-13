# Remove BG API [Projeto para Estudo]

## Descrição

O projeto **Remove BG** é uma API desenvolvida em Python utilizando o framework Flask. Ela permite realizar o upload de imagens, remover o fundo de imagens e adicionar um fundo personalizado. O objetivo principal é estudar as tecnologias utilizadas e compreender os conceitos de back-end utilizando protocolo http.

## Funcionalidades

- **Upload de Imagens**: Envie imagens para o servidor.
- **Remoção de Fundo**: Remova o fundo de uma imagem enviada.
- **Adição de Fundo**: Adicione um fundo personalizado a uma imagem.
- **Download de Imagens Processadas**: Baixe as imagens processadas diretamente do servidor.
- **Documentação Interativa**: Acesse a documentação interativa da API com Swagger.


## Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/felipesbarcellos/remove-bg.git
   cd remove_bg
   ```

2. Crie um ambiente virtual e ative-o:
   ```bash
   python -m venv .venv
   .\.venv\Scripts\activate
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

   **Principais dependências**:
   - Flask
   - Pillow
   - Flask-RESTful
   - pytest

## Uso

1. Inicie o servidor Flask:
   ```bash
   python main.py
   ```

2. Acesse a documentação interativa da API (Swagger):
   - URL: `http://localhost:5000/apidocs`

3. Utilize os endpoints disponíveis para:
   - Fazer upload de imagens.
   - Remover o fundo de imagens.
   - Adicionar um fundo personalizado (apenas RGB).
   - Baixar imagens processadas.

## Endpoints Principais

### 1. Upload de Imagem
- **URL**: `/api/upload`
- **Método**: `POST`
- **Descrição**: Envia uma imagem para o servidor.
- **Parâmetros**:
  - `file` (formData, obrigatório): O arquivo a ser enviado.

### 2. Remover Fundo
- **URL**: `/api/remove-background`
- **Método**: `POST`
- **Descrição**: Remove o fundo de uma imagem enviada.
- **Parâmetros**:
  - `file` (query, obrigatório): o nome e a extensão do arquivo.

### 3. Adicionar Fundo
- **URL**: `/api/add-background`
- **Método**: `POST`
- **Descrição**: Adiciona um fundo personalizado a uma imagem.
- **Parâmetros**:
  - `file` (query, obrigatório): o nome e a extensão do arquivo.
  - `color` (query, opcional): A cor do fundo a ser adicionado (opcional).

### 4. Download de Imagem Processada
- **URL**: `/api/download`
- **Método**: `GET`
- **Descrição**: Faz o download de uma imagem processada.
- **Parâmetros**:
  - `file` (query, obrigatório): O nome do arquivo a ser baixado, incluindo a extensão.

### 5. Health Check
- **URL**: `/api/health`
- **Método**: `GET`
- **Descrição**: Verifica o status da API.

## Testes

Para executar os testes automatizados, utilize o comando:
```bash
pytest tests/
```

Os testes cobrem:
- Upload de imagens.
- Remoção de fundo.
- Adição de fundo personalizado.
- Download de imagens processadas.
- Verificação de saúde da API.

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e pull requests.

## Licença

Este projeto está licenciado sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.
