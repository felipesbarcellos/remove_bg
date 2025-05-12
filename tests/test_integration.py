import pytest
import os
from flask import Flask
from util.api import app


@pytest.fixture
def client():
    app.testing = True
    with app.test_client() as client:
        yield client


def test_health_check(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json["_links"]


def test_upload_image(client):
    data = {"file": (open("imagens/entrada/teste.jpg", "rb"), "teste.jpg")}
    response = client.post("/api/upload", data=data, content_type="multipart/form-data")
    assert response.status_code == 200


def test_remove_background(client):
    response = client.post("/api/remove-background?file=teste.jpg")
    assert response.status_code == 200


def test_add_background(client):
    response = client.post("/api/add-background?file=teste.jpg&color=255,255,255")
    assert response.status_code == 200


def test_download_image(client):
    response = client.get("/api/download?file=teste.png")
    assert response.status_code == 200
