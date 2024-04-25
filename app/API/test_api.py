from fastapi.testclient import TestClient
from datetime import datetime
from unittest.mock import MagicMock, patch


# import sys et os pour ajouter le chemin du répertoire parent
# au chemin du module pour importer les fonctions de requête MongoDB du fichier mongo_queries
# et l'API
import sys
import os

# ajout du chemin du répertoire parent au chemin du module
# pour importer les fonctions de requête MongoDB
sys.path.insert(0, os.path.dirname(__file__))

from api import api
from mongo_queries import (
    get_historical_data,
    get_transformed_data,
    get_prediction_data,
    advice,
)

# instanciation du client de test pour l'application FastAPI
client = TestClient(api)

# Test unitaire de simulation pour les fonctions de api.py


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
def test_get_historical_data():
    # création d'un filtre pour récupérer les données historiques d'une certaine période
    start_date = datetime(2020, 4, 26)
    end_date = datetime(2020, 4, 27)
    filter = {"timestamp": {"$gte": start_date, "$lt": end_date}}

    # création d'un mock pour la collection historique
    mock_collection = MagicMock()
    mock_collection.find.return_value = [
        {
            "_id": "1",
            "symbol": "BTCUSDT",
            "timestamp": datetime(2020, 4, 26),
            "open": 7539.03,
            "high": 7583,
            "low": 7522.17,
            "close": 7561.4,
            "volume": 2675.645139,
        }
    ]

    # utilisation du mock dans la fonction get_historical_data
    with patch("mongo_queries.collection_historical", mock_collection):
        # appel de la fonction get_historical_data avec le filtre
        result = get_historical_data(filter)

        # vérification que la fonction renvoie une liste de données historiques
        assert isinstance(result, list)

        # vérification que chaque élément de la liste contient les champs attendus
        for item in result:
            assert "_id" in item
            assert "symbol" in item
            assert "timestamp" in item
            assert "open" in item
            assert "high" in item
            assert "low" in item
            assert "close" in item
            assert "volume" in item


# test de la route pour récupérer les données historiques transformées
# définition de la fonction de test pour la route de récupération des données historiques transformées
def test_get_transformed_data():
    # définition un nombre d'éléments pour limiter les données (optionnel)
    number_of_items = 0
    limit = number_of_items if number_of_items else 0

    # création d'un mock pour la collection des données transformées
    mock_collection = MagicMock()
    mock_collection.find.return_value = [
        {
            "_id": "1",
            "open": 7503.13,
            "high": 7519.99,
            "low": 7478.07,
            "close": 7505.68,
            "volume": 3476.577759,
            "taux_variation": 0.5605724471688561,
        }
    ]

    # utilisation du mock dans la fonction get_transformed_data
    with patch("mongo_queries.collection_history_transformed", mock_collection):
        # appel de la fonction get_transformed_data avec le nombre d'éléments
        result = get_transformed_data(limit)

        # vérification que la fonction renvoie une liste de données transformées
        assert isinstance(result, list)

        # vérification que chaque élément de la liste contient les champs attendus
        for item in result:
            assert "_id" in item
            assert "open" in item
            assert "high" in item
            assert "low" in item
            assert "close" in item
            assert "volume" in item
            assert "taux_variation" in item


# test de la route pour récupérer les prédictions
# définition de la fonction de test pour la route de récupération des prédictions
def test_get_prediction_data():
    # création d'un filtre pour récupérer les données de prédiction d'une certaine période
    start_date = datetime(2024, 4, 22)
    end_date = datetime(2024, 4, 23)
    filter = {"timestamp": {"$gte": start_date, "$lt": end_date}}

    # création d'un mock pour la collection des données de prédiction
    mock_collection = MagicMock()
    mock_collection.find.return_value = [
        {
            "_id": "1",
            "timestamp": datetime(2024, 4, 22),
            "open": 7503.13,
            "high": 7519.99,
            "low": 7478.07,
            "close": 7505.68,
            "volume": 3476.577759,
            "next_close": 7510.0,
        }
    ]

    # Utiliser le mock dans la fonction get_prediction_data
    with patch("mongo_queries.collection_streaming", mock_collection):
        # appel de la fonction get_prediction_data avec le filtre
        result = get_prediction_data(filter)

        # vérification que la fonction renvoie une liste de données de prédiction
        assert isinstance(result, list)

        # vérification que chaque élément de la liste contient les champs attendus
        for item in result:
            assert "_id" in item
            assert "timestamp" in item
            assert "open" in item
            assert "high" in item
            assert "low" in item
            assert "close" in item
            assert "volume" in item
            assert "next_close" in item


# test de la route pour obtenir des conseils d'investissement
# définition de la fonction de test pour la route de récupération des conseils
# Test pour la fonction advice lorsque la collection des prédictions contient des données
def test_advice():
    # création d'un mock pour la collection des prédictions
    mock_collection = MagicMock()
    # simulation des données de prédiction
    prediction_data = {
        "_id": "1",
        "close": 7505.68,
        "next_close": 7503.13,
    }
    # définition du comportement du mock
    mock_collection.find_one.return_value = prediction_data

    # utilisation du mock dans la fonction advice
    with patch("mongo_queries.collection_streaming", mock_collection):
        result = advice()

        # vérification que la fonction retourne les conseils appropriés
        assert result["next_price"] == "7503.13 USD"
        assert result["actual_price"] == "7505.68 USD"
        assert (
            result["advice"]
            == "En vue de la diminution prochaine de la valeur nous vous conseillons de vendre"
        )
