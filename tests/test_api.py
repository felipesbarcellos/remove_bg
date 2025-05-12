import pytest
from flask.testing import FlaskClient
from util.api import app
import io

@pytest.fixture
def client():
    app.testing = True
    with app.test_client() as client:
        yield client

def test_upload_file(client: FlaskClient):
    # Test valid upload
    with open('imagens/entrada/teste.jpg', 'rb') as f:
        data = {'file': (f, 'teste.jpg')}
        response = client.post('/api/upload', data=data, content_type='multipart/form-data')
    assert response.status_code == 200
    assert 'fileName' in response.json

def test_upload_file_no_file(client: FlaskClient):
    # No file part in request
    response = client.post('/api/upload', data={}, content_type='multipart/form-data')
    assert response.status_code == 400
    assert 'error' in response.json

def test_upload_file_invalid_extension(client: FlaskClient):
    # Invalid file extension
    data = {'file': (io.BytesIO(b"fake data"), 'test.txt')}
    response = client.post('/api/upload', data=data, content_type='multipart/form-data')
    assert response.status_code == 400
    assert 'error' in response.json

def test_upload_file_empty_filename(client: FlaskClient):
    # Empty filename
    data = {'file': (io.BytesIO(b"fake data"), '')}
    response = client.post('/api/upload', data=data, content_type='multipart/form-data')
    assert response.status_code == 400
    assert 'error' in response.json

def test_add_background(client: FlaskClient):
    params = {'file': 'teste.jpg', 'color': '#FFFFFF'}
    response = client.post('/api/add-background', query_string=params)
    assert response.status_code == 200
    assert 'download_url' in response.json

def test_add_background_no_file(client: FlaskClient):
    params = {'color': '#FFFFFF'}
    response = client.post('/api/add-background', query_string=params)
    assert response.status_code == 400
    assert 'error' in response.json

def test_add_background_file_not_found(client: FlaskClient):
    params = {'file': 'notfound.jpg', 'color': '#FFFFFF'}
    response = client.post('/api/add-background', query_string=params)
    assert response.status_code == 404
    assert 'error' in response.json

def test_remove_background(client: FlaskClient):
    params = {'file': 'teste.jpg'}
    response = client.post('/api/remove-background', query_string=params)
    assert response.status_code == 200
    assert 'download_url' in response.json

def test_remove_background_no_file(client: FlaskClient):
    response = client.post('/api/remove-background')
    assert response.status_code == 400
    assert 'error' in response.json

def test_remove_background_file_not_found(client: FlaskClient):
    params = {'file': 'notfound.jpg'}
    response = client.post('/api/remove-background', query_string=params)
    assert response.status_code == 404
    assert 'error' in response.json

def test_download_image(client: FlaskClient):
    params = {'file': 'teste.png'}
    response = client.get('/api/download', query_string=params)
    assert response.status_code == 200
    assert response.content_type == 'image/png'

def test_download_image_no_file_param(client: FlaskClient):
    response = client.get('/api/download')
    assert response.status_code == 400
    assert 'error' in response.json

def test_download_image_file_not_found(client: FlaskClient):
    params = {'file': 'notfound.png'}
    response = client.get('/api/download', query_string=params)
    assert response.status_code == 404
    assert 'error' in response.json

def test_health_check(client: FlaskClient):
    response = client.get('/api/health')
    assert response.status_code == 200
    assert response.json.get('status') == 'healthy'
    assert response.status_code == 200
    assert 'healthy' in response.json.values()

def test_add_background(client: FlaskClient):
    params = {'file': 'teste.jpg', 'color': '#FFFFFF'}
    response = client.post('/api/add-background', query_string=params)
    assert response.status_code == 200
    assert 'download_url' in response.json

def test_remove_background(client: FlaskClient):
    params = {'file': 'teste.jpg'}
    response = client.post('/api/remove-background', query_string=params)
    assert response.status_code == 200
    assert 'download_url' in response.json

def test_download_image(client: FlaskClient):
    params = {'file': 'teste.png'}
    response = client.get('/api/download', query_string=params)
    assert response.status_code == 200
    assert response.content_type == 'image/png'
