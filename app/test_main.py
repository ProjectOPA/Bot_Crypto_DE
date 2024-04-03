from fastapi.testclient import TestClient
from .main import app

client = TestClient(app)


def test_get_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Bienvenue sur l'API de récupération de données historiques et de prédictions"
    }


def test_get_historical():
    response = client.get("/historical")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_prediction():
    response = client.get("/predict")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
