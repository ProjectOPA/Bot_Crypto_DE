from datetime import datetime
from typing import List, Optional
from fastapi import FastAPI
from mongo_queries import (
    get_historical_data,
    get_prediction_data,
    HistoricalData,
    PredictionData,
)

# définition de l'application FastAPI
app = FastAPI(
    title="API request historical data and predictions",
    version="1.0.0",
    openapi_tags=[
        {"name": "home", "description": "page d'accueil de l'API"},
        {
            "name": "historical",
            "description": "page requete sur les données historiques",
        },
        {"name": "predict", "description": "page requete sur les prédictions"},
    ],
)


# définition de la route pour la page d'accueil de l'API
@app.get("/", tags=["home"])
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
@app.get("/historical", response_model=List[HistoricalData], tags=["historical"])
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
            filter = {"timestamp": {"$gte": start_date, "$lte": end_date}}
        # récupération des données historiques en fonction du filtre
        historical_data = get_historical_data(filter)
        # retourne les données historiques récupérées sous forme de liste HistoricalData si aucune erreur n'est levée
        return historical_data
    # lève une exception si une erreur est rencontrée
    except Exception as e:
        return {"error": str(e)}


# définition de la route pour récupérer les données de prédiction sur une période donnée
# pour les données de prédiction, nous utilisons le modèle PredictionData pour la réponse
# la route est définie pour accepter des paramètres de requête start_date et end_date
# les paramètres de requête sont optionnels et peuvent être fournis pour filtrer les données de prédiction
# la route renvoie une liste de données de prédiction si aucune erreur n'est levée
@app.get("/predict", response_model=List[PredictionData], tags=["predict"])
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
            filter = {"timestamp": {"$gte": start_date, "$lte": end_date}}
        # récupération des données de prédiction en fonction du filtre
        prediction_data = get_prediction_data(filter)
        # retourne les données de prédiction récupérées sous forme de liste PredictionData si aucune erreur n'est levée
        return prediction_data
    # lève une exception si une erreur est rencontrée
    except Exception as e:
        return {"error": str(e)}


# exécution de l'API FastAPI
# lorsque le script est exécuté en tant que programme principal
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

# exécution de l'API Fastapi dans le terminal
# uvicorn main:app --reload ou python main.py
