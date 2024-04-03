from fastapi.testclient import TestClient
from .main import app

# instanciation du client de test pour l'application FastAPI
client = TestClient(app)

# définition des tests unitaires pour les routes de l'API FastAPI


# test de la route pour récupérer la page d'accueil de l'API
# définition de la fonction de test pour la route de la page d'accueil
def test_get_home():
    # instanciation du client de test pour l'application FastAPI
    response = client.get("/")
    # réponse attendue pour le statut de la requête
    assert response.status_code == 200
    # réponse attendue pour le contenu de la réponse
    assert response.json() == {
        "message": "Bienvenue sur l'API de récupération de données historiques et de prédictions"
    }


# test de la route pour récupérer les données historiques
# définition de la fonction de test pour la route de récupération des données historiques
def test_get_historical():
    # instanciation du client de test
    response = client.get("/historical")
    # réponse attendue pour le statut de la requête
    assert response.status_code == 200
    # réponse attendue pour le contenu de la réponse
    # la réponse doit être une liste
    # car la route renvoie une liste de données historiques
    assert isinstance(response.json(), list)


# test de la route pour récupérer les prédictions
# définition de la fonction de test pour la route de récupération des prédictions
def test_get_prediction():
    # instanciation du client de test
    response = client.get("/predict")
    # réponse attendue pour le statut de la requête
    assert response.status_code == 200
    # réponse attendue pour le contenu de la réponse
    # la réponse doit être une liste
    # car la route renvoie une liste de prédictions
    assert isinstance(response.json(), list)
