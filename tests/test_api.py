import pytest
from flask.testing import FlaskClient
from util.api import app

@pytest.fixture
def client():
    app.testing = True
    with app.test_client() as client:
        yield client

def test_upload_file(client: FlaskClient):
    data = {
        'file': (open('imagens/entrada/teste.jpg', 'rb'), 'teste.jpg')
    }
    response = client.post('/api/upload', data=data, content_type='multipart/form-data')
    assert response.status_code == 200
    assert 'filePath' in response.json

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
