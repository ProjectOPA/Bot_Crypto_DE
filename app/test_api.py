from fastapi.testclient import TestClient
from datetime import datetime
from .api import app
from .mongo_queries import get_historical_data, get_prediction_data

# instanciation du client de test pour l'application FastAPI
client = TestClient(app)

# Tests unitaires pour les routes de l'API FastAPI


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


# Test unitaire pour les fonctions de requête mongo_queries.py


# test de la fonction pour récupérer des données historiques de MongoDB sans filtre (aucun filtre)
# définition de la fonction de test pour la fonction get_historical_data() sans filtre
def test_get_historical_data_no_filter():
    # appel de la fonction get_historical_data() sans filtre
    data = get_historical_data()
    # vérification que la réponse est une liste
    assert isinstance(data, list)
    # # vérification que la réponse n'est pas vide (à vérifier une fois que le chemin soit correct)
    # assert len(data) > 0


# test de la fonction pour récupérer des données de historiques de MongoDB avec filtre
# définition de la fonction de test pour la fonction get_historical_data() avec filtre
def test_get_historical_data_with_filter():
    # définition d'un filtre pour la requête MongoDB
    # le filtre est un dictionnaire avec les dates de début et de fin
    filter = {"timestamp": {"$gte": "2020-05-24", "$lte": "2020-05-26"}}
    # appel de la fonction get_historical_data() avec filtre
    data = get_historical_data(filter)
    # vérification que la réponse est une liste
    assert isinstance(data, list)
    # # vérification que la réponse n'est pas vide(à vérifier une fois que le chemin soit correct)
    # assert len(data) > 0


# # test de la fonction pour récupérer des données de prédiction de MongoDB sans filtre (aucun filtre)
# # définition de la fonction de test pour la fonction get_prediction_data() sans filtre
# def test_get_prediction_data_no_filter():
#     # appel de la fonction get_prediction_data() sans filtre
#     data = get_prediction_data()
#     # vérification que la réponse est une liste
#     assert isinstance(data, list)
#     # vérification que la réponse n'est pas vide
#     assert len(data) > 0 (à vérifier une fois que le chemin soit correct)

# test de la fonction pour récupérer des données de prédiction de MongoDB avec filtre
# définition de la fonction de test pour la fonction get_prediction_data() avec filtre
# def test_get_prediction_data_with_filter():

#     # définition d'un filtre pour la requête MongoDB
#     # le filtre est un dictionnaire avec les dates de début et de fin
#     filter = {"timestamp": {"$gte": "2020-05-24", "$lte": "2020-05-26"}}
#     # appel de la fonction get_prediction_data() avec filtre
#     data = get_prediction_data(filter)
#     # vérification que la réponse est une liste
#     assert isinstance(data, list)
#     # vérification que la réponse n'est pas vide
#     assert len(data) > 0 (à vérifier une fois que le chemin soit correct)
