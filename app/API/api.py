from datetime import datetime
from typing import List, Optional
from fastapi import FastAPI

# import sys et os pour ajouter le chemin du répertoire parent
# au chemin du module pour importer les fonctions
# de requête MongoDB du fichier mongo_queries
import sys
import os

# ajout du chemin du répertoire parent au chemin du module
# pour importer les fonctions de requête MongoDB
sys.path.insert(0, os.path.dirname(__file__))

from mongo_queries import (
    get_historical_data,
    get_transformed_data,
    get_prediction_data,
    advice,
    HistoricalData,
    TransformedData,
    PredictionData,
)

# définition de l'application FastAPI
api = FastAPI(
    title="API request historical data and predictions",
    version="1.0.0",
    openapi_tags=[
        {"name": "home", "description": "page d'accueil de l'API"},
        {
            "name": "historical",
            "description": "terminaisons requetes sur les données historiques",
        },
        {"name": "predict", "description": "terminaisons requetes sur les prédictions"},
    ],
)


# définition de la route pour la page d'accueil de l'API
@api.get("/", tags=["home"])
async def get_home():
    """
    Description:
    - Page d'accueil de l'API.

    Args:
    - Aucun argument n'est requis.

    Returns:
    - dict: Un message de bienvenue.
    """
    return {
        "message": "Bienvenue sur l'API de récupération de données historiques et de prédictions"
    }


# définition de la route pour récupérer les données historiques sur une période donnée
# pour les données historiques, nous utilisons le modèle HistoricalData pour la réponse
# la route est définie pour accepter des paramètres de requête start_date et end_date
# les paramètres de requête sont optionnels et peuvent être fournis pour filtrer les données historiques
# la route renvoie une liste de données historiques si aucune erreur n'est levée
@api.get("/historical", response_model=List[HistoricalData], tags=["historical"])
async def get_historical(
    start_date: Optional[datetime] = None, end_date: Optional[datetime] = None
):
    """
    Description:
    - Récupère des données historiques sur une période donnée.
    - La collection "historical_data" de la base de données "extract_data_binance" contient des données jusqu'il y a 4 ans.
    - Les données sont actualisées toutes les 24 heures.

    Args:
    - start_date (datetime, optional): Date de début de la période (format ISO), le format est "YYYY-MM-DD". Aucune date n'est fournie par défaut.
    - end_date (datetime, optional): Date de fin de la période (format ISO). le format est "YYYY-MM-DD". Aucune date n'est fournie par défaut.

    Returns:
    - list: Une liste HistoricalData contenant les données historiques sur la période demandée.
    """
    try:
        # définition du filtre pour la requête MongoDB en fonction des dates de début et de fin
        filter = {}
        # si les dates de début et de fin sont fournies, le filtre est défini
        if start_date and end_date:
            # définition du filtre pour la requête MongoDB en fonction des dates de début et de fin
            # timestamp est le champ utilisé pour filtrer les données historiques
            # $gte signifie "greater than or equal to" (supérieur ou égal à)
            # $lte signifie "less than or equal to" (inférieur ou égal à)
            filter = {"timestamp": {"$gte": start_date, "$lte": end_date}}

        # définition d'une variable pour stocker les données historiques
        # utilisation de la fonction get_historical_data pour récupérer les données historiques en fonction du filtre
        # la fonction prend en argument le filtre
        historical_data = get_historical_data(filter)

        # retourne les données historiques récupérées sous forme de liste HistoricalData si aucune erreur n'est levée
        return historical_data

    # lève une exception si une erreur est rencontrée
    except Exception as e:
        return {"error": str(e)}


# définition de la route pour récupérer une liste d'éléments de la collection "historical_data_transformed"
# pour les données transformées, nous utilons le modèle TransformedData pour la réponse
# la route est définie pour accepter un paramètre de requête number_of_items
# le paramètre de requête est optionnel et peut être fourni pour limiter les données transformées
@api.get(
    "/historical_transformed", response_model=List[TransformedData], tags=["historical"]
)
async def get_transformed(number_of_items: Optional[int] = None):
    """
    Description:
    - Récupère une liste d'éléments de la collection "historical_data_transformed" de MongoDB.
    - La collection "historical_data_transformed" contient des données transformées à partir des données historiques.
    - Les données sont actualisées toutes les 24 heures.

    Args:
    - number_of_items (int, optional): Nombre d'éléments à récupérer. Aucun nombre n'est fourni par défaut.

    Returns:
    - list: Une liste TransformedData contenant les données transformées récupérées.

    """
    try:
        # définition d'une variable pour stocker la limite des données
        # si la limite est fournie, les données sont récupérées en fonction de la limite
        # sinon, toutes les données sont récupérées
        limit = number_of_items if number_of_items else 0
        # définition d'une variable pour stocker les données transformées
        # utilisation de la fonction get_transformed_data pour récupérer les données transformées
        # la fonction prend en argument le nombre d'éléments à récupérer
        # récupèration des données transformées en fonction de la limite
        transformed_data = get_transformed_data(limit)

        # retourne les données transformées récupérées sous forme de liste TransformedData si aucune erreur n'est levée
        return transformed_data

    # lève une exception si une erreur est rencontrée
    except Exception as e:
        return {"error": str(e)}


# définition de la route pour récupérer les données de prédiction sur une période donnée
# pour les données de prédiction, nous utilisons le modèle PredictionData pour la réponse
# la route est définie pour accepter des paramètres de requête start_date et end_date
# les paramètres de requête sont optionnels et peuvent être fournis pour filtrer les données de prédiction
# la route renvoie une liste de données de prédiction si aucune erreur n'est levée
@api.get("/predict", response_model=List[PredictionData], tags=["predict"])
async def get_prediction(
    start_date: Optional[datetime] = None, end_date: Optional[datetime] = None
):
    """
    Description:
    - Récupère des données de prédiction relative à la valeur de clôture sur une période donnée.

    Args:
    - start_date (datetime, optional): Date de début de la période (format ISO), le format est "YYYY-MM-DD". Aucune date n'est fournie par défaut.
    - end_date (datetime, optional): Date de fin de la période (format ISO). le format est "YYYY-MM-DD". Aucune date n'est fournie par défaut.

    Returns:
    - list: Une liste PredictionData contenant les données de prédiction sur la période demandée.
    """
    try:
        # définition du filtre pour la requête MongoDB en fonction des dates de début et de fin
        filter = {}
        # si les dates de début et de fin sont fournies, le filtre est défini
        if start_date and end_date:
            # définition du filtre pour la requête MongoDB en fonction des dates de début et de fin
            # timestamp est le champ utilisé pour filtrer les données historiques
            # $gte signifie "greater than or equal to" (supérieur ou égal à)
            # $lte signifie "less than or equal to" (inférieur ou égal à)
            filter = {"timestamp": {"$gte": start_date, "$lte": end_date}}

        # récupération des données de prédiction en fonction du filtre
        prediction_data = get_prediction_data(filter)
        # retourne les données de prédiction récupérées sous forme de liste PredictionData si aucune erreur n'est levée
        return prediction_data

    # lève une exception si une erreur est rencontrée
    except Exception as e:
        return {"error": str(e)}


@api.get("/invest", name="Investment adviser", tags=["predict"])
async def get_advise():
    """
    Description:
    - Point de terminaison permettant d'obtenir un conseil d'investissement sur le BITCOIN.

    Args:
    - Aucun argument n'est requis.

    Returns:
    - dict: valeur prochaine prédite de la paire BTCUSDT, valeur actuelle de la paire, conseil.
    """
    return advice()


# # exécution de l'API FastAPI
# # point d'entrée de l'application FastAPI pour l'exécution de l'API
# if __name__ == "__main__":
#     import uvicorn

# uvicorn.run(api, host="0.0.0.0", port=8000)

# # exécution de l'API Fastapi dans le terminal
# # uvicorn api:api --reload ou python3 api.py
